---
title: A builder agent can outlive its own session/usage window — checkpoint to disk, resume on reset, never retry into the wall
date: 2026-08-17
category: orchestration
tags: [dispatch, durable-execution, cost]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A builder agent died mid-verification when it hit a session or usage-window limit, and the
platform offered an immediate "try again." Retrying right away simply hits the same wall a second
time. What actually survives across that boundary is the agent's committed work on disk (its
worktree commits and transcript) — the work is paused, not lost. The correct response to a
usage-limit death is to set a timer for the stated reset moment and then resume the SAME agent
(with its transcript and worktree intact) once that time passes, rather than retrying immediately
or — worse — dispatching a brand-new agent that abandons the paused one's already-committed
progress. A usage-limit stop is best modeled as an outage-class pause, not a work failure: timed
resume, never blind retry, and never a fresh re-dispatch over a paused-but-intact agent.
