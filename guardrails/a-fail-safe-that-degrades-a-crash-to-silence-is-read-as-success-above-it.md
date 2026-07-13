---
title: The dominant false-green pattern — a fail-safe degrades a crash to silence, and the layer above reads silence as success
date: 2026-07-12
category: guardrails
tags: [fail-open, gating, ci]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Four independent systems reviewed in one session shared the exact same failure shape despite having nothing else in common. In each case a lower layer had a legitimate-looking safety wrapper — catch an exception and return a default, treat any nonzero exit as "not applicable," collapse an enumerated list of error fields into a summary — and a layer above it treated the resulting default, silence, or summary as evidence that everything was fine. A required health probe that crashed was reported as "skipped, therefore passed." A stale failure flag was left standing because nothing re-checked it once the underlying crash cleared. A scheduler's due-check treated a crashed helper identically to "not due yet" and silently disabled itself forever. A rollup that watched a fixed list of error-field names went blind the moment a new kind of error appeared under a different field name. Each of these shipped with green builds and green tests, and each was caught only by an adversarial pass that deliberately forced the failure condition and watched what the parent layer did with it.

The generalizable rule: any fail-safe, try/except, or degrade-to-default should immediately be checked against one question — what does the layer above do when it receives this degraded value? If the honest answer is "treats it the same as a real success," the fail-safe is a false-green generator. A required check that cannot be verified must be treated as failed or unknown, never as passed; a fail-open branch must fail loudly (log and continue) rather than silently; and any rollup that aggregates sub-results should key off each sub-result's actual verdict, never off an enumerable set of field names that a future change can silently extend past.
