---
title: A plain git fetch of one branch can under-report a moved ref, and a sibling's merge-tree conflict may be the sibling's own rebase debt
date: 2026-08-17
category: infra
tags: [git, verification, reconcile]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Multiple agents working the same reconciliation session found that a plain `git fetch origin
<branch>` reported a stale remote-tracking tip for that branch while directly querying the remote
(`git ls-remote`) showed the real, already-moved tip — reconciling against the plain-fetch result
would have re-created a conflict that had already been resolved upstream. A plain fetch of a single
named branch can, in some situations, update the special FETCH_HEAD marker without correctly
advancing the persistent remote-tracking ref that later merge operations actually read. Before any
reconciliation against a shared branch, fetch using the explicit source-and-destination refspec
form (or independently confirm via a direct remote query) rather than trusting a plain fetch to
have moved the tracking ref.

Separately, a reviewer's mergeability check flagged one branch as "conflicting" with the branch
under review on several files — but those files turned out not to be part of the reviewed branch's
own changeset at all; they were the OTHER branch's unrelated divergence from an older shared
history. A raw mergeability check between two branches surfaces every difference in their combined
history, including one branch's own un-reconciled distance from trunk, which can make it look like
the branch under review is at fault. The fix is to intersect any reported conflicting files against
the branch actually under review's own changeset before assigning blame — a conflict outside that
changeset is the OTHER branch's rebase debt to resolve, not a defect in the one being reviewed.
