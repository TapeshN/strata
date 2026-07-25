---
title: A merge whose history contains a revert of an ancestor commit can silently drop every file that commit touched but your branch never revisited
date: 2026-07-25
category: guardrails
tags: [git, revert-of-merge, reconciliation, verify-dont-trust]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

When a feature is built across two branches — one that introduces the groundwork and a second, later branch that continues it — and somewhere on the trunk that groundwork merge gets reverted before the continuation lands, merging trunk into the continuation branch can silently destroy the entire original contribution, with zero merge conflicts reported. The mechanism: the merge-base is the groundwork commit itself. For every file the continuation branch never touched again after that base, the trunk's revert reads as simply "the newer change" and wins outright — no conflict marker, nothing to review. Only the handful of files both sides had touched since the base show up as conflicts, which makes the merge look fully resolved when the conflict list is actually a small fraction of the real damage.

The class rule: after any merge whose ancestry contains a revert of a commit that is also an ancestor of your branch, do not trust the conflict list as the damage list. Diff the merged result against your branch's own tip across the feature's entire footprint, not just the files the merge flagged. For each file that differs, confirm whether it is a pure revert (identical to the pre-revert state) before restoring it wholesale, and for any file where the trunk also advanced legitimately since the revert, reapply your branch's specific delta on top rather than blindly overwriting. This was only caught because the post-merge verification ran the complete test suite rather than a targeted subset — a partial verify would have reported green on a merge that had quietly erased most of a feature.
