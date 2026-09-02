---
title: A "skip if the container runtime is unavailable" CI gate does not distinguish CI from a real operator machine, and an unwired suite quietly accumulates real bugs
date: 2026-09-02
category: infra
tags: [ci, docker, skip-gates, test-harness, ratchet]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

**1. A common CI runner image ships with a container runtime installed and running, so gating a test on "is the container runtime available" does not gate on what was meant.** A test suite meant to run only against an operator's real local runtime — a fixed working directory, live containers already up — was designed to skip itself when a container runtime wasn't present, on the assumption that CI wouldn't have one. The default CI image actually has a working container runtime, so the skip condition never fired there, and the suite attempted to run against infrastructure that doesn't exist in that environment. Confirmed by deliberately breaking the runtime's reachability in CI — pointing its control socket at a dead address, and separately removing its command-line tool from the environment's search path — and observing the suite still attempted to run either way. Rule: a suite that needs a specific operator environment, not merely "a container runtime present," must gate on an operator-specific precondition — a known working directory exists and the runtime actually answers a live query — since the presence of a command-line tool is not evidence of the environment actually needed.

**2. A test suite parked behind an "intentionally not wired into the pipeline yet" marker accumulates real, unnoticed bugs the whole time it sits there.** A configuration-scanning pattern had carried a false-positive rule for months, undetected, because the suite that would have caught it was deliberately excluded from the pipeline while its author waited for a good time to wire it in. Rule: any suite marked as intentionally unwired needs either an expiry date or a review trigger, not an indefinite exemption. The sequence that actually proves the gate works is: make it pass hermetically, wire it into the real pipeline, then delete the exemption — and right before deletion, the newly wired gate should go red at least once against a known-bad case to prove it can actually fire.
