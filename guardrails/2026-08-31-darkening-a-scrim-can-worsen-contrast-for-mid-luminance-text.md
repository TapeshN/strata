---
title: Darkening a scrim over video or animated media can make text contrast worse, not better, when the text sits at a mid-luminance color
date: 2026-08-31
category: guardrails
tags: [contrast, accessibility, media-overlay, design-verification, measure-dont-eyeball]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A text overlay sitting on top of video content read poorly during the video's brighter moments. The reflexive fix — darken the overlay behind it further — was assumed to help and nearly shipped unmeasured. The text used a mid-luminance color, a standard "muted" tone that was safe everywhere else it appeared on flat backgrounds, while the video behind it swung from near-black to near-white. Because a darkening overlay drags the composited background down through the text's own luminance on its way to black, contrast against a mid-luminance foreground falls to a minimum partway through the darkening range and only partially recovers afterward. Direct measurement across a range of overlay strengths, against the media's actual brightest frame, never reached an acceptable contrast ratio at any single strength, while every increment needlessly darkened content that was meant to stay visible.

Text placed over any variable-luminance background — video, animated gradients, photography — needs to sit at an extreme of the luminance range, near-black or near-white, not at a middle tone that is only safe on flat, controlled backgrounds; a mid-luminance foreground cannot be rescued by scrim strength alone. Before reaching for "darken the overlay" as a fix, compute contrast at several overlay strengths against the media's actual measured peak brightness, sampled from real decoded frames across the whole loop rather than an average or a single screenshot — the worst frame is often nowhere near the frame anyone eyeballs by habit. If the text color sits between the background's bright and dark extremes, no uniform overlay solves it; the fix is to change the text's color or give it a fixed local background, not to keep pushing overlay strength.
