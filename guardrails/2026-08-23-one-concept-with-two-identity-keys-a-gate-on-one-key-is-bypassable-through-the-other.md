---
title: One concept with two identity keys — a gate that checks one key is bypassable through the other
date: 2026-08-23
category: guardrails
tags: [identity, gate-design, boundaries, security]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A new machine subsystem reused an existing table as the carrier for its own work items rather than adding one. The administrative surface built on top gated every user-visible write on a single structural column being set — the column the subsystem's own producer always populated. But the subsystem's wire contract identified the very same work by a DIFFERENT field: a free-text topic string supplied by the caller.

A reviewer created an ordinary record carrying that topic through a caller-facing tool where the string was model-steerable, then watched the queue deduplicate onto it, a machine worker claim it, and the completion publish machine-generated analysis into an end user's notification feed — with the gate present, in place, and reading green the whole time. Two prior remediation rounds had hardened the sinks without ever seeing the second key.

The root cause is twin identity: one concept rendered by two keys with nothing keeping them in agreement. Every gate that checks one key is bypassable through the other, and that bypass is invisible to a reviewer who only knows about the key the gate names.

The fix has three parts, and fewer than three leaves a hole. Reserve the wire vocabulary at the PRODUCING chokepoint so a caller-supplied value from the subsystem's namespace is refused outright. Bind every deduplication and lookup read to the structural column so nothing merges onto a foreign row. And make the gate require BOTH keys, so rows that predate the gate cannot satisfy it by accident.

Prevention is a design-time question, not a review-time one. When a new subsystem reuses an existing store as a carrier, ask on day one: by which column does EACH consumer identify "mine"? If the answers differ, that IS the finding — before any gate is written. Review briefs for shared-carrier work should name this check explicitly, because a reviewer reading only the gate's own key will confirm the gate and miss the door beside it.
