---
title: Probe a credential's capability at boot rather than diagnosing it two gates downstream, and tell the human when a bounded approval window opens
date: 2026-09-05
category: guardrails
tags: [hitl, autonomy, gating, preflight, determinism]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A multi-agent dispatch pipeline reported the same class of failure on every attempt for over two weeks. Reconstructing it by hand revealed not one bug but a chain of four independent gates, each of which only became visible once the gate before it was satisfied: an expired credential the dispatcher depended on, which surfaced two layers downstream as an unrelated-sounding resolution error rather than as an authentication failure; a hard cap on how much inline decision context a human-approval channel would accept, which refused any request that exceeded it rather than truncating; a required piece of routing configuration that was simply unset in the environment actually running the pipeline; and a bounded wait for a human decision that expired by its default because nobody had been told it had opened.

None of the four was itself a bug — each was a guard doing exactly its job. The compounding failure was diagnostic: the error surfaced at each stage named only the symptom of THAT stage, never the fact that more gates stood behind it once it was fixed, so weeks of identically-worded failures all read as one problem instead of four sequential ones.

Rules distilled from reconstructing it: (a) any credential a pipeline depends on should be probed at boot with a direct, minimal capability check — "can this identity actually perform its narrowest required action right now" — and reported by name as a credential failure, never left to surface downstream under an unrelated symptom, which sends diagnosis in the wrong direction for as long as the chain is long; (b) when a task needs to carry non-trivial decision context through a channel with a hard size limit, hand that channel a reference to a committed artifact the recipient can open, not inlined prose that risks tripping the cap; (c) a bounded human-approval window is only a real control if the human is actively told the window has opened and how long it lasts — a decision silently queued and left to expire is functionally identical to an automatic denial; (d) when a lane fails with the same signature for an unusually long time, run it by hand once and read every message end to end — a long-lived stable failure signature usually names the FIRST gate in an unexamined chain, not the only gate.

Addendum from the same investigation: the approval-window duration turned out to be a plain configurable value, and the approval mechanism re-attaches to a decision already made for a given task rather than re-asking — so a pending approval survives a restart of the component that issued it. Practical implication: widen the window to human-presence scale for an unattended run (hours, not minutes) rather than assuming a short default is fixed, and design the approval store so a decision, once made, is honored even if the requesting process restarts before it is consumed.
