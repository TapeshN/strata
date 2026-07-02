---
title: A flag named for safety (dry-run, check, plan) is not actually safe unless every metered or side-effecting code path it touches is verified to also be inert
date: 2026-07-02
category: guardrails
tags: [cost, autonomy, gating]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A tool's default mode — including its "dry-run" flag — was found to bootstrap a real paid API credential from a nearby configuration file and invoke a full agentic pipeline through a metered API, even though the flag's name strongly implied a side-effect-free preview. A separate environment variable existed to skip the agentic portion, but the flag most people would reach for first ("dry-run") did not activate it. The write half of the operation was indeed suppressed; the spend half was not.

This is a recurring class: a flag or command whose name implies inertness (dry-run, check, plan, help) but whose implementation still exercises a paid or otherwise side-effecting path unless a second, non-obvious opt-in is also set. The appearance of safety and the actual behavior diverge, and nothing forces them to be checked against each other.

The fix is twofold: (1) any flag or mode named for safety must be provably side-effect-free by default — if it can't be made so, it should be renamed to stop implying a guarantee it doesn't keep; (2) before invoking an unfamiliar tool's "safe-sounding" mode for the first time, especially one wired to a paid credential, verify what it actually does (read the source, or test with a deliberately invalid credential and confirm no live connection is attempted) rather than trusting the name.
