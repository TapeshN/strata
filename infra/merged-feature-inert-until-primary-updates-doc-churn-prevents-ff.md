---
title: A merged feature is inert until the primary checkout updates; perpetual doc-churn dirtiness prevents the fast-forward that would make it live
date: 2026-06-14
category: infra
tags: [worktree, multi-repo, docs, ci, loop]
confidence: learned
source: private-work
---

A feature merged to the main branch on the remote is not "live" in any workflow or tool that runs from a local primary checkout that hasn't been updated. If the primary checkout is perpetually dirty with uncommitted working-file changes (e.g., a running doc state that accumulates edits but is never committed), the safe fast-forward (`pull --ff-only`) that would advance the checkout is skipped as a loss-safety measure. The result:

- Merged code features are latent — any tool or scheduled task that runs from the primary executes the pre-merge version of the code, silently.
- The uncommitted doc working-set is at risk — days of state live only in local working files, not in git history.

**The cascade:** perma-dirty primary → fast-forward skipped → primary goes stale → scheduled tasks run stale code → merged capabilities are inert → the primary's stale-behind count grows → the problem compounds.

**Safe reconcile recipe when the primary is dirty and behind:**
1. Check the conflict surface first: compare the set of incoming merged changes against the set of locally-modified files. If the intersection is small (typically near-zero for doc-churn vs. code merges), the reconcile is low-risk.
2. Back up runtime append-only ledger files that were modified but not committed.
3. Stash the working-file changes (or move them aside).
4. Apply the fast-forward.
5. Re-apply the stashed changes and restore the backed-up ledger appends.
6. Verify the feature that was previously latent is now live.

**Bootstrap-safe fix pattern for scheduled tasks:** if a tool or cron job runs from a primary checkout on a schedule, add a preflight step that detects a clean primary and fast-forwards it before running. This ensures a merged change activates on the next scheduled run without requiring a manual primary reconcile.

**The class fix:** the root cause is doc-state that never gets committed. A regular doc-sweep cadence (committing control-plane doc changes to main) keeps the primary clean enough that fast-forwards succeed automatically.
