---
title: A per-event draft generator needs a per-recipient digest, or the recipient's inbox becomes the deduplication layer
date: 2026-08-22
category: guardrails
tags: [comms, read-models]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A generator produced one AI-drafted communication for every reply event on a shared feedback thread. On a single day, roughly thirty owner replies produced roughly thirty near-identical drafts, several naming a page label that an unrelated bug had invented and that a later reconciliation pass had already removed. None were sent, and the intended recipient was never actually told anything meaningful had happened.

The fix consolidates this into one digest per recipient per day, regenerated from current, reconciled state (not a snapshot taken at the moment of the original event) and superseding any stale earlier draft for the same period automatically.

General rule: any generator that emits one artifact per upstream event, rather than one artifact per downstream recipient per period, will flood the recipient with near-duplicates the moment event volume rises — and any generator drawing on mutable upstream state (labels, ids, statuses) must regenerate from current state at send time, not from a stale snapshot taken when the triggering event fired. Build the recipient-grain rollup up front; don't let the human's inbox become the deduplication and staleness filter.
