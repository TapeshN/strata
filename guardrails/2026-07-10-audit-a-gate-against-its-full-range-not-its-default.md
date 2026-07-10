---
title: Audit a safety gate against its full intended range, not its shipped default value
date: 2026-07-10
category: guardrails
tags: [safety-gates, entitlements, race-conditions, code-review, configuration-drift]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A gate that checks a cap or entitlement against a hardcoded default can be technically correct today while hiding a broken invariant that only activates once that value becomes configurable. When you reason about whether a limit is "safe," you have to evaluate it against the full range the field is designed to support — not the single value currently shipped.

**What happened:** An engineering team had a capability-consuming feature gated by an atomic database check (an "update rows where used count is less than the allowed limit" pattern) that correctly prevented double-spending a one-time grant. At the shipped default (limit of exactly one), the atomic compare-and-update genuinely closes the race: two concurrent requests can't both succeed. But the schema's own documentation noted that the limit was intended to become operator-adjustable in the future — a per-client override lever, not a fixed constant. Nobody had re-examined whether the same check still held once that limit could be greater than one. A careful review caught this and flagged it as worth fixing now, even though it wasn't exploitable yet, rather than dismissing it as "not a real bug because it isn't reachable today."

**How to apply:** When you review or write a safety gate — a rate limiter, an entitlement check, a quota, a permission threshold — identify every place its bound is declared to be adjustable (a config field, an admin lever, a documented "future: make this configurable" comment) and re-derive the gate's correctness using the *maximum* value that lever could ever take, not the value it happens to hold in production right now. "Safe at N=1" is not the same claim as "safe for all N," and code that conflates the two will pass every test today and fail silently the day someone turns the dial. Treat "this will become configurable" as a design requirement to satisfy immediately, before the config surface ships — the fix is cheaper before the invariant is load-bearing in production.
