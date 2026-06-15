---
title: A stacked branch carries its parent's pre-fix code — fold mainline before sweeping the child
date: 2026-06-11
category: orchestration
tags: [ci, gating, dag]
confidence: learned
source: private-work
---

A child branch cut from its parent *before* the parent's CI fix landed reproduced the parent's exact red. Stacking copies the parent's tree at fork time; fixes that land on the parent afterwards do not propagate to children already cut. A merge sweep that refuses red branches is correct but cannot self-heal a stale child — it just refuses forever.

The delicate sequence for stacked PRs: the parent merges green first; then the mainline is folded into the child branch (a conflict stops the sweep loudly rather than auto-resolving); only then does the child's own merge sweep arm. When orchestrating with chained workflows, fork a child lane only after the parent's verifier — including any fixes the verifier pushed — has fully completed.

The standing rule: never arm a child's sweep on fork-time state. Sweeps stay refuse-on-red and refuse-on-empty-checks; a repo with no CI merges only on explicit verifier evidence weighed by the coordinator, never by automation.
