---
title: Read CI verdicts from named check conclusions, not pipeline exit codes
date: 2026-06-10
category: guardrails
tags: [ci, gating, verify-dont-trust, release]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A merge decision based on a pipeline command's exit code will sometimes be wrong. The exit code of a pipeline that includes filtering, pagination, or line-counting commands reflects the last command in the chain, not the job outcome. Two merges landed on wrong branches — one on pending CI, one on red CI — because the decision came from the exit code of a command that happened to succeed even when the CI results it was summarizing contained failures.

The reliable check: read named check conclusions. After any CI run, the source of truth is the list of named required checks and their conclusion fields. A merge is safe when every required check has a conclusion of "success"; any other state (pending, failing, neutral, skipped) is not a green.

Two adjacent traps with the same root:

- **The top-of-run-list trap.** The most recent entry in a CI run list is not necessarily the most recent run for the relevant pull request. Runs appear in creation order, not completion order, and a re-triggered run may not yet appear. Drill to the specific workflow event and step rather than trusting the list ordering.
- **The whole-failure-list trap.** When a CI check fails, reading only the first failure and acting on it can miss a second, distinct failure that will keep CI red after the first fix lands. Read the complete failure list before acting on any item.

The reliable protocol: query the named check status on the specific pull request, count the rows with a non-success conclusion, and merge only when that count is zero. For automation, the count is the gate — not the exit code of the query command.
