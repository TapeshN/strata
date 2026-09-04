---
title: A global capture-phase "first gesture" listener can silently fight the very control the user pressed
date: 2026-08-31
category: guardrails
tags: [event-capture, race-condition, ui-affordance, autoplay]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A media player used a common pattern to work around blocked autoplay-with-sound: arm a one-time, document-level pointerdown listener in the capture phase that unmutes the player on the user's first gesture anywhere on the page. A user reported that the player's own explicit mute/unmute button had stopped working. The button's own logic was correct in isolation, toggling state and its label properly on every click. The actual defect: when the user's first gesture on the page IS a press of the mute button itself, the capture-phase listener fires first — capture phase always wins the race against a target's own bubble-phase handler — unmutes the player as a side effect of "first gesture," and then the button's own click handler toggles FROM the state the listener just silently set, landing back where it started.

The fix: both listeners now check whether the event target is inside an interactive control before acting, and only remove themselves once they have genuinely fired on a non-control gesture.

General rule: any document-level "first gesture" or one-shot listener that reacts to any user interaction must explicitly exempt interactive controls, or it will race — and silently fight — whichever control the user reaches for first. A capture-phase listener specifically guarantees it wins that race, which makes the bug both invisible when the control is tested in isolation and highly visible to a real user reaching for it as their first action on the page.
