---
title: State and handoff operations must use absolute paths, never a cwd-relative one
date: 2026-07-01
category: infra
tags: [worktree, cwd-drift, shadow-state, multi-repo]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A long-running agent session let its shell's current working directory drift over time — after a worktree was removed, the session's cwd ended up one level higher than expected, at the root of a multi-repo workspace instead of inside any single repo's checkout.

A file-queue mechanism (an outbox/inbox pattern used to hand tasks to a background dispatch process) resolved its file paths relative to that drifted cwd. This silently created a second, stray copy of the same directory structure one level up from the real one — invisible unless someone happened to list both trees side by side. Two old, already-handled tasks that lived only in the stray copy then "reappeared" to the session, triggering a false alarm that work was being duplicated, and a routine file-move operation failed with a confusing error because it was operating against the wrong physical location.

The state itself was never actually duplicated or corrupted — the real queue was untouched the whole time. The apparent bug was entirely an artifact of resolving paths against a moving current-working-directory instead of an absolute, known-good root.

The general fix: any operation that reads or writes a durable, cross-session state store (a task queue, a handoff ledger, an inbox/outbox) must resolve its paths absolutely, anchored to a fixed repository root, never relative to the invoking shell's current directory. In a long session, cwd is a moving target — it shifts after directory removals, worktree operations, or simple navigation — and any code trusting it for state resolution can silently start reading or writing the wrong tree. When state appears to "reappear" unexpectedly in an append-only store, the first check should be which physical file is actually being read, before theorizing about a resurrection or corruption mechanism.
