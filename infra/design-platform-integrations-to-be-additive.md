---
title: Design deliverables so platform integrations are additive, not reconstructive
date: 2026-06-02
category: infra
tags: [layering, interfaces, contracts]
confidence: learned
source: private-work
---

When building a client deliverable that will later integrate with a platform, design the deliverable's output shape to match what the platform would generate or consume from day one. Then the integration becomes additive — plug in the platform, it generates what already fits — rather than reconstructive, where the deliverable must be rebuilt to fit.

Under deadline pressure, ship the client deliverable first. The integration demo later becomes "take the shipped deliverable and show the platform generating its layer on top" — a stronger story than an incomplete combined build.

General lesson: check whether the platform's output shape matches the proposed directory or data structure at design time, not at integration time. Align them before starting; the integration is then a drop-in, not a rebuild.
