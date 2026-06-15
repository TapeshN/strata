---
title: One slow chain idled the whole fleet — waves are per-repo pipelines, not global barriers
date: 2026-06-11
category: orchestration
tags: [throughput, parallel-sessions, dag]
confidence: learned
source: private-work
---

A multi-repo coordinator treated each wave as a global barrier: it waited for every lane in the wave to return before planning the next one. The result, observed by the operator before the coordinator noticed: one long-running chain in a single repo kept running while five other repos sat idle against a ready backlog. Nothing in the written protocol expressed a saturation expectation, so the barrier behavior read as correct.

The fix is a scheduling rule, recorded where the coordinator actually works: waves are per-repo pipelines. Any lane completing triggers a refill check — scan for idle repos against the backlog and dispatch immediately, still honoring single-writer-per-repo. The barrier is only real when a later phase genuinely needs all prior results at once; "the wave isn't finished yet" is not that.

Two structural supports make the rule stick: the expectation lives in the planning doc (so it survives coordinator hand-offs), and a per-repo activity panel makes idleness visible at a glance instead of discoverable by audit.
