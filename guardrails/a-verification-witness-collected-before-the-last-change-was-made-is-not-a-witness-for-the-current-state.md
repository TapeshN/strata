---
title: A verification witness collected before the last change was made is not a witness for the current state, and an exit code without its message is not a verdict
date: 2026-07-02
category: guardrails
tags: [verify-dont-trust, ci, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A pre-stop safety check blocked progress with "no witness for what was actually changed." It initially felt like a false alarm — a relevant test's output was visibly present earlier in the session. Re-running the full witness set anyway surfaced two real problems: a type-check that had genuinely started failing because of a file written after the last time that check was run (only a different, narrower check had been re-run since), and a status that had been reported as a soft warning but was actually a file-not-found error from a tool that no longer existed at the expected path on a stale checkout — an exit code was being read as a graded verdict without ever looking at what it actually printed.

Two generalizable lessons. First: a verification witness is only valid for the state that existed when it ran — any mutation made after collecting it invalidates it, and the correct discipline is re-running the full relevant witness set after the LAST change, not after the last convenient one. Second: an exit code alone is not a verdict — the same non-zero code can mean "the check ran and failed" or "the check could not even start" (missing binary, wrong path, wrong environment), and treating both identically as a graded failure can hide a much simpler infrastructure problem. Always capture and read the actual output alongside any exit code before drawing a conclusion from it.
