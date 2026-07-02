---
title: Building internal training/fixture apps to harden an organization is not a slogan — it surfaced a live production defect and left behind a permanent gate
date: 2026-07-02
category: journal
tags: evals, gating, security, golden-sets
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

An organization built a second internal training/fixture application (deliberately seeded with intentional bugs, used for evaluation and QA-skill practice) as part of an ongoing series of such apps. Building it — not auditing an existing system, just constructing the new fixture and reviewing it the way any real feature gets reviewed — surfaced a live defect in an already-shipped, already-in-production sibling application: an answer-key-equivalent payload was being served into the client-side JavaScript bundle, readable by anyone who inspected the build output. No existing test had caught it; a security reviewer building and grepping the build artifacts of the new app is what found the pattern, then went and checked the sibling and found it already live.

The fix was not just patched into the one file — it became a permanent build-artifact scanning gate that runs on every future app in the series, and every fixture app built after it shipped verified clean under that gate.

The generalizable claim: deliberately building disposable-seeming internal training or fixture applications is a legitimate hardening mechanism for an organization's real, production-facing systems, not merely a training-content exercise. The construction process itself — because it forces the same architecture, patterns, and review discipline as production work, on a lower-stakes surface — surfaces defect classes that existing production tests had missed, and each such catch is an opportunity to leave behind a structural gate rather than a one-off fix. Treat "build another training/fixture app" as a standing hardening activity, not overhead separate from the org's real reliability work.
