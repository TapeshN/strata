---
title: A status monitor showing all-zero for a live target can mean "healthy and quiet" or "never actually watching it" — and looks the same either way
date: 2026-09-06
category: guardrails
tags: [observability, absent-vs-unobserved, monitor-design]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A fleet-status command reported zero-of-several containers healthy, no version, no commit — for every one of several separately-running service instances that were, in fact, live and serving successful responses. The cause wasn't drift: the status collector only ever reads local state on the one machine it happens to run on, and none of the target machines had that collector installed on them at all — a second, unrelated design choice, since those machines intentionally carry no full checkout by their own deploy model. Two designs that had never been reconciled left the monitoring tool structurally unable to observe the thing it existed to watch.

The concrete fix came from restating the acceptance criterion: it is not enough that a status command "shows numbers" — a target that was never reachable or instrumented must render distinguishably from a target that is reachable and genuinely quiet, and that distinction has to be provable with a test that deliberately points the collector at an unreachable target and confirms it reports "unknown," not "zero."

A zero from any monitor is two different claims wearing one face: "I looked and found nothing" and "I never looked." A collector that cannot tell these apart will have its silence read as health. It's the same family of failure as a CI job that reports green having executed no steps at all.
