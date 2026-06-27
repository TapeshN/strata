---
title: A standalone API-request fixture in a browser test does not share the page's cookie jar; use the page's own request context
date: 2026-06-22
category: mcp
tags: [determinism, reproducibility, evals]
confidence: learned
source: private-work
---

When a browser test issues an API call using a standalone request fixture (a separate API context independent of the browser page), response cookies land in that fixture's own jar and never reach the page's browser context. Any subsequent page navigation that depends on those cookies — a session cookie, an authentication cookie, a state cookie — will behave as if the API call never happened.

The symptom: the API call succeeds (correct status, correct response body), but the page's subsequent behavior shows no state change. A banner that should disappear stays up. An authenticated route remains inaccessible. The implementation is correct; the test is using the wrong context.

The fix is to issue the API call through the page's own request context rather than the standalone fixture. The page's request context shares the browser page's cookie jar, so cookies set by the response are immediately visible to subsequent page navigations.

This is a test-authoring error, not an application error. The underlying implementation may be entirely correct while the test produces a false failure because it simulates the HTTP path without simulating the browser context that the application relies on.
