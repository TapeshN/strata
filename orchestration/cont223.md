---
title: "I re-reviewed a PR against the wrong baseline and nearly published a false verdict"
date: 2026-09-06
category: orchestration
tags: ["re-review-baseline", "verdict-sha", "false-negative", "coordinator-defect", "client-blocking"]
confidence: learned
source: private-work
---

a re-review's baseline is the head the VERDICT was written at, never the head the monitor most recently announced. The watch reports the newest ready event; it does not know which head a human reasoned about. Every verdict comment already carries its SHA — read it back rather than trusting recall or the notification.

"no code changed since I looked" is a claim about a diff RANGE, and a wrong range makes it confidently wrong in the direction that blocks work. Before asserting a fix is absent, state the two SHAs being compared and check the left one came from the verdict, not the feed.
