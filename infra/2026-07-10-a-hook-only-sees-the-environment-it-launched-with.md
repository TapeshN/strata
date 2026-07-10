---
title: A pre-tool hook only sees the environment it launched with
date: 2026-07-10
category: infra
tags: [hooks, process-environment, bypass-flags, shell-export, debugging]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

If a guard, hook, or middleware process reads an environment variable to decide whether to allow or block an action, setting that variable in a shell *after* the guarding process has already started will not affect it — and any documentation telling a user to "export FOO=1 to bypass" mid-session is misleading.

**What happened.** A long-running automation process had a pre-check step that inspected an environment variable to decide whether to allow a certain kind of dispatch. Partway through a session, an operator tried to unblock that dispatch by running `export SOME_FLAG=1` in their interactive shell and expected the check to pick it up. It didn't. The reason is structural: the guarding process had already been launched, and its environment was a snapshot taken at that launch time (in this case inherited from the parent process that started the whole session). A later `export` in a *different*, already-running shell session changes that shell's own environment going forward, but it cannot reach backward into a sibling or parent process's environment — environment variables propagate downward at process-spawn time only, never sideways or backward between already-running processes.

**How to apply.** When you build a gate that reads an env var as a bypass or feature flag, be explicit about the propagation boundary: either (1) require the flag to be set before the guarded process starts (via its launch command, a systemd/launchd environment block, or a full restart), or (2) have the gate re-read a file or external config on every check instead of a frozen process environment, if you actually want live mid-session toggling. If you can't change the gate, don't fight it — route around it: many gates only watch one code path (e.g. a specific automated dispatch mechanism), so the same change made through a different, ungated path (direct manual edits, a different tool) may be unaffected. Diagnose "my export didn't work" by asking which process actually reads the variable and when it was forked, not by re-running the export.
