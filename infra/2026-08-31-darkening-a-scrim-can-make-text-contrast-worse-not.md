---
title: Darkening a scrim can make text contrast WORSE, not better: the background sweeps through the text's own luminance
date: 2026-08-31
category: infra
tags: [contrast, accessibility, video-overlay, design-verification, measure-dont-eyeball.]
confidence: learned
source: private-work
---

text over variable-luminance media must sit at an EXTREME of the luminance range, not the middle. The site's mid-grey small-print token is safe only on flat ground; over media it is unfixable by scrim strength.

before reaching for "darken the overlay", compute contrast at several alphas against the media's MEASURED peak luminance, not its average and not a screenshot's vibe. If the text colour lies between the background's bright and dark extremes, no uniform overlay solves it — change the text colour or give it local ground. Sample the real decoded frames across the whole loop: this clip's worst frame was at 5.5s of 7s, nowhere near the poster or the first frame anyone eyeballs.
