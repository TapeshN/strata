---
title: A grep that returns empty is not proof of absence on files with multi-byte characters
date: 2026-06-17
category: guardrails
tags: [tooling, determinism, evals]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

File-argument grep can silently return no matches on files that contain dense multi-byte or box-drawing characters when the process locale is set to a byte-oriented or unset locale. The search appears to succeed — exit code zero, no error — while producing no output for strings that are plainly in the file. The same content piped through a shell command exhibits the same failure mode.

A witness that can silently return empty is worse than no witness. "grep returned nothing" reads as "the string is absent" when it may mean "grep could not read the file correctly."

When confirming that content exists in a file where encoding may be non-trivial, use a tool that reads the file directly (a file viewer or direct file access) as the authoritative source. Grep is appropriate for filtering large outputs but unreliable as an absence proof on files with encoding complexity.

This is the same class of false-negative as a report-only gate that reads green while broken: the verification step produces a result that appears negative while the actual state is positive. In both cases the correct response is to use a more reliable witness, not to trust the empty result.
