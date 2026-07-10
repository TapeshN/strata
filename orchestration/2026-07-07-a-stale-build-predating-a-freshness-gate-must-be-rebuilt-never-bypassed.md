---
title: A stale build predating a dispatch freshness gate must be rebuilt, never bypassed
date: 2026-07-07
category: orchestration
tags: [orchestration, dispatch, stale-build, dont-skip-the-gate]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A background dispatch system had a deliberate safeguard: before firing off a coding task to a remote agent, it checks whether the locally-compiled build artifacts are older than the source they were built from, and refuses to proceed if so — precisely to prevent a stale compiled dependency (one still missing a recent fix) from silently producing a corrupted or incomplete result, such as a dropped record in a cost ledger. When a session's checkout had been automatically fast-forwarded to a newer source revision at the start of a session, but never rebuilt, that freshness gate correctly refused to run. The tempting shortcut — an environment override that skips the freshness check — would have defeated the exact protection the gate exists to provide. The correct response was simply to rebuild from the repository root and then retry, which then completed successfully and produced a genuine result record.

The general rule: a "refuse to run when stale" gate is protecting a real invariant; satisfy it by actually rebuilding, never by overriding past it. Any checkout that has been automatically advanced to a new source revision (for example, by an automated startup routine) should be treated as needing a fresh build before any operation that consumes compiled output.

A related lesson about proving a dispatch actually worked: the only real evidence that a remote coding-agent dispatch succeeded is an artifact that lands on the target system that the dispatching process itself did not author — a real branch or pull request appearing on the remote host, or a genuine record appearing in a downstream ledger with the expected shape. A dispatch mechanism self-reporting a "completed" or "passed" status is not, by itself, sufficient proof; the witness has to be something independently observable on the receiving end.
