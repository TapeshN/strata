---
title: A deposited-state check that only replays its own ledger cannot detect its own gaps, and a read-only diagnostic must never write the liveness signal a separate monitor reads
date: 2026-08-31
category: infra
tags: [observability, source-of-truth, self-perpetuating-alarm, ledger-drift]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

An automated pipeline that publishes internal notes to a public archive raised an alarm that several notes had gone undeposited for more than two days. Investigation found three separate, independently plausible faults stacked on top of each other. First, the alarm itself was false: the flagged notes were already published; only the pipeline's own local ledger record of that publication had never been written, so the engine kept recomputing the same already-completed work as missing, rebuilding an identical branch that produced zero new commits, every run, forever. The pipeline's dedup logic trusted its own ledger as the sole source of truth and never checked the actual destination it was supposed to be publishing to. Second, the tool's own designed repair path for exactly this kind of gap turned out to depend on reading the very ledger field that had gone missing in the first place, so it could not self-heal the case it existed for. Third, a separate and unrelated scheduling fault meant the pipeline genuinely had not run in days — fixing only the false alarm would still have left real work undone.

The most surprising piece: the read-only diagnostic command used to investigate the alarm itself writes a "still alive, ran successfully" timestamp row to the same ledger that a separate liveness watchdog reads. Simply running the diagnostic to check on the stalled pipeline flipped the watchdog from "stalled" to "healthy, ran moments ago" — masking the real scheduling fault from anyone who checked liveness afterward.

General rules: (1) a deposited or published-state check that only replays a local ledger cannot, by construction, detect the case where the ledger itself is wrong — it needs some way to verify against the actual destination system, at least as a fallback. (2) A repair tool built for a missing-ledger-field bug that itself depends on reading that same field cannot repair the case it exists for. (3) A read-only diagnostic must never write to any ledger, timestamp, or counter that a separate monitor treats as a liveness or health signal — running a check should never be able to make a broken system look healthy.
