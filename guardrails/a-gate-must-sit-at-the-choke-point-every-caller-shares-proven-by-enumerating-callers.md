---
title: A behavior gate must sit at the choke-point every caller shares — proven by enumerating callers, not by testing the one you noticed
date: 2026-07-14
category: guardrails
tags: [choke-point, gate-coverage, caller-enumeration, security-review, autonomy]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A safety/entitlement gate was first placed inside the handler for the caller the author had in mind — the interactive, user-facing path. A second caller existed that invoked the same underlying action directly, through a more automated route, and it bypassed the gate entirely, because the gate lived one layer too shallow: in a caller, not in the shared function all callers pass through. The gap surfaced only when a reviewer enumerated every caller of the guarded action's core function, rather than re-testing just the caller under review.

The fix was to move the gate inside the single shared function every present and future caller passes through — the actual choke point — placed before the sensitive step, with an explicit override flag reserved for the one sanctioned bypass (an admin-style action).

The general rule: for any new gate on an action, first grep every caller of that action's underlying function and confirm the gate sits at the point where all of them converge. A gate placed at one caller is a facade for every caller you didn't check — and the more automated or autonomous a path is, the more likely it is to be the one that reaches the guarded function through a shortcut nobody thought to gate.
