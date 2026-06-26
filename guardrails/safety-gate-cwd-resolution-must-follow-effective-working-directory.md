---
title: A safety gate that resolves branch from invoking cwd will false-block legitimate worktree operations
date: 2026-06-23
category: guardrails
tags: [worktree, gate-calibration, false-positive, cwd-resolution, destructive-guard]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A gate that checks "are you on a protected branch?" by reading the branch of the shell's invoking current working directory will produce false positives whenever a compound command navigates away before the protected operation. If the primary checkout is parked on `main` and a script leads with `cd primary && … && cd worktree && git <operation>`, the gate fires on the primary's `main`, not on the worktree's feature branch where the operation actually runs.

This false-block is silent from the developer's point of view: the worktree is correctly branched, the operation is legitimate, and the gate rejects it anyway. The defect is in how the gate reads branch state, not in what the developer did.

The correct fix is for the gate to derive the target branch from the effective working directory — the directory that git will actually operate on — rather than from the hook's invoking cwd. In practice this means parsing the command for an explicit `-C <path>` flag or following any `cd` navigation steps that precede the git command.

Until the gate is fixed, the safe workaround is to never prefix worktree git operations with a `cd` into the primary. Keep each git command single-purpose and start from the worktree's own directory. Avoid chaining a commit and a push in the same shell expression — run them as separate, sequential commands.

The broader class: any hook that resolves state (branch, repo, env) from the hook process's own cwd instead of the command's effective target will produce false positives for compound navigation patterns. Gate resolution logic should follow the operation, not the invoker.
