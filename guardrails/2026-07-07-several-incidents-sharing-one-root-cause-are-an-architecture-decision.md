---
title: Several incidents sharing one root cause are an architecture decision waiting to be written, not another bug report
date: 2026-07-07
category: guardrails
tags: [architecture-decision, root-cause-consolidation, fail-open, data-classification]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Across one extended work session, more than a dozen separately-logged incidents — a stale lock file, a drifted ledger, an orphaned background task, a status indicator with no real producer feeding it, a timezone miscalculation — turned out, once someone stepped back and looked at them together, to reduce to a single underlying architectural choice: important runtime state was being kept in flat files under version control and reconciled by hand, rather than in a proper shared data store with its own invariants. Filing each new occurrence as its own isolated bug fix treats a structural decision as a string of unrelated incidents.

The general rule: when adding a new "we hit this again" entry to a learnings log, check whether it shares a root cause with entries already on record. Once roughly three or more incidents trace to the same underlying design choice, stop filing them as individual bugs and instead write the fix as an explicit architectural decision — the real fix is choosing a different foundation, not patching the tenth symptom.

A related, separately-discovered lesson from the same session: when a system has two different code paths that both handle the same sensitive category of data, but each path defaults to a different failure posture (one defaults to a safe/local-only behavior, the other defaults to a less-safe/external behavior unless an environment variable happens to override it), that divergence is itself a latent privacy failure waiting for an environment misconfiguration to trigger it. The fix is to make the classification of "how sensitive is this data" happen in exactly one place — a single, mandatory routing decision that every caller must go through, with the safe behavior as the only reachable default for that data category — rather than trusting every individual call site to independently choose the safe path.
