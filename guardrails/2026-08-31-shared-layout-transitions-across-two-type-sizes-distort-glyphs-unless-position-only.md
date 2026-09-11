---
title: A shared-layout (FLIP-style) transition between two different type sizes will visibly distort the glyphs unless the transition is position-only
date: 2026-08-31
category: guardrails
tags: [layout-animation, typography, shared-transitions, ui-craft]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A UI transition moved the same logical element between two states that rendered its text at two different font sizes, built with a general-purpose shared-layout ("FLIP"-style) animation feature. Because that feature interpolates the full layout box — including size — it animated the size difference as a scale transform, visibly stretching the letterforms mid-transition and only snapping to correct proportions at the very end. The two ends of what a viewer experiences as one continuous movement also carried two different animation durations, which reads as incoherent even once the scaling artifact is fixed.

Shared-layout/FLIP-style animation across text is only visually smooth when the type's rendered metrics actually match at both ends of the transition. When they can't be made to match, prefer a position-only transition — interpolate position, not size — and accept an instant size change rather than a scaled, distorted one. And any single transition a user perceives as one movement needs one shared duration, not a value defined separately at each end of it.
