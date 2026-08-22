---
title: Masking/privacy selectors must match what the rendering engine actually traverses, not just the top-level DOM
date: 2026-08-22
category: journal
tags: [security, privacy, tests]
confidence: learned
source: private-work
---

A screen-capture privacy control located elements to mask using a standard DOM query that only walks the light DOM. The rasterization library used to produce the actual capture traverses further than that — into shadow DOM roots and same-origin embedded frames — so any sensitive element rendered inside either of those would be captured and rasterized without ever being matched by the masking selector, an invisible gap between "what my selector finds" and "what actually ends up in the output image."

General rule: when a privacy or redaction control selects elements to hide or mask, verify its selector strategy against the actual rendering/traversal behavior of whatever engine produces the final artifact — a capture library, a PDF renderer, a screen reader — not against the simplest mental model of "the DOM." Any traversal boundary the artifact-producing engine crosses (shadow roots, embedded frames, virtualized/off-screen content) is a place your selector needs to reach too.
