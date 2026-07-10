---
title: Cross-surface UI parity requires diffing computed geometry, not source values
date: 2026-06-29
category: guardrails
tags: [ui, brand-parity, css, verify-by-traversal]
confidence: learned
source: private-work
---

Polishing a shared visual element (a logo/wordmark) across two different pages of the same product surfaced three subtle bugs that a successful build or a passing test suite would never catch — each one only visible by actually looking at the rendered page.

First, a logo that visually "shifts" or looks different in size between two pages is rarely a font-size mismatch. The real culprit is usually the surrounding header geometry: header height (a taller header vertically centers the wordmark differently), line-height (a default browser value differs meaningfully from an explicitly-set value of one), padding, and even a text-rendering/antialiasing setting, which can make identical text look measurably lighter or thinner on one page than another at the same nominal font weight. The fix is to measure both instances' actual rendered bounding boxes at the same viewport size and match every one of these properties, not just the pixel font size.

Second, a translucent/frosted navigation bar (a background with partial opacity plus a blur effect) reads as intentional when it sits over a rich, colorful background, but reads as an odd, washed-out "pale strip" when the same styling sits over a flat, plain background. The fix is to make the header fully solid whenever its backdrop is flat, and reserve the frosted treatment for backgrounds with enough visual texture to justify it.

Third, driving an element's on-screen position with a CSS transition while ALSO updating that same property every animation frame from a separate script creates a permanent tug-of-war: each new frame sets a new transition target before the previous transition ever finishes easing toward it, so the element appears to lag or freeze, only "catching up" once the per-frame updates stop. The fix is to pick exactly one mechanism — drive the property from a single per-frame animation loop that eases a current value toward a target value itself (rather than layering a CSS transition underneath it), and to use an absolute, ever-increasing clock (not a timer that resets to zero) for any idle/ambient motion, so the animation does not visibly snap back to a "home" position whenever the user's input stops.

The general prevention: for cross-surface visual parity, diff the actual computed/rendered geometry of a shared element on both surfaces, not just the source values used to build it — and never mix a CSS-driven transition with a JavaScript-driven per-frame animation on the same property.
