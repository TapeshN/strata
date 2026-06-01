---
title: Gates that are never run are fiction — a decorative gate manufactures false confidence
date: 2026-05-31
category: guardrails
tags: [gating, ci, verify-dont-trust, release]
confidence: learned
source: private-work
---

Landing a release surfaced two gate illusions at once, in opposite directions. A *false positive*: a release had been treated as "blocked" for a whole session on the strength of a buggy proxy count — nobody had run the real gate, which showed zero matches. A *false negative*: the stated release gate ("build clean") had never actually been run green from a clean checkout — two latent build breaks were masked by stale local artifacts, and no CI ran the build, so many releases had shipped on a gate that was purely decorative.

General lesson: a gate's verdict — pass *or* fail — must never enter your records unless you produced it by running the real gate clean. A gate with no CI behind it is worse than no gate: it manufactures false confidence. Wire the gate into CI so its verdict is mechanical, not on-paper.
