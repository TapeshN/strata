---
title: An automated geometry check can pass while the human-visible look is wrong, and a screenshot can hide the difference
date: 2026-07-16
category: guardrails
tags: [ui, visual-verification, css, verify-by-traversal]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

When a UI change is checked automatically by comparing element positions and bounding-box overlaps — does this sit where it's supposed to, does it not overlap that — the check can report a clean pass while the actual rendered look, meaning background fill, border, corner rounding, and animation state, is visibly wrong to a human. Overlap and position math is blind to all of these surface properties; a widget can be in exactly the right place, at exactly the right size, and still look broken. This gap is made worse on stacks where taking a screenshot freezes whatever compositor-driven animation is in flight, which can make a genuinely broken animated state look static and "fine" in the captured image, feeding a false read of "nothing looks wrong in the capture, so it must be fine."

Four consecutive review rounds on the same visual element each shipped a build that passed its own geometry-based verification and was then rejected on sight by a human reviewer. The fix was to extend the verification recipe to explicitly assert computed surface properties — background, border, animation state, corner radius — alongside geometry, in addition to document-flow and edge-alignment checks; and, separately, to scope any CSS override introduced to fix one visual state to that specific state rather than to a shared selector, so that fixing one state cannot silently regress a sibling state that shares the same underlying component. General rule: on any stack where a screenshot can misrepresent live animation, treat a live human look — not an automated geometry check and not a static screenshot — as the real verification channel for a visual change.
