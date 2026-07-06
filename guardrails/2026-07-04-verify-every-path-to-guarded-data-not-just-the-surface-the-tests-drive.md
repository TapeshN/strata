---
title: An access-control fix verified airtight at the surface can still leave the layer behind it wide open — verify every path to the same data, not just the one the tests exercise
date: 2026-07-04
category: guardrails
tags: [owasp-a01, double-verification, api-behind-the-guard]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

An authorization fix centralized a guard on a page route and was verified thoroughly — both the builder and a first independent reviewer confirmed the guard held in both directions across a full end-to-end test pass. A second, independent security-focused reviewer asked a different question: what enforces the same restriction on the API route that actually serves the underlying data behind that page? It turned out nothing did — the API endpoint had zero ownership check of its own, so a request that bypassed the page entirely (a direct call) could retrieve the exact same restricted data the page guard was supposed to protect.

The general failure mode: a guard gets verified at the one surface the test suite exercises, while a sibling path to the identical data — an API route, a server-rendered payload, a second UI entry point — shares none of that verification and can be missed even by a careful, well-tested fix, because "the tests are green" only proves the tested surface is sound.

The generalizable review discipline: for any access-controlled resource, enumerate every path that can reach the same data — the page, the API route(s) behind it, any server-rendered payload that might carry more than it displays — and verify authorization independently at each one, not just the path the UI/end-to-end tests happen to drive. This is exactly why a security-focused independent review earns its cost beyond ordinary code review: a second reviewer with a different mental model asks "what else reaches this data" rather than re-confirming the one path already under test.
