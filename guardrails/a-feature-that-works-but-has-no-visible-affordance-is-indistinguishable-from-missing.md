---
title: A feature that works but has no visible affordance is indistinguishable from a missing feature
date: 2026-07-22
category: guardrails
tags: [ux, discoverability, wired-not-working]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A UI control was fully implemented and functioned correctly end to end — the underlying component was rendered, wired to real state, and behaved as designed when exercised directly. Despite this, a real user reported the feature as simply not working, because the only way to discover and operate it was through an unstyled, unlabeled interactive element with no visual cue that it existed, that it responded to interaction, or that it supported the range of behavior it actually had (in this case, a resize interaction that only worked from one edge, in one direction, on one class of device, through a plain button with no grip or handle indicator).

This is a variant of "wired but not working," moved from the code layer to the UX layer: verifying that a feature's logic is correct and reachable through direct interaction is not the same claim as verifying that an ordinary user can discover it exists at all. A completeness review of user-facing work should therefore include an explicit discoverability pass — can an unbriefed user find this control, understand it is interactive, and infer roughly what it does — as a distinct check from "does the handler fire when triggered." Shipping the underlying mechanism without shipping a visible affordance for it should be treated as shipping half the feature, because from the user's side of the interaction, an undiscoverable feature and an absent one produce the identical experience.
