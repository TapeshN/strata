---
title: Brand/category accent colors fail AA as TEXT on dark; a single-variant a11y scan hides it
date: 2026-06-16
category: infra
tags: [a11y, design-system, theming, wcag, testing-blindspot]
confidence: learned
source: private-work
---

a theme helper exposes both `accent` (decorative) and `accentText` (AA-verified per surface); compute/verify each tint's ratio. Run the a11y scan across EVERY theme variant, not a representative one.

treat "accent as text" as guilty until the contrast ratio is verified on the actual background; never reuse a decorative accent for text without checking.
