---
title: Decorative accent colors require a separate contrast-safe text variant — and a11y scans must cover every theme permutation
date: 2026-06-16
category: guardrails
tags: [evals, determinism, golden-sets, gating, preflight]
confidence: learned
source: private-work
---

A saturated brand or category accent color that works well as a decorative element — a border, background chip, or icon tint — will often fail WCAG AA contrast requirements the moment it is used as foreground text on a dark surface. The failure is not obvious by eye: the color feels bold and visible, but the luminance ratio against a near-black background can sit well below the 4.5:1 threshold required for normal-weight text. This was observed directly when a category-theming pass reused a decorative accent as text color, producing a contrast ratio of roughly 3.5:1 — a clear violation that was invisible during design review.

The compounding risk is in test coverage. An automated accessibility scan that exercises only one theme variant — one representative category or lab — can pass cleanly while every other variant carries the identical latent violation. The scan does not prove the system is accessible; it proves that one permutation is accessible.

Two rules follow from this:

First, any design-token or theme system that exposes an accent must expose two distinct roles: a decorative accent (unrestricted, used for non-text elements) and a text-safe accent (verified to meet the required contrast ratio against each surface it will appear on). These must be computed and checked independently, because the decorative value cannot be inferred to be text-safe.

Second, accessibility gating must enumerate and scan every theme permutation, not a representative sample. The number of permutations is bounded and usually small; there is no valid reason to skip variants. A scan-all policy converts the a11y gate from a spot-check into an actual invariant. Treat any accent applied as text as a contrast violation by default until the ratio is verified on the specific background it will render against.
