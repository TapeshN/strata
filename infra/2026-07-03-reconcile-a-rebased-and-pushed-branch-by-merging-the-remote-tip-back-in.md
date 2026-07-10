---
title: Reconcile a rebased-and-pushed branch by merging the remote tip back in, never by force-pushing
date: 2026-07-03
category: infra
tags: [worktree, release, rollback]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

An automated post-merge maintenance routine rebased an already-pushed, in-flight feature branch onto a newly advanced main branch. Because the remote copy of that branch still held the pre-rebase commits, a subsequent plain push was rejected, and the path of least resistance looked like a force-push — a destructive-class operation that rewrites remote history and can silently discard anything else that landed on that branch in the meantime.

There is a loss-free alternative that avoids the destructive operation entirely: merge the remote branch's current tip back into the freshly rebased local branch. Where the two histories contain identical underlying changes (as they do right after a pure rebase with no new remote commits), this merge resolves automatically with no conflicts, and a subsequent plain, fast-forward-compatible push succeeds — the history gains one extra merge commit, but nothing already on the remote branch is rewritten or lost, and any open pull request tied to that branch remains intact throughout.

The generalizable rule for any automated tooling that rebases branches which may already have a remote counterpart: reconcile local/remote divergence after a rebase by merging the remote tip back in, never by defaulting to a force-push. Where practical, the safer long-term fix is for the automated routine itself to detect that a target branch already has un-rebased remote commits and skip rebasing it, leaving that reconciliation to a human or a deliberate follow-up step.
