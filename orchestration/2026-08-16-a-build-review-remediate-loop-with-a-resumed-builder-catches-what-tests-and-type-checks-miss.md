---
title: A build-review-remediate loop with a RESUMED builder catches what tests and type-checks miss
date: 2026-08-16
category: orchestration
tags: [security, review-loop, subagents]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Across a long stretch of parallel feature work — most of it auth- or money-adjacent — the
following loop was run for every batch before merge: a builder agent ships a change with its own
witnesses, then an independent reviewer agent attacks the change adversarially (re-running gates
itself wherever possible), and on any BLOCK verdict the ORIGINAL builder agent is resumed (its
context and history intact, no re-briefing) with the findings quoted at the exact location they
apply to. The reviewer then re-checks only the delta, and the change merges on a clean pass.

Across six-plus batches, this loop caught several firm high-severity findings pre-merge that a
green type-check and a green test suite had both already passed — a page-level access guard that
was implemented at only one entry point while other reachable pages and API routes stayed
unguarded, an unbounded resource counter that let a concurrent burst blow past its intended cap,
and an identity-correlation scheme where free-text user input turned out to be treated as
authentication rather than as a mere label. Resuming the ORIGINAL builder (rather than dispatching
a fresh one) matters: the fix lands with full context of why the code was written that way, at a
fraction of the cost of re-briefing a new agent from scratch, and fast-follow issues can ride
along as inline review comments so they travel with the code instead of getting lost.
