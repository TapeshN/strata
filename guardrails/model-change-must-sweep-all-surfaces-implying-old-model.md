---
title: A pricing or access-model change must grep every surface that implies the old model; a partial fix reads as a contradiction
date: 2026-06-22
category: guardrails
tags: [multi-repo, docs, release, ci]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

When a feature's access model changes — who can use it, what tier unlocks it, how it is presented to different user classes — the change propagates to more places than the code that enforces it. Marketing copy, label text, subtext strings, legend descriptions, and pricing tables can all imply the old model while the enforcement logic reflects the new one.

A user who reads the marketing text and the in-product experience back to back encounters a contradiction. The contradiction is as visible and damaging as a broken feature.

The discipline: after any pricing, gating, or access-model change, grep the full repository for the old framing before calling the change done. Old framing typically appears as: strings containing the old tier name, label text that implies the old restriction, subtext that references the superseded rule. The grep is cheap; the remediation pass is a few targeted string replacements. Missing it is expensive because it ships a user-facing contradiction into production.

A static audit of the changed files will miss this class of defect. The only reliable check is a live traverse of the actual user experience — reading what a real user would read, in the order they would read it — combined with a broad text search for the now-incorrect framing.
