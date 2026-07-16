---
title: Recurring per-surface UI drift is a missing shared primitive — fix it once and add a guard test
date: 2026-07-16
category: guardrails
tags: [design-system, shared-primitive, recurrence-gate, consistency]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A single small UI element — a link inviting a user to report a problem — had drifted into several visually different implementations across separate surfaces of the same product: different colors, different presence or absence of an icon, different styling conventions, each one hand-rolled independently by whichever surface needed it. This is the same underlying pattern already known from design-review triage — a repeated finding across many surfaces signals a missing shared primitive one layer down — but observed here from the implementation side: the fix was one shared component, applied everywhere the element was needed, replacing every hand-rolled variant.

The addition that made the fix durable rather than a one-time cleanup was a small automated consistency check wired into the build: a test that fails if any surface reintroduces its own version of the element instead of using the shared component. Without that guard, the same drift reliably recurs the next time a surface is built or redesigned, because nothing stops a future change from hand-rolling the element again. The generalizable rule: when consolidating N independently-drifted implementations of the same UI element into one shared primitive, ship a mechanical test alongside it that fails the build on reintroduction — the consolidation alone fixes the present instances, but only the guard test prevents the pattern from regenerating.
