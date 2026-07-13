---
title: A control-plane "halt everything" switch is a facade unless every autonomous queue is gated at its own route
date: 2026-07-12
category: guardrails
tags: [autonomy, gating, fail-open]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A kill-switch that is supposed to stop every autonomous or cloud-model-calling process is only as complete as the set of routes it was wired into. A system had three lanes gated behind a halt flag — a generation queue, a research endpoint, and an intake path — but a fourth queue that also made a paid remote-model call had its own bearer-token check and no reference to the halt flag at all. Flipping the master switch off did nothing to that fourth lane: the remote consumer kept polling and spending while the control panel reported every lane as closed. An automated build-and-verify pass over the change passed, because it only checked the lanes it had been told about; an adversarial review that swept for every remote-claim / cloud-model-call site found the gap.

The generalizable rule: enforce a halt at the server-side route, never at the remote consumer's discretion — a consumer that is merely asked nicely to stop is the exact fail-open condition the halt exists to prevent. Any lane that makes a paid or remote-model call should check the same master flag every other lane checks, not just its own topical toggle. And whenever a new halt or kill-switch is introduced, the closing step is a sweep: enumerate every bearer-token/claim route and every remote-model-call trigger and confirm each one is wired to the same flag, not just the ones remembered when the switch was designed.
