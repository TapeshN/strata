---
title: An unset keep-alive on a model-residency serving path is an accidental latency bug, and generic latency percentiles hide it
date: 2026-07-11
category: infra
tags: [latency, cost, cache]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A locally-hosted model server that unloads an idle model after a default timeout will silently reintroduce a multi-second reload cost on the next request unless something in the serving path explicitly overrides that default — and if no layer in the chain (the proxy, nor either caller) ever sets a keep-alive/TTL value, the platform's out-of-the-box default quietly governs a decision nobody actually made. Measured directly: a cold reload added several seconds of load time versus a small fraction of a second when the model was already resident — almost the entire user-visible latency spike traced to that one unset setting.

The instrumentation gap that let this ship unnoticed matters as much as the bug itself: request-rate, error-rate, and general latency dashboards were all genuinely wired — collecting and displaying real data — but none of them asked the one question that would have caught this: "is the model still resident right now, or am I about to eat a cold reload?" A generic latency percentile actively hides this class of bug, because it blends fast warm requests and slow cold ones into one middle number instead of showing the bimodal split. The witness that actually catches it is a direct residency check (is the model currently loaded, and if so until when) taken immediately before a request, kept as a distinct signal rather than folded into an aggregate.

The generalizable rule: any serving path with a model-residency or similarly expensive lazy-load cost needs an explicit, deliberate keep-alive/TTL decision made at design time — an unset default is not a decision, it's an unnoticed accident waiting for someone to hit it live — and its dashboard needs a residency-specific witness, not just aggregate latency, or the gap will look invisible until demonstrated live.
