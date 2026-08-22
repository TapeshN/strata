---
title: When a rendered visual pass is blocked, a code walkthrough is a real substitute — and a CSS class name is a shared decision
date: 2026-08-16
category: guardrails
tags: [gating, boundaries]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

With the normal path to visually rendering an app blocked (a browser policy preventing
the tool from reaching certain URLs), per-change code walkthroughs stood in instead —
and one caught a defect that a green type-check and hundreds of passing unit tests could
not: a newly added UI element reused an existing CSS class name, and a pre-existing
responsive rule attached to that class name (written for a different, unrelated element
that had its own phone fallback) silently hid the new element below a certain viewport
width. A pure CSS-cascade interaction, invisible to any test that only exercises logic.

Two generalizable points follow. First, when the rendered-visual verification path is
unavailable, a code walkthrough that explicitly asks "what does this look like on the
default or mobile view" is a legitimate substitute for actually looking at it — don't
merge visual or layout-affecting work on green logic tests alone when the render path is
blocked. Second, reusing another component's CSS class name is not just a styling
shortcut — it inherits every rule already attached to that class, including ones written
for a completely different component and its own constraints. A class name is a shared
decision the same way a shared constant or a shared schema field is; check what else
already depends on a class before attaching a new element to it.
