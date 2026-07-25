---
title: A status artifact nothing prunes becomes a liar — derive a work-list by diffing sources of truth, not by reading a cache
date: 2026-07-25
category: guardrails
tags: [stale-status, verify-dont-trust, idempotency, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Any status file, queue, or count that nothing is contractually obligated to prune will eventually describe a world that no longer exists — and it keeps being read as current truth long after it stops being one. In a single work session this pattern surfaced six separate times from different angles: a completion-tracking gate run inside a checkout that was behind its remote reported a large backlog, while the same gate run against the current remote reported none — the entire "backlog" was staleness, not real work; a courtesy queue file listed several items as still pending that an earlier pass had already finished, so following it literally would have re-done completed work; a recurring reminder kept firing off the same unpruned file and could not be satisfied by doing the work, because the file itself was never updated; and a stale documentation/memory pairing led to an unnecessary follow-up question about something that had already been resolved.

The generalizable fix is two-part. First, never trust a queue, pending-list, or cached count as the work-list — always compute the actual gap by diffing the authoritative source (where new work originates) against the authoritative record of what is done (a durable ledger of completed items), and treat any pointer file as a courtesy hint at most, never the source of truth. Second, before trusting any gate's verdict as a fact about the system, confirm the checkout producing that verdict is actually current against its remote — a verdict computed against a stale tree is not wrong reasoning, it is correct reasoning about a world that no longer exists.
