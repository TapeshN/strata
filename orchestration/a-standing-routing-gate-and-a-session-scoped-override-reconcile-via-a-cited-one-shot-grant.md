---
title: A standing execution-routing guard and a session-scoped operator override reconcile via a cited, one-shot grant — not by relaxing the guard
date: 2026-07-20
category: orchestration
tags: [autonomy, hitl, gating]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A standing rule routes a class of work to one execution path by default (for example: "product-shaped work always goes to an external delegated worker, never handled directly in-session"). Within a single session, the operator gave an explicit, narrower instruction that contradicted the default for that session only ("handle this one directly yourself; reserve the external path for a different, named piece of work").

The clean way to reconcile a standing routing rule with a live, narrower operator instruction is not to weaken or disable the standing rule — that would silently widen the exception to every future session. Instead, record a one-shot grant that quotes the operator's own words verbatim, scoped to exactly the session and task it was given for. The standing gate stays intact and fires normally for every other case; the exception is itself an auditable, ledgered event rather than an invisible deviation.

General rule: when a live instruction conflicts with a standing autonomy/routing floor, the resolution artifact should be a scoped, attributed, one-time grant — not a change to the floor itself. This keeps the gate meaningful (it still fires on the next unrelated case) while still honoring the operator's real-time authority over their own current request.
