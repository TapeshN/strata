---
title: Route at the producer, not the consumer — a triage-only downstream step signals an upstream gap
date: 2026-06-02
category: orchestration
tags: [dag, layering, contracts, interfaces]
confidence: learned
source: private-work
---

A pipeline step that must decide how to route its input based on that input's content is a sign that the routing decision was not made upstream. If a downstream reviewer or triage step exists only because the upstream producer did not classify its output, fix the producer: add a routing label to the schema and instruct the producer to populate it at write time. The consumer's job then becomes mechanical rather than interpretive, and the separate review pass is no longer needed for well-labeled entries.

The naming signals the problem: a step called "review" that is really "triage" reveals that the upstream didn't finish its work. The correct pipeline is distill → classify → route → act; inserting a consumer-side triage pass is a workaround for an incomplete producer.

General lesson: when designing a feedback loop, routing labels belong at the source. If a downstream step must infer routing from content, add the label field to the schema and move the routing logic upstream.
