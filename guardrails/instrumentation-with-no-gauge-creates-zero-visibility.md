---
title: Instrumentation with no gauge creates zero visibility
date: 2026-06-16
category: guardrails
tags: [cost, observability, instrumentation, wired-not-working, done-definition, dashboard]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Building the write path of a metric is not the same as making the metric useful. An instrumentation pipeline whose read path — harvest, surface, display — is permanently deferred to "phase 2" produces zero behavioral signal, even when the underlying data is accurate and complete.

A cost substrate can be fully wired (emit rows on every turn, store them correctly) and yet never influence any decision if no one can read it without running a manual script. The same applies to latency and quality metrics. A meter with no display is a black box: you cannot act on data you cannot see, and you cannot diagnose a spend spike you cannot observe.

The definition of done for any observability feature must include a named, human-readable surface — a dashboard tile, a CLI summary printed on every run, or a stop-hook nudge. An instrument that is neither periodically run nor displayed is indistinguishable from one that was never built.

Corollary: when an audit discovers that "harvest has never been run" despite the emit side being live for weeks, the root cause is always the same — surfacing was classified as a separate deliverable and deprioritized. Treat the emit step and the display step as a single unit of work.
