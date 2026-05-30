---
title: Worktree guard activates on directory existence, not upstream registration
date: 2026-05-30
category: infra
tags: [worktree, multi-repo, guardrails, parallel-sessions]
confidence: learned
source: private-work
---

When a new repo directory is created under a multi-repo workspace root, the PreToolUse worktree guard activates for that directory immediately — it does not wait for the repo to be pushed to a remote, registered in a manifest, or tagged in any config file. The guard keys on filesystem presence alone.

This means the bootstrapping window (git init through first push) requires an intentional bypass. The pattern that works: use the bypass for the minimum number of commits needed to get the repo live upstream, then work in worktrees from that point forward exactly like any other sub-repo in the workspace.

The broader lesson: mechanical enforcement at the filesystem level is stricter and more reliable than enforcement that depends on a registry or remote state. A guard that activates on directory presence catches accidental edits even before the repo has any history — which is the right tradeoff for a workspace where parallel sessions share the same root.

The corollary: when planning a new repo bootstrap, budget for 1–2 commits using the bypass, treat them as infrastructure-only commits (no feature work), and switch to the worktree model immediately after the first push lands.
