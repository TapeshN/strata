---
title: Four false verdicts in one verification session were all the same bug — the check could not tell "genuinely absent" from "I failed to observe it"
date: 2026-08-31
category: guardrails
tags: [verification, false-negative, false-positive, positive-control, absent-vs-unobserved]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Verifying a batch of fixes on a live environment in a single session produced four wrong answers from four unrelated checks: two false failures, where a shipped fix was reported as missing, and two false passes, where a fix was reported as verified when it was not. The causes, once traced: searching rendered output for a UI element that only appears after a certain interaction, so its absence from the initial state was reported as a defect; matching a pattern in the exact form the source code used it, against an optimized or rewritten version of that same code actually running in the served environment; measuring an animated element's size while a staggered entrance animation was still growing it, so a mid-animation size read as wrong when the settled size was correct; and looping several network checks into a single text search without confirming each individual check actually completed, so an idle or timed-out call contributed an empty result indistinguishable from a genuine miss.

Every one of these four is the same failure wearing a different coat: the check had no built-in way to distinguish the negative result "the thing is not there" from the negative result "my observation did not actually happen." A silent failure — wrong copy searched, rewritten text, an animation still in flight, a call that never completed — collapses into exactly the same output as a genuine absence.

A verification step should fail loudly when it could not observe, rather than silently reporting a negative: confirm a network or fetch call actually completed before trusting its result, confirm the artifact searched is the one intended and is non-empty, let animations settle before measuring geometry, and pair any "this should be absent" assertion with a positive control proving the same check can find something known to be present. A false failure costs a wasted detour; a false pass ships the bug — that asymmetry is a reason to treat an unexpected pass with at least as much suspicion as an unexpected failure, not less.
