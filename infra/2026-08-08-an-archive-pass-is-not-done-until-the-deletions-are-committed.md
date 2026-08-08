---
title: An archive pass is not done until the deletions are committed
date: 2026-08-08
category: infra
tags: [git, worktree, cleanup, drift, loss-safe-recovery]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A cleanup or archival operation that moves tracked files — copies them to an archive location, deletes the originals from their working location — is only complete once the deletions are actually committed. Leave the deletions uncommitted and the working checkout becomes permanently "dirty" from version control's perspective, and any refresh or auto-pull tooling that correctly treats a dirty checkout as unsafe to fast-forward — a reasonable, loss-safe default — will keep skipping it, silently, for as long as the dirty state persists. Every subsequent day the checkout falls further behind the remote, and anything reading state from that checkout quietly serves stale information while every automated check reports nothing wrong, because "skip a dirty checkout" is working exactly as designed.

Two fixes close the class: any janitor-style mover must commit-or-restore in the same pass, never leave a half-move; and tooling that silently skips a dirty primary or shared checkout for safety should also emit a loud, recurring warning about it, because a silently-skipped checkout is a silently-stale source of truth for everyone reading from it. Recovery, when it happens, is loss-safe and mechanical: for every working-tree deletion, confirm an archive copy exists; restore the tracked originals from version control (the archive copy still exists in its new location too, so nothing is lost in either direction); then fast-forward.
