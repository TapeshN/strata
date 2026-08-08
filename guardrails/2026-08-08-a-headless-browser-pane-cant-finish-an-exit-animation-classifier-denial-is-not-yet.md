---
title: A headless browser pane can't always finish an exit animation; a classifier denial is an operator "not yet"
date: 2026-08-08
category: guardrails
tags: [browser-automation, verification, testing, autonomy, permissions]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

An embedded or headless browser pane used for automated UI verification can fail to ever complete certain animation-driven transitions. For example, a "wait for the outgoing element to finish exiting, then mount the incoming one" pattern can hang indefinitely if the pane's compositor cannot drive the exit animation to completion, even though the identical transition works fine in a normal browser. This is not necessarily your change: before concluding a UI component is broken, reproduce the hang against an UNMODIFIED baseline of the code first — if the hang exists on the baseline too, it is an environment limitation, not a regression. Where the component under test has its own reduced-motion or zero-duration code path, prefer temporarily forcing that flag — as a clearly-marked, reverted-before-commit local patch — over hand-patching the automation environment's own animation timers, which frequently do nothing because an animation library captures its own timing source at initialization, before any late patch can intercept it.

Separately: when an automated permission or safety classifier blocks an action — and especially when it blocks the SAME kind of action twice — treat that as an operator saying "not yet," not as a bug to route around. The pattern that works: stop after the second denial, report exactly what was blocked and why it's needed, and let an explicit, later, human instruction re-open the path. Do not invent a workaround or retry with a slightly different phrasing to slip past the same gate — a classifier gate exists precisely to force that pause, and creative retries defeat its purpose even when well-intentioned.
