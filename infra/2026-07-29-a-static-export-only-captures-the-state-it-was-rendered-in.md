---
title: A static export only captures the state it was rendered in — every other branch of conditional content silently disappears
date: 2026-07-29
category: infra
tags: [reproducibility, determinism]
confidence: learned
source: private-work
implementation_target: infra-tooling
efficacy: load-bearing
---

A promotional content section that existed in the source design — gated behind a state toggle — was missing from every rendered output. The tool that converted the dynamic source into static files rendered each page against its default state only; every non-default branch evaluated to empty and was silently dropped, with no error, no warning, and a perfectly well-formed result on the other side.

The failure mode is exactly shaped like success: the output file is valid, any structural test passes, the page renders — the absence is invisible unless you already knew the content should be there. This generalizes to any bake, static-export, or snapshot step over content with conditional branches: it must either enumerate and emit every reachable state, or fail loudly the moment a conditional evaluates to empty, never silently emit nothing. A useful heuristic in retrospect: if a baked or exported artifact is meaningfully smaller than the surface area of its source, something was probably dropped — and an unused grant or permission in surrounding config (an allowance for a feature that turns out to have zero live usages) is itself a smell that content went missing upstream.
