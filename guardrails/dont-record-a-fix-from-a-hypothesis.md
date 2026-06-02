---
title: Don't record a fix-plan from a hypothesis — read the failure log first
date: 2026-06-01
category: guardrails
tags: [verify-dont-trust, ci, context-window, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Resuming after a context compaction to fix a red CI run, the handoff doc carried a confident, prescriptive fix-plan. Reading the actual CI log showed an entirely different root cause: a recursive file-glob threw a permission-denied error on a directory it couldn't read — a directory present only in the CI environment (the library suppressed only not-found errors by default, not permission errors). The plan in the handoff had been written from a *hypothesis* the prior session never checked against the log — and the compaction summary, smoothing the doc forward, stripped the hedging so the guess read as a settled diagnosis.

General lesson: before recording a fix-plan for a CI or test failure, read the actual failure output, not a hypothesis about it. A handoff step must quote the observed error — especially across a compaction boundary, where qualifiers evaporate and a guess hardens into "the diagnosis." On resume, treat any inherited fix-plan as a hypothesis until you've re-grounded it in the live failure.
