---
title: A post-deploy grep returning zero can be a false negative from mid-propagation, not a failed deploy
date: 2026-07-21
category: guardrails
tags: [deploy-witness, verify-dont-trust, ci]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Immediately after triggering a deploy, grepping the freshly-deployed asset for expected new content returned zero matches — which reads exactly like "the deploy failed." It hadn't: the fetch had raced a not-yet-propagated or momentarily-missing asset path, so the "zero matches" was actually zero bytes of the RIGHT content fetched, not proof the right content wasn't there. Re-fetching a moment later with the HTTP status and byte size printed alongside the grep showed a normal success response with the expected content.

**The rule:** never trust a bare match COUNT from a post-deploy check as a verdict by itself. Always print the fetch's HTTP status code and downloaded byte size alongside any grep count, so "zero matches" and "zero bytes fetched because the request itself didn't succeed yet" can't be confused with each other.
