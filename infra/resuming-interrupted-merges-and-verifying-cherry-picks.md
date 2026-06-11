---
title: Interrupted merges resume cleanly per-worktree; cherry-picks get verified against the production tree
date: 2026-06-11
category: infra
tags: [worktree, merge, testing]
confidence: learned
source: private-work
---

Three mechanics from an agent that inherited orphaned work after a machine reboot:

- **A worktree abandoned mid-merge resumes cleanly.** Merge state (including the prepared merge message) persists per-worktree under the repo's worktree metadata, so the recovery is just: resolve the remaining conflict markers, stage, commit. No need to abort and redo the merge — the interrupted state is durable and legitimate.
- **Cherry-picking a fix from an unmerged sibling branch carries that branch's assumptions.** Before accepting the pick, verify every selector/identifier the picked code targets actually exists in the tree you're landing on — the sibling may reference elements only *it* introduces. A pick that compiles can still target phantoms.
- **Run convention-dependent checks from the directory that owns the convention.** A module using bare sibling imports (by pre-existing local convention) import-checks correctly only from its own directory, not the project root. The check must replicate the runtime's working directory, or it tests a world that never executes.
