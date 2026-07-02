---
title: Recovering a diverged branch without force-push: reset the ref to the real remote tip, then cherry-pick only your one genuinely new commit
date: 2026-07-02
category: infra
tags: worktree, ci, rollback
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A local branch that had been reconstructed from an existing pull request's tip ended up with different commit SHAs than the actual remote branch for what were logically the same changes — a stray local operation had rewritten history that should have stayed identical to the remote. The two branches now disagreed on every commit, even though only one of them (the newest one) represented real, not-yet-published work.

The loss-safe recovery, without ever force-pushing: point the local branch reference directly at the real remote tip (checkout a new branch from the remote ref, replacing the local one entirely — this discards nothing because the remote tip already has everything except the one new commit), identify the single commit that is genuinely new and not already represented on the remote tip, cherry-pick just that one commit on top, and then push normally — a plain fast-forward, since the branch now has the remote's exact history plus one new commit at the end.

The generalizable rule: when a local branch has diverged from its remote counterpart for a PR that's still open, the fix is never to force-push a rewritten history over the remote — that risks clobbering real work that only exists on the remote side, or a collaborator's changes. Instead, isolate exactly which commits are genuinely new and not represented upstream, reset the local ref to match the remote exactly, and replay only the genuinely-new commits on top. This reduces every divergence-recovery case to a small, auditable diff instead of a full history rewrite, and the resulting push is always a fast-forward.
