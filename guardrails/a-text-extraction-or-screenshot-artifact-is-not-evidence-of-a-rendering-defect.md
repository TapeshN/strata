---
title: A serialized-text extraction or a screenshot is not, by itself, evidence of a rendering defect
date: 2026-07-22
category: guardrails
tags: [verify-dont-trust, false-positive, browser-audit]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Twice in one review session, a tooling artifact read convincingly as a severe product bug. A text-extraction tool emitted a UI's speaker/attribution labels in a different order than they visually render, making correctly-attributed content look completely inverted when read as plain text — a specific rendering defect that a screenshot immediately showed wasn't real. Separately, a dropdown appeared visually clipped off-screen in a screenshot; measuring the element's actual on-screen position showed it was comfortably inside the viewport — the screenshot itself had been cropped, not the menu misplaced. Both would have been filed as confident, specific, and wrong.

**The rule:** text extraction can reorder content relative to how it visually renders, and a screenshot can be cropped or otherwise fail to represent the true viewport — neither is, by itself, the rendered truth. Before filing a defect based on either, measure the actual DOM/element geometry or look at genuinely full, unmodified pixels.
