---
title: Keep structured-output fields plain prose, and mine the transcript before re-running a dead agent
date: 2026-07-19
category: agents
tags: [structured-output, agents, reliability, context-window]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A long-running diagnostic agent died at its structured-output retry limit because one of its own field values embedded markup-like characters that the output parser choked on repeatedly. The full diagnosis wasn't lost, though — it was recovered from the agent's own failed tool-call payloads in the transcript and fed forward into the resumed run as a precomputed stage, at zero re-diagnosis cost.

Two rules follow. First, any prompt asking a model to emit structured fields should require plain, bounded, markup-free prose in every field — angle brackets, backticks, and other parser-meaningful characters inside a field value are a self-inflicted failure mode. Second, treat a structured-output death as a FORMATTING failure until proven otherwise: before re-running an agent that died this way, mine its transcript for the attempted (but rejected) payloads — the work is usually already there, just unparsed.
