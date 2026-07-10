---
title: Handler-Only Tests Miss Middleware-Level Auth Bugs
date: 2026-07-03
category: guardrails
tags: [testing, middleware, auth, integration-testing, web-frameworks]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Rule: a route-handler unit test that imports and calls a handler function directly bypasses any middleware sitting in front of it in production — so a middleware-level auth or redirect bug can be invisible to the entire test suite and to CI, even while every test is green.

What happened: a machine-to-machine API route was designed to accept a Bearer token (no browser session cookie) and shipped with passing tests. In production, though, the app's middleware layer intercepted every request under that path prefix and issued a redirect to a login page whenever no session cookie was present — running before the route handler's own Bearer-token check ever got a chance to execute. So a legitimate machine caller, presenting only a Bearer token and no cookie, was redirected away and never reached the handler at all. The defect had actually broken an earlier, supposedly "verified" endpoint on the same pattern for its entire existence, because that endpoint's tests were also handler-level: a direct call to the exported handler function, plus a separate test that mocked the HTTP layer entirely. Neither test path ever went through the real middleware, so neither could catch a redirect happening upstream of the handler.

How to apply: for any route meant to be reached by non-browser or non-session callers (service-to-service, webhooks, CLI/API clients), write at least one test that exercises the actual integrated request path — invoke the framework's real middleware/interceptor function against a cookieless or session-less request and assert it does not redirect or short-circuit for that path, while confirming it still behaves correctly for routes that should require a session. A handler-level unit test proves the handler's own logic works; it proves nothing about whether a caller can actually reach that logic.
