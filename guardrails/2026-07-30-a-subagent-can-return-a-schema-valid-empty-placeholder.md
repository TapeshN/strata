---
title: A subagent can return a schema-valid, empty placeholder — passing validation is not evidence any real work happened
date: 2026-07-30
category: guardrails
tags: [subagents, evals]
confidence: learned
source: private-work
implementation_target: agent-guardrails
efficacy: load-bearing
---

In a fan-out of parallel reconnaissance sub-tasks, one produced a response that perfectly matched the expected JSON schema — correct keys, correct types, a plausible-looking finding — while every field inside it was a literal placeholder value. It passed schema validation, the harness reported it as completed with zero errors, and it would have been silently folded into downstream work as an equally-weighted input alongside genuine results.

The structural gap: a validation layer checks shape (does the output match the schema) and a harness checks completion (did the process exit without error); neither can see that the content itself is a self-test stub with no real information in it. A completion count of zero errors is a liveness signal — it says the process ran — and is never, on its own, a quality signal. The cheap, generalizable mitigation: after any structured fan-out, spot-check each payload for content plausibility before consuming it — does a cited file path actually exist, does a quoted snippet actually appear in the file it claims to come from. A payload that fails that check should be treated as no result at all, not partial credit.
