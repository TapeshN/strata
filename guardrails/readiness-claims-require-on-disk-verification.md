---
title: Readiness claims require on-disk verification, not in-context belief
date: 2026-06-06
category: guardrails
tags: [verify-dont-trust, gating, lifecycle]
confidence: learned
source: private-work
---

Asserting that a system is ready to run based on in-context belief — "I made the edits, so it should be ready" — produces a false-green that wastes a run or causes a bad outcome. The execution path reads files from disk; the relevant checkout may be behind the version where the required configuration changes landed.

In a concrete case, a system was asserted ready because the edits had been made in the session. The actual primary checkout was ten commits behind those edits — it had none of the session's work. The run would have executed a pre-session plan.

Prevention: "ready" is a claim that requires verification. Check that the HEAD of the actual execution path (the checkout the run reads) matches the version that contains the required changes. When an operator challenges a confidence claim, treat it as a cue to verify, not to restate the belief.
