---
title: Back-compat means satisfying the original assertions, not preserving selectors
date: 2026-06-11
category: evals
tags: [contracts, evals]
confidence: learned
source: private-work
---

A UI refactor "kept backwards compatibility" by retaining a legacy element's test handle — but rendered the element hidden. It passed a DOM-presence check while failing every assertion the original suite actually made: visibility, item count, text content. Keeping the selector is not back-compat; the *original assertions* are the contract, and a compatibility surface must satisfy them as written, not merely exist.

Corollary from the same fix: duplicating a test handle across two components (the old surface and its replacement) trips strict-mode locators, which rightly refuse an ambiguous match. A back-compat root belongs in exactly one place.

The general check: before claiming a refactor is compatible, run the *pre-refactor* test suite against the post-refactor surface unmodified. If you had to edit the assertions to make them pass, the claim is migration, not compatibility — which may be fine, but say so.
