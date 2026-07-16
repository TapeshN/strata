---
title: A partial rollout of a fix commonly leaves the highest-traffic caller on the old behavior
date: 2026-07-16
category: guardrails
tags: [fan-out-completeness, partial-rollout, enumerate-callers]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A more robust rate-limiting mechanism was built to replace a per-instance limiter that didn't hold up across multiple running instances, and it was wired into the two call sites where the original bug had been reproduced. Those two call sites were not the busiest ones sharing the same underlying cost-limited resource — a higher-traffic set of call sites hitting the identical resource were left calling the old, per-instance-only limiter, because they weren't part of the original repro and so weren't in scope when the fix was rolled out.

The generalizable pattern: when closing a finding that affects a shared resource or a shared code path, the repro that surfaced the bug is rarely the only caller that shares the vulnerable pattern, and it is very often not the highest-traffic one — the highest-traffic caller is disproportionately likely to be a different code path that happens to share the same underlying dependency. Fixing only the call site in the repro gives a false sense of closure. The rule: before considering a fan-out finding closed, grep every caller of the pattern being fixed (not just the one in the bug report), migrate all of them, and if any are deliberately left out, document that scope explicitly rather than leaving it implicit.
