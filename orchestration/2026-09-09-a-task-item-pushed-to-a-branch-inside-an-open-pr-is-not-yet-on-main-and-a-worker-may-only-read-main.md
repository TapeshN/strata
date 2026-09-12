---
title: A task item pushed to a branch inside an open PR is not yet "on main" — and a worker may only ever read what's on main
date: 2026-09-09
category: orchestration
tags: [artifact-is-on-main-not-in-a-commit, repeated-own-lesson-same-session, brief-has-no-done-state, worker-refusal-was-correct]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A full, ready-to-paste dispatch prompt was written for a client-work item that had, in fact, only been committed to a feature branch inside a still-open pull request — never merged to the shared main branch. The downstream worker correctly refused the dispatch, citing that the item was absent from the current shared branch and that the standing rule forbids reconstructing an item from chat history when it isn't there. No worktree, branch, or PR got created on the wrong premise — the refusal cost only the one round trip.

What made this worth recording is that, earlier in the very same working session, the same person had written — in a commit message — that two other not-yet-merged items had already cost roughly three hours of idle downstream capacity for exactly this reason, and had even said, out loud, "push it so it can actually be read," while pushing only to a branch rather than getting it merged. The lesson had been freshly stated and was still missed within the same session, because nothing mechanically checked for it.

Root cause: "committed and pushed" felt equivalent to "delivered." For a dispatch, the real artifact isn't the commit — it's the copy sitting on the shared main branch, because that's the only thing a downstream worker is allowed to treat as ground truth. Fix at the source: before writing any dispatch prompt, confirm the item's presence on the current shared main branch with a direct, mechanical check — not a memory of having pushed it.

A second, quieter risk surfaced alongside it: two further items, both drafted directly by the coordinating layer rather than by a worker, still read as open and claimable on the shared branch with no marker of being finished — meaning a worker could, in principle, redo already-completed work against a live client's application. Both were given an explicit do-not-claim marker once noticed. The general shape: a task item with no recorded completion state is a task item that can be done twice.
