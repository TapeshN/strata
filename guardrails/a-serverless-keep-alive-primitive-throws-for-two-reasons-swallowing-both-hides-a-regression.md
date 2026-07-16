---
title: A serverless keep-alive primitive throws for two different reasons — swallowing both hides a real regression
date: 2026-07-16
category: guardrails
tags: [serverless, silent-regression, telemetry, durability]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Serverless platforms offer a primitive for scheduling background work that should keep running after the visible response is sent. That primitive throws in two structurally different situations: a benign one (it is invoked outside of any active request — for example from a test runner or a script, where there is no response to extend) and a genuine one (it is invoked inside a real request, but the hosting platform or a self-hosted adapter never wired up the mechanism that lets work outlive the response). A catch block that swallows both cases identically — logging nothing, or silently falling back to a fire-and-forget call — makes a platform or deployment misconfiguration invisible. The background work silently stops being durable, with zero signal in any monitoring system, which is exactly the failure mode the primitive was adopted to prevent.

The rule: when adopting a "run after the response" primitive, distinguish its two failure classes rather than treating any throw as routine. The benign, no-request-scope case can usually be identified by a distinct error marker the platform attaches to it; anything else that throws from the same call site should be surfaced loudly (an error log, a metric, an alert) so a real platform regression is visible where it happens, not discovered later as an unexplained gap in the data the background work was supposed to produce.
