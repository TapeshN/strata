---
title: A runtime ledger appended inside a worktree is invisible to a gate that reads the primary's canonical copy
date: 2026-07-10
category: guardrails
tags: [worktree, primary-drift, gitignored-ledger, session-boundary]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A control-plane pipeline keeps a small set of append-only runtime ledgers — event logs that later gates and hooks read to reconstruct recent history — and deliberately resolves them from the primary checkout's canonical root rather than from whichever working copy happens to be active, because an earlier incident had shown that a worktree's copy of these ledgers goes stale. A session working inside a worktree appended a completion event to its own local copy of one such ledger. Because that specific file is intentionally excluded from version control (its content is high-volume runtime telemetry, not source to be reviewed), the append could never reach the primary through the normal branch-and-merge path used for tracked files — there is no pull request that could carry an untracked file's contents over. A downstream gate, reading the primary's untouched copy, saw no new event and — correctly, from its own point of view — treated the underlying work as not yet done, blocking a later step on stale evidence for work that had genuinely been completed.

The generalizable rule: a codebase that mixes two kinds of persistent state needs each session to know which write path applies to which kind. Tracked control-plane documents travel via a branch and a pull request, merged into the canonical location over time. Untracked, append-only runtime ledgers that a gate resolves from a fixed canonical root have no such path — they must be appended directly at that canonical location, in the same session that performs the action the ledger exists to record. Conflating the two write paths — treating a gitignored runtime ledger as if it were a trackable document — makes a real, completed action invisible to the exact gate that was built to consume it.
