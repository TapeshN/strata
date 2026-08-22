---
title: A security gate's runtime-mode discriminant should be a build-time artifact property, not a process-mode check
date: 2026-08-22
category: guardrails
tags: [docker, security, cost, demo-infra]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A set of demo applications ran a memory-heavy development server around the clock, solely because an internal "no credential required" door was gated on the process not being in production mode. The gate's logic was sound — an explicit opt-in AND not-production — but the "not-production" half was expressed as a live runtime property, so the only way to keep the door open for demo walkthroughs was to run the most expensive server mode available.

The fix moved the discriminant into the built artifact itself: a build-time constant baked into every server and client bundle at compile time, checked alongside the production flag. A real production build never carries the demo marker, so the original security invariant is unchanged — a mis-set runtime environment variable still opens nothing — but the app can now run its cheapest, most efficient server mode in the demo-serving container. Memory usage per instance dropped by roughly an order of magnitude, witnessed live.

The general lesson: when a gate's second factor is "what mode is this process in," ask what that mode costs to sustain at the scale you actually run it. A build-time constant embedded in the artifact can provide the identical tamper-resistance as a runtime environment check, for a fraction of the resource cost — and it removes the temptation to loosen the gate later just to make the cheaper runtime available.
