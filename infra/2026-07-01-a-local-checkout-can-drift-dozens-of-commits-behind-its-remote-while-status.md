---
title: A local checkout can drift dozens of commits behind its remote while status checks report nothing wrong
date: 2026-07-01
category: infra
tags: [worktree, parallel-sessions, drift, git]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

In a workflow where most work lands via isolated branches merged directly to a shared remote, and only one coordinating checkout is allowed to receive direct edits to control-plane files, that coordinating checkout can silently fall far behind — tens of commits — while nothing about its local status looks wrong. A routine status check only diffs a checkout against its own last-known state, not against the remote; it cannot reveal "behind," only "dirty." Meanwhile, direct edits to shared documents kept landing on top of an increasingly stale base, compounding the drift across a long working session.

The consequence of this class of drift is not cosmetic: files and modules that had already been merged upstream can be entirely missing from the local working directory, so any process that reads "the current state" from that checkout — grounding an important operation in supposedly-current documentation, for instance — is silently working from a stale snapshot with no error to signal it.

The fix at source is procedural and needs to be a habit independent of who did the most recent merge: any session that merges anything into a shared remote should refresh every checkout that tracks that branch, not only its own. And before trusting any coordinating checkout's contents for a consequential operation, explicitly fetch and diff against the remote — a plain status check is not sufficient evidence of freshness, only of local cleanliness.
