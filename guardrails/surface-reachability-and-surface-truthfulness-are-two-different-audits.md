---
title: "Surface exists and is reachable" and "surface tells the truth" are two different audits
date: 2026-07-22
category: guardrails
tags: [traversal, delivery, definition-of-done, ux]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A live traversal confirmed every expected artifact on a page was present, well-placed, and structurally correct, and that traversal was reported as a clean pass. A follow-up pass asking specifically whether the DATA shown was actually meaningful and current found real problems invisible to the structural check: a status banner confidently claiming nothing needed attention sitting directly above a genuinely unanswered question outstanding for over a week, a confirmation prompt that kept re-asking because it never recognized a valid affirmative answer, and a real, substantive update sitting in an unstructured free-text note while every structured field claiming to capture that same information still read as blank.

**The rule:** a structural traversal (does the surface exist, is it reachable, are all the expected pieces present) and a content/truthfulness audit (does what's shown here actually reflect reality) are two genuinely different checks, and delivery requires BOTH — a clean structural pass says nothing about whether the actual content displayed is accurate, current, or meaningful.
