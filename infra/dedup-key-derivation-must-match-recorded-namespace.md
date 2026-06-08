---
title: A dedup key derived from hand-recorded data must be backfilled, not re-derived, to avoid re-deposits
date: 2026-06-06
category: infra
tags: [idempotency, reproducibility, multi-repo]
confidence: learned
source: private-work
---

When a dedup system derives keys deterministically from source headers, but the original records were hand-abbreviated at first deposit, re-deriving the keys will mark historical entries as new and re-deposit them. The deterministic function produces different keys than the ones the human chose.

The fix: a one-time human-reviewed backfill that pins each historical entry to its hand-recorded key, after which all future writes use the deterministic function and the namespace self-heals. The dedup set is the union of the new deterministic records and the frozen backfill.

General lesson: when a dedup key is derived from data a prior process recorded by hand, diff the deterministic key against the real records first. If they diverge, reconcile with a frozen backfill — never let the re-derivation silently re-emit historical entries.
