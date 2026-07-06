---
title: Merging one layer of a stacked pull-request set with an auto-delete-branch option can permanently close its open dependents
date: 2026-06-30
category: orchestration
tags: [dag, gating, ci, multi-repo]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When a set of pull requests is stacked (a later PR's base branch is an earlier PR's still-open head branch), merging the earlier layer with an option that also deletes its branch can close the dependent PR outright rather than retargeting it. The hosting platform only retargets a child PR to the parent's merge target in some cases; deleting the base branch of an open PR can close it as an unintended side effect, and a PR whose base branch no longer exists generally cannot be reopened through the normal UI or API path. The recovery is to open a fresh pull request from the dependent's surviving head branch against the real target branch — the original PR's history and number are lost.

The generalizable rule for merging any stacked set: never delete a branch that still has an open dependent. The correct order is (1) merge the foundational layer without deleting its branch, (2) retarget each direct dependent's base to the new merge target, (3) rebase the dependent onto the updated target in isolation, (4) merge it, and only then (5) reclaim branches once the entire stack has landed. Treat "does this branch have an open child PR" as a mandatory check before any merge action that also deletes the branch.
