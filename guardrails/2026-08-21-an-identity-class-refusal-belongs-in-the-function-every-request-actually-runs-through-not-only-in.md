---
title: An identity-class refusal belongs in the function every request actually runs through, not only in the entry door or the session-refresh path
date: 2026-08-21
category: guardrails
tags: [security, tenancy, authorization]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A rule stating that a certain class of account should never hold an independent session was
enforced at the login entry point and again during periodic session refresh — but the ONE function
that loads the acting identity on every single incoming request never applied the same restriction,
because that function is called far more often than the refresh path runs. An adversarial
re-review minted a session for that restricted account class directly in a test harness and
successfully performed a privileged action with it. The gap was not reachable through the
production login flow, but the code comment describing the restriction called it "absolute" while
the enforcement was, in practice, only two-thirds complete.

The generalizable rule: an identity-class restriction (a certain kind of account should never act
as though it were a different kind) must be enforced in the function that runs on EVERY request —
not only at the door where a session begins, or in a periodic refresh path that runs far less
often. The same class of gap applies to any parent-scoped relation exposed through a shared,
tenant-scoped resource: a query scoped correctly to one tenant does not automatically scope every
relation it includes or selects — each related lookup needs its own explicit scope check.
