---
title: An independent review of the whole value chain caught a paid-tier gate blocking the free step upstream of it
date: 2026-06-28
category: orchestration
tags: [gating, roles, contracts]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A full session of solo building and happy-path dogfooding on a multi-step product flow missed a gate that had been scoped one step too broad: an authorization check meant to protect a paid stage of the flow was also, as an unintended side effect, blocking the deliberately free stage immediately before it — inverting the intended funnel, since the entry point meant to be open to everyone now failed for anyone who hadn't yet reached the paid stage.

What surfaced it was a structured, adversarial review that deliberately traced the entire value chain end to end from two different lenses — one focused on what a paying or prospective customer actually experiences, one focused on how the system's internal gates are wired — rather than reviewing any single feature or file in isolation. Neither the builder's own tests nor a feature-scoped code review would have caught this, because each passed for the surface it was written to check; only tracing the full sequence of steps revealed that a gate on step N was also blocking step N-1.

The generalizable lesson: for any multi-step flow with a mix of gated and intentionally ungated stages, run an independent, whole-chain trace before declaring the flow correctly wired — a gate protecting a later stage must not silently reach backward and block an earlier stage that was deliberately left open. This class of defect is specifically the kind that surfaces only when someone traces the chain as a user or as a system, not when someone reviews a component.
