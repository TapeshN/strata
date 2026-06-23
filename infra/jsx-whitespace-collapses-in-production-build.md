---
title: A space between a closing inline tag and following text collapses in a production build; use an explicit space literal
date: 2026-06-22
category: infra
tags: [determinism, reproducibility, ci]
confidence: learned
source: private-work
---

In a framework that compiles JSX for production, a literal space character between a closing inline element and adjacent text is not preserved. The whitespace collapses, and words from the two adjacent nodes run together in the rendered output.

The fix is to replace every instance of a space-after-closing-tag with an explicit space literal in the markup (`{" "}`). An explicit space literal is guaranteed to produce exactly one space regardless of the build optimizer's whitespace handling.

Before concluding that adjacent text has a missing space, verify the rendered text content directly from the DOM — either by inspecting the element's text content programmatically or by reading the actual rendered characters. A visual screenshot or zoom can be ambiguous: a subtle color transition between two adjacent text nodes can appear to be a gap when no gap exists. Confirming from the DOM text content is unambiguous and prevents "fixing" text that is actually correct.

This class of bug is invisible in development mode (which preserves whitespace more liberally) and only surfaces in the optimized production build. Any rendering gap between words in a production build that does not appear locally should be checked for whitespace collapse before looking for other causes.
