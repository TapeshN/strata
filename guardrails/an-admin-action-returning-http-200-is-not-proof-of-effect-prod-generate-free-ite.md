---
title: an admin action returning HTTP 200 is not proof of effect: prod "Generate free iteration" enqueued nothing
date: 2026-07-19
category: guardrails
tags: [witness-dont-assert, enqueue-vs-execute, prod, gate-blocked, generation-lane, no-guess-retry]
confidence: learned
source: private-work
---

witness the effect (counter/row/event), not the 200 (extends "witness don't assert" to the enqueue class). When a mutating UI action returns success but state doesn't move, check the network response first (rule out client error), then the queue/consumer health — don't re-click. A "Generate" that enqueues to a dead lane should surface a lane-health warning, not a silent 200 (product gap → candidate for the generation-lane-health surface).
