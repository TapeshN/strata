---
title: An unattended scheduled task silently hangs on a permission prompt when its first command is not allow-listed
date: 2026-06-20
category: infra
tags: [autonomy, gating, lifecycle, ci]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A nightly scheduled task produced zero output for six consecutive runs. The diagnostic turned on the permission layer: the task's first step was a standalone environment variable export. The scheduled runner executes each step as a Bash tool call under the project's permission settings, and `export` was not in the allow-list. With no human present to approve the prompt, the call hung and was killed before the task's real work could begin. The run log showed a closed stream, not a code error — the failure mode is invisible unless you know to look at the permission layer first.

The immediate fix is to inline the environment variable into the command that actually needs it (`VAR=value cmd`) rather than exporting it as a standalone step. A variable inlined into a command rides the command's existing permission grant; it does not require its own entry in the allow-list. The structural fix is a rule: every early step in an unattended task must either be in the allow-list or be expressed as an inline argument to an already-allowed command.

Diagnosing a stalled unattended job: check the permission layer before looking at code. An interactive session would simply prompt the human and continue; the stall class is invisible in interactive runs and surfaces only under headless execution. A silent hang with no error output and no CPU activity is the signature of a permission-prompt timeout, not a runtime error.

A secondary gap: the monitoring signal for this class of failure was measuring last-successful-deposit, not last-run-attempt. A task that hangs at step one increments the run counter but never reaches the deposit step, so a deposit-lag monitor never fires. The correct signal for an unattended channel is active liveness: did the task run within the expected window, regardless of what it produced?
