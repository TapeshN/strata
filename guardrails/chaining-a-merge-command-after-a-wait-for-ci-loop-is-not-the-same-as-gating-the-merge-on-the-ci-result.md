---
title: Chaining a merge command after a wait-for-CI loop is not the same as gating the merge on the CI result
date: 2026-07-02
category: guardrails
tags: [ci, release, gating]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A pull request was merged while one of its checks was actually failing, because the merge command was fired in the same shell chain immediately after a loop that waited for checks to stop being pending — and "no longer pending" includes both "passed" and "failed." The loop exited correctly; the merge then ran without anyone reading whether the checks that finished were green or red.

In this case the outcome was benign (the failing check turned out to be a pre-existing, already-diagnosed issue unrelated to the change), but the ordering was wrong regardless: triage happened after the merge instead of before it, purely by luck rather than by design.

The fix: never chain "wait for checks to finish" and "merge" in one uninterrupted command sequence. Explicitly read the check results and confirm zero failures before issuing the merge — a short guard that counts failing checks and refuses to proceed if the count is nonzero is enough. A wait loop that exits on "nothing pending" will exit on outright failure just as readily as on success, so pending-status alone is never sufficient permission to merge.
