---
title: Cross-repository test dependencies are a structural failure class — every boundary-crossing read ships an env seam
date: 2026-06-11
category: guardrails
tags: [ci, isolation, gating, recurrence]
confidence: learned
source: private-work
---

Three times in 24 hours, a test went green locally and red in CI for the same root cause: code read a file from a *sibling repository* (a persona file, a CLI script, a config registry), and the CI checkout — which only clones the repo under test — didn't have the sibling. One instance is a bug; three in a day is a **class**, and a class gets structural treatment, not three patches.

The structural fix, now standing policy:

- **Every file read whose path crosses a repository boundary ships, in the same change: (1) an environment-variable seam** that overrides the path, **and (2) a test fixture** used as the default in tests. The production default can still point at the sibling; tests never do.
- **Lane/worker prompts carry the rule explicitly** so builders apply it at write time instead of discovering it at CI time.
- **A preflight gate is the recurrence stopper**: grep new code for relative paths that escape the repo root (`../sibling-repo/` shapes) without a corresponding env seam, and fail the candidate before CI ever runs.
- Meta: a recurrence-tracking radar over your learnings ledger should *promote* any tag-class that re-fires within a window from "documented lesson" to "needs a mechanical gate." Documentation didn't stop instances two or three; only the gate ends the class.
