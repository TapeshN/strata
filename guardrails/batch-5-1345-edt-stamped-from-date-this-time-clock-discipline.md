---
title: Always stamp time-of-day from the system clock, never from session narrative
date: 2026-06-10
category: guardrails
tags: [determinism, hitl, docs, gating]
confidence: learned
source: private-work
---

A recurring failure mode in long agentic sessions is that the agent narrates time-of-day from accumulated session momentum rather than from an actual clock query. A session that began in the morning and ran for several hours will start writing phrases like 'end of day,' 'this evening,' or 'tonight' into coordination documents — handoffs, run-state files, scheduling notes — even when the real wall-clock time is early afternoon. This is not a one-off error; it compounds silently until a human reader or downstream scheduler acts on the wrong temporal framing.

A second, related hazard: timestamps emitted by version-control systems and CI pipelines are UTC. If an agent reads a commit or merge timestamp without converting to the local timezone, a mid-afternoon event at UTC−4 will visually appear as 'late evening' (e.g., 17:37 Z reads as 5:37 pm UTC, which looks like end-of-business even though local time is 1:37 pm). Forgetting the offset compounds the narrative drift.

The practical cost is real: handoff documents that claim end-of-day at 1 pm cause the next reader or scheduler to treat the remaining half-day of runway as already consumed. Inboxes staged 'for tomorrow morning' may wake agents or humans half a day late.

The fix is structural, not attentional. Any agent writing a time-of-day claim to a coordination document must derive that claim from an explicit clock read in the same turn — not from how long the session has felt. Trailing-Z timestamps must be treated as UTC and converted before narrating. Framing this as a guardrail rather than a style suggestion is important: the documents that carry these timestamps are scheduling inputs, and scheduling inputs need deterministic provenance.
