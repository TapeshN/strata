---
title: A memory-summary of an existing system can badly understate what's already built — read the source before any gap analysis
date: 2026-07-21
category: guardrails
tags: [gap-analysis, source-of-truth, competitor-analysis]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A recollection of an existing application's capabilities ("it's basically just a static view plus some in-memory demo data") turned out to significantly understate what the actual, current source already contained — real state-tracked records, a multi-stage pipeline, an approval flow, multiple user roles. A first analysis based on that recollection overstated the real gap; re-doing the analysis from an actual source-level read corrected it to a much narrower, more accurate gap.

**The rule:** for any "what do we have versus what do we need" analysis on an existing system, read the CANONICAL, current source before drawing conclusions — verify you're looking at the actual deployed/current version, not a stale export or an old checkout — rather than reasoning from a summary or a memory of what the system used to contain. A summary is a hypothesis about the system; the source is the fact.
