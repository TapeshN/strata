---
title: the coordinator's own primary hijack, and the fleet that flew against a dead server
date: 2026-08-29
category: guardrails
tags: [worktree-protocol, git, gates]
confidence: learned
source: private-work
---

A `cd <primary> && git checkout -b` hijacks the SHARED primary — the worktree protocol binds the coordinator too.

branch work happens in worktrees, period — `git -C <worktree>` forms, never `cd <primary> && checkout`. a worker agent's stop-and-report floor did its job; the boot protocol's "pull would mutate another worker's state = STOP" is validated.

never combine `cd <primary root>` with a state-changing git verb in one command; the primary is read-only from every session's bash.

Never restart a server a browser fleet is flying against.

substrate mutations (server restart, env reload, DB switch) happen BEFORE launching a fleet, never during; fleet prompts get a liveness pre-check of their target.

before any browser fleet: curl the target; while a fleet flies: no config touches.

Audit the PINNED record, not the derived summary.

when auditing "is X recorded", enumerate every rendering of the concept and check the AUTHORITATIVE editable store, not the display cache.

Park the original before overwriting untracked config; check before `cat >`.

gitignored files have NO archive — copy the original line/file to the scratchpad first. For tracked files, `ls`/read before `cat >`; append or Edit unless replacement is the intent.

Claim-by-draft-PR is the cross-harness dedupe seam.
