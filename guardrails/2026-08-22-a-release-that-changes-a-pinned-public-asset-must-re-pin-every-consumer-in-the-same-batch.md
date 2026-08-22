---
title: A release that changes a pinned public asset silently breaks every consumer that pins it by subresource integrity — re-pin them in the same batch
date: 2026-08-22
category: guardrails
tags: [release, monitoring]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

An embeddable widget script was updated as part of an unrelated privacy fix. One consuming site had deliberately pinned the widget by a subresource-integrity hash — "if the upstream bytes ever change, fail closed rather than silently load something different." The browser did exactly that: it refused the new bytes, and the widget disappeared from that one client's live surface until a human noticed, while every other, unpinned consumer picked up the new version transparently and was unaffected.

The pin itself was correct behavior. The gap was in the release process: nothing in the release ritual for that shared asset enumerated which consumers pin it and re-pinned them in the same change. A fail-closed integrity control with no paired release step is a self-inflicted outage waiting for the next release.

General rule: whenever a release changes a publicly-served asset that any consumer might pin by hash, the release process must include a step that finds every pinning consumer (grep for the pin/hash reference across all consumer configs) and updates their pin in the same batch — and a runtime health signal should independently compare each consumer's pinned hash against what's actually being served, so drift surfaces even if the release step is missed.
