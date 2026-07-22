---
title: A fail-open exception handler can make a gate return a plausible answer from the WRONG source — assert the source, not just the output
date: 2026-07-22
category: guardrails
tags: [gates, fail-open, false-green, verify-dont-trust]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A drift-detection check that's supposed to compare a working copy against its true root fell back, on an internal import failure, to a nearby but WRONG directory — and that wrong directory happened to already be clean, so the check confidently reported "all clear" while the actual root it was supposed to protect held real, unrecorded changes. The gate whose entire purpose was catching exactly this kind of silent loss was itself silently failing via a fail-open exception branch, and no output-only assertion could ever have caught it, because the output looked completely normal — only running the gate through its real, fully-wired invocation path (not a unit test calling the function directly) revealed the wrong root was being used.

**The rule:** for any check whose correctness depends on which underlying resource/path a fallback branch actually used, the test must assert what that fallback ACTUALLY RESOLVED TO, not merely that the function returned a plausible-looking value — a fail-open catch-all can produce output indistinguishable from a correct result while quietly operating on the wrong source entirely.
