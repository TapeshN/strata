---
title: A self-written verifier reporting failure is more likely your bug than the system's
date: 2026-06-16
category: guardrails
tags: [verify-the-witness, self-written-tool, coordinator-not-exempt, rule-15]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When a verification script you just wrote reports that the system is broken, the most probable explanation is that the script is wrong — not the system. This is the inverse of the usual wired-not-working trap (where a gate exists but silently does nothing); here the gate is active and loudly wrong.

Two failure modes combine: first, the author applies rule-15 ("verify, don't claim") to workers but suspends it for their own tooling, treating a freshly written audit script as authoritative. Second, the verifier-has-its-own-bug trap — a script that reads from the wrong data key, uses the wrong endpoint, or makes a faulty assumption about format will produce a confidently wrong result.

The pattern has a recognizable signature: the "broken" verdict is surprising, the system was working before the script was written, and manual inspection of the system suggests it is actually correct. In that situation, re-examine the verifier first. Check which key it reads, which endpoint it calls, and whether the data shape it expects matches reality. Confirm against the canonical source before believing the failure report.

Corollary: the coordinator is not exempt from their own gating rules. A changelog requirement that was documented after being tripped by a builder still applies to the coordinator's own subsequent operations. The knowledge that a rule exists — and that one wrote it — does not grant immunity from it. Document, then obey.
