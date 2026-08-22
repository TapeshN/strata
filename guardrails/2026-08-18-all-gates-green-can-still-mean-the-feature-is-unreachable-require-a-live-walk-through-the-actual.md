---
title: "All gates green" can still mean the feature is UNREACHABLE — require a live walk through the actual application, not a route probe
date: 2026-08-18
category: guardrails
tags: [verification, false-green, delivery]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A feature passed its type-check, both of its full automated test suites, and continuous
integration — and its underlying business logic was largely correct — yet it shipped with
literally zero user-facing screens: every entry point was API-only, with no in-app trigger for the
end user to actually reach it. In the running application, the intended user could not find or use
any of it. This mirrors an earlier finding from the same builder where a delivered acceptance test
suite could not actually execute — a different shape of the same underlying failure: verification
that never actually touches the running, navigable reality of the app.

The generalizable rule: for any feature meant to be used by an end user (owner, member, or any
other persona), acceptance must include actually reaching that feature through the application's
own in-app navigation AS that persona — not merely probing its underlying routes directly — and
that requirement belongs explicitly in the written brief, not left implicit. The question to ask
of every feature before calling it delivered: "if that persona logged in right now, could they
actually find and use this?" Route-level green does not answer that question.
