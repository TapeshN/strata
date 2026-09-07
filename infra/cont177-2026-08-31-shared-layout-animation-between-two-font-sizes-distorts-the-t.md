---
title: shared-layout animation between two font sizes distorts the type
date: 2026-08-31
category: infra
tags: [framer-motion, layout-animation, typography.]
confidence: learned
source: private-work
---

identical font size on both ends plus `layout="position"` (position-only FLIP, no scale) and one matched duration.

shared-layout/FLIP across text is only smooth when the type metrics match at both ends; if they cannot, use position-only layout and accept an instant size change rather than a scaled one. And a shared transition needs ONE duration, not one per end.
