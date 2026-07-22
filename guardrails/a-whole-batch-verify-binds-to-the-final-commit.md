---
title: A whole-batch verify binds to the FINAL commit, not the commit it ran on
date: 2026-07-19
category: guardrails
tags: [ci, verify-dont-trust, release, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A full-suite verification pass ran clean across an entire batch of changes. A follow-up commit then landed afterward — a security-hardening pass adding a new, more aggressive data-deleting call — and only the batch's own narrow specs were re-run against it, not the full gate suite. The structural safety guard that would have caught the new call first fired in CI, not locally, because the "verify once on the whole batch" step had already been marked done before that commit existed.

**The rule:** a batch's verification is only valid for the commit it actually ran against. Any commit added after the verify pass — even a small, well-intentioned one — reopens the batch and requires a full gate-suite re-run, not just the touched files' own tests. Treat "verified" as a claim about a specific commit, not about a batch's intent.
