---
title: Gate rejections are telemetry — instrument the rejection stream rather than discarding it
date: 2026-06-14
category: guardrails
tags: [evals, dedup, gate-holds, signal, telemetry, learning-loop]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When a deduplication or near-duplicate gate rejects a submission because a substantially similar entry already exists, that rejection is not a failure — it is a signal. An observation that the system keeps re-deriving independently is a high-confidence, load-bearing principle. The rejection event reveals which principles are being hit repeatedly, which is more useful than the submissions themselves.

The naive response to a dedup-gate rejection is to discard it. The productive response is to record it: which principle did this trigger against? How many times has it been triggered? A ledger of rejection events, indexed by the principle they matched, produces a ranked list of the most-reinforced ideas in the corpus. That ranking is the highest-priority signal for which principles deserve promotion, elaboration, or mechanical enforcement.

The same applies to any gate that holds or rejects rather than approves: a capability-check that rejects a "resume this WIP" request because the capability already shipped on a different branch is signaling that the triage step is blind to a class of state. Instrument the rejection to surface that blind spot rather than treating the rejected work as simply wrong.

When building a dedup or hold gate: emit a structured record for every hold event. Include the candidate identifier, the existing entry it matched, and the match confidence. This record is the input to a recurrence analysis — the tool that converts the gate's negative outputs into positive learning signal.
