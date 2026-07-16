---
title: When a design review finds the same class of issue on many surfaces, root-cause it to a missing design-system primitive and fix it once
date: 2026-07-16
category: orchestration
tags: [design-system, review-triage, root-cause]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A structured design review that walks a product surface by surface, using a fixed set of review lenses, can trace what looks like a scattered list of independent high-severity findings back to a small handful of missing pieces at the design-system layer — for example, the absence of semantic state-color tokens (so surfaces reach for raw utility colors with no dark-mode variant), no defined spacing scale, or missing shared primitives for common controls, each of which then gets reinvented slightly differently on every surface that needs it.

When a review turns up the same shape of finding repeatedly across surfaces, the efficient response is to rank the resulting punch list by "fix once in the shared token or primitive layer" ahead of any per-surface patch. A token-layer or primitive-layer fix collapses many per-surface findings into one change, while patching each surface independently both costs more total effort and leaves the surfaces inconsistent with each other afterward. General rule: treat a repeated review finding as a signal to look one layer down for a missing shared primitive before treating each occurrence as its own isolated bug.
