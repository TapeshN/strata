---
title: IDs generated from a time window need a uniqueness guard, not just a readable format
date: 2026-06-11
category: infra
tags: [determinism, idempotency, contracts]
confidence: learned
source: private-work
---

Two records opened in the same second, for two scopes whose names shared a long common prefix, received the identical generated id. The generator combined a second-granularity timestamp with a *truncated* slug of the scope name — truncation collapsed the discriminating suffix of the two names into the same string — and there was no collision check, so both records were written under one identity. The defect surfaced in live use roughly thirty minutes after the feature merged with a fully green test suite.

The class: any id scheme that combines a coarse time bucket with a potentially shared prefix is susceptible to same-window collisions. The property worth testing is **uniqueness under collision**, not "the id looks right." Drive two generations in the same time window with near-identical inputs and assert the ids differ; separately, give the writer a guard that probes the ledger for an existing id and appends a counter until the slot is free.

Truncation was the root cause and the missing guard was the amplifier. Removing the truncation fixes the observed instance; the uniqueness guard closes the entire class. Generated-id schemes deserve a property-style collision test from day one.
