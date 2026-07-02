---
title: A screenshot's pixel dimensions are not the same coordinate space as the page's CSS pixels, and clicking screenshot coordinates directly can silently miss
date: 2026-07-02
category: guardrails
tags: [ci, verify-dont-trust]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

During a browser-driven traversal, several precise-looking clicks on a visible, clearly-labeled button did nothing, while other native browser behaviors (like input focus) kept working normally — a pattern that at first looked like a page-wide rendering or hydration failure. Direct inspection from inside the page confirmed the page was healthy and the element was genuinely clickable; the actual fault was that the screenshot used to compute click coordinates was rendered at a different pixel density than the page's own logical CSS pixel width, so every coordinate derived from the screenshot landed measurably off-target.

The diagnostic tell worth remembering: when native browser behaviors keep working but every coordinate-driven interaction fails, suspect the coordinates, not the page — a genuinely broken page tends to fail more uniformly, not selectively by interaction type.

The fix, and the durable rule: before relying on screenshot-derived click coordinates, compare the screenshot's pixel width against the page's actual logical viewport width. If they differ (which they will on any display with a non-1.0 pixel density), either scale every coordinate by the ratio, or better, drive the interaction semantically — through element references or DOM-level selection — rather than raw pixel coordinates.
