---
title: Never merge on pending or red CI — confirm green independently and refresh stale branches first
date: 2026-06-20
category: guardrails
tags: [gating, ci, preflight, determinism, lifecycle]
confidence: learned
source: private-work
---

Two related failures exposed the same gap in merge discipline during an autonomous multi-PR run. In the first case, a pull request was merged while its CI status was still pending — it happened to pass, but that was luck rather than verified correctness. In the second case, CI was genuinely red, but the redness was caused by branch staleness: a long-lived branch had been cut early in the run and had not absorbed a fix that had since landed on the main branch via a different PR, causing roughly a dozen tests to fail against an already-corrected codebase.

The root cause was twofold. First, the branch-protection configuration did not enforce the primary test-and-preflight workflow as a required status check, so the merge path remained open on pending or red CI — the coordinator's own discipline was the only gate, and that discipline slipped. Second, no step in the merge process required confirming that a long-lived branch was current with the main branch before trusting its CI result.

The corrective pattern that proved effective: before merging any PR, independently verify CI status through the tooling (not by relying on a summary from a prior step or a handback message), and explicitly check whether the branch is stale relative to the current tip of the main branch. If staleness is detected, rebase or merge from main, let CI re-run on the refreshed branch, and only then confirm green before proceeding.

The durable structural fix is to make the primary test workflow a required status check at the repository level, so that a merge on pending or red CI is mechanically blocked regardless of coordinator discipline. This converts a soft norm into a hard gate and eliminates the class of slip entirely.

The broader lesson: a terminal verification step whose scope includes 'is CI actually green right now on the current branch tip' catches failures that a code-correctness review alone will miss. Witness the state; do not assert it from memory or delegate its confirmation to an earlier step in the same session.
