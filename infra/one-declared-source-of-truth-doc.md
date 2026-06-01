---
title: Two planning docs with no declared hierarchy will drift
date: 2026-05-30
category: infra
tags: [docs, planning, source-of-truth]
confidence: learned
source: private-work
---

A workspace kept two long-lived planning documents — an older aspirational vision and a newer approved execution plan — with no declared relationship between them. The superseded one was still being edited as if live, and a decision baked into it directly contradicted the approved plan.

The fix: declare an explicit hierarchy at the top of the canonical docs ("X is the source of truth; amend it, never the archived one"), make the approved plan *visible* (not hidden in a tool's private state), and physically move the superseded doc into an `archive/` folder.

General lesson: when two documents can both plausibly answer "what are we doing," readers and agents will edit whichever they opened. Ambiguity about which doc is authoritative is itself a bug — resolve it with a visible banner and one archive move, not with discipline.
