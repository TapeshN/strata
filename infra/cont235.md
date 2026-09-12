---
title: "I diagnosed a stale demo three times and was wrong three times, each in a different direction"
date: 2026-09-06
category: infra
tags: ["diagnosis-discipline", "build-host-vs-appliance", "wrong-correction", "read-the-header"]
confidence: learned
source: private-work
---

when a deploy path is unclear, READ THE SHIP SCRIPT'S HEADER before theorising about hosts. And before recording that config is wrong, resolve its paths on every candidate machine — a path that is absent on one host and present on another is a clue about WHICH host it means, not evidence of drift.

three failed diagnoses in one thread is itself the signal — stop generating hypotheses and go read the thing that already documents the answer. Also: a correction entered into a durable doc needs the same evidence bar as the original claim, because a wrong correction is harder to unwind than a wrong claim.
