---
title: When N parallel PRs fail the identical check, fix at the shared base and merge-forward — not N times
date: 2026-06-24
category: orchestration
tags: [parallel-sessions, multi-repo, ci, gating]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When several parallel branches independently fail the same CI check, the natural impulse is to fix each branch. That is the wrong response: it is N times the work, each fix can drift, and it treats a single cause as N separate bugs.

The pattern: all branches share a base where one component had a defect. The same check fails on every branch that includes that component because they all include the same broken base. The fix lives in exactly one place — the shared base.

**The correct sequence:** diagnose the common failure on the shared base BEFORE touching any downstream branch; land the fix on the base; then run a clean `git merge origin/main` (or equivalent) on each affected branch. Each branch picks up the fix with no per-branch code change, no rebuild of the fix, and no divergence.

The triage signal is the identity of the failure, not its count. When two or more branches report the same check failing at the same component, confirm the fix belongs on the base and stop dispatching per-branch remediation until the base is green.
