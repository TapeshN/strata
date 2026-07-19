---
title: Reconciling a behind-AND-dirty shared primary: snapshot first, re-apply deterministically, stash the churning ledgers
date: 2026-07-18
category: infra
tags: [git, reconciliation, stash-pop-partial-fail, shared-primary, loss-safe, runtime-ledger-churn]
confidence: learned
source: private-work
---

A shared working copy that is both BEHIND its remote and DIRTY with runtime ledger churn needs a deterministic recovery order: snapshot the dirty state first (a stash with a message, or a WIP commit on a branch), fast-forward to the remote, then re-apply the snapshot. Never fast-forward over tracked edits, and treat append-only ledger files as the churn class most likely to conflict — re-apply them last and verify the pop completed cleanly, because a partial stash-pop fails silently on conflicted paths.
