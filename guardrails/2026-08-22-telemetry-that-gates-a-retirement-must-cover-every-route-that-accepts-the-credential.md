---
title: Telemetry that gates a retirement decision must instrument every route that accepts the credential being retired
date: 2026-08-22
category: guardrails
tags: [security, observability]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A legacy authentication credential was being phased out under a documented rule: retire it once usage telemetry reads zero. The telemetry counter, however, was only wired into a minority of the routes that actually accepted the legacy credential — the rest silently used it with no instrumentation at all. Following the documented retirement rule as written, based on the partial counter reading zero, would have cut off a pipeline still carrying live production traffic through an uninstrumented route.

General rule: a usage counter that gates a go/no-go decision (retire a credential, remove a fallback, delete a code path) is only trustworthy if it covers every call site that could exercise the thing being measured. Partial instrumentation is worse than no instrumentation for this purpose — it produces a confident, green-looking "safe to proceed" signal precisely in the case where proceeding is unsafe. Before trusting a "reads zero, safe to retire" signal, enumerate every route/queue/caller that accepts the credential and confirm each one is instrumented.
