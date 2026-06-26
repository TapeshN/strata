---
title: Dispatching to a new product repository requires a registry entry before the first dispatch
date: 2026-06-23
category: orchestration
tags: [dispatch, registry, new-product, dispatch-quality, onboarding]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

An orchestration layer that gates dispatch on a registered entity will refuse to dispatch any work to a product repository that has not been registered — even if the credentials, repository URL, and task brief are fully formed. The gate is correct: unregistered products have no declared autonomy level, concurrency limit, or model policy, so the dispatcher has no way to enforce the operating constraints that make the dispatch safe.

The fix is to create the registry entry before the first dispatch, not as a prerequisite discovered at failure time. For each new product, the one-time registration step must include: the product identifier, the repository reference, the maximum parallel lanes, the autonomy level, the model policy, and whether agent dispatch is enabled. Once registered, all subsequent dispatches for that product reuse the entry without modification.

This is a one-time cost that pays for itself immediately: the dispatch pipeline stays consistent (all work routed through the same orchestration layer, subject to the same policies), the concurrency cap is respected, and the learning capture that depends on routing through the dispatcher is never bypassed.

The practical checklist: before scheduling the first dispatch to any new repository or product, confirm the registry entry exists and is active. A dispatch attempt that fails with a "not found" or "entity not registered" error is not a tooling bug — it is the gate performing its function.
