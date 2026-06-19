---
title: Two green siblings composed red: opt-in behavior change × orphan-test CI wiring
date: 2026-06-11
category: infra
tags: [[emergent-composition], [merge-protocol], [ci-discovery], [recurrence]]
confidence: learned
source: private-work
---

(a) fresh-CI-on-merge-ref is non-negotiable — this class is invisible to per-branch CI by construction; (b) when adding a conditional member to a collection an invariant iterates, declare the condition as a queryable constant beside the collection; (c) wiring orphan tests into CI is itself a behavior change — the wiring lane should run the orphans against ALL open sibling branches in its verify step.
