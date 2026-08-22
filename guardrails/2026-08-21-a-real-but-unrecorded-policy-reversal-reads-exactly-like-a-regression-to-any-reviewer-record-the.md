---
title: A real but unrecorded policy reversal reads exactly like a regression to any reviewer — record the authorization where the guardrail itself lives
date: 2026-08-21
category: guardrails
tags: [governance, security, false-green]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A change re-introduced a category of data that an earlier, deliberate decision had removed, and in
the SAME change also narrowed the automated test that had been specifically written to forbid that
category of data from reappearing. An adversarial review correctly flagged this as a blocking
finding — "a guardrail test narrowed alongside the exact change it exists to forbid" is
indistinguishable from an attempt to quietly reverse a settled decision. It later turned out the
reversal genuinely was authorized — but that authorization existed only inside an unrecorded prior
conversation, nowhere near the code or the test itself.

The generalizable rule: a guardrail test that pins a policy decision should carry its own policy
history directly alongside it — what the original ruling was, when, who re-authorized any reversal,
and a pointer to wherever that decision is durably recorded — and a durable decision log should
carry the matching entry. A policy reversal is only valid when the artifact that PINS the policy
itself cites the reauthorization; absent that, a narrowed guardrail test is treated as a regression
by default, never inferred as an intentional change from the fact that a suite still passes.
Reviewers should diff the TEST before the code on any change touching a policy-pinning suite, since
a passing suite over a reversed ruling is exactly what a false-green looks like.
