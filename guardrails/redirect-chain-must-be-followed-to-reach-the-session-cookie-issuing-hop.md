---
title: Follow every redirect to the hop that issues the session cookie, not just the first response
date: 2026-06-25
category: guardrails
tags: [determinism, reproducibility, ci, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

In any redirect-based authentication flow (OIDC, SSO, SAML, or any multi-hop login chain), the session cookie is issued on a later redirect hop, not on the first POST or callback response. The first response typically sets only a correlation or nonce cookie; the actual session is established when the application completes the final exchange hop.

A test harness that stops at the first redirect, or that uses a non-follow-redirect mode, never completes the exchange. The cookie check at that point will always fail because the session was never issued.

A real browser auto-follows the full chain. This means manual login succeeds while the automated harness reports "not authenticated," and the asymmetry is easy to misread as an application-side problem. The true cause is the harness stopping one redirect short of the issuing hop.

The diagnostic signal: manual login works; the automated harness fails on the session cookie check. This pattern means the harness is not following a redirect the browser does. Trace the full hop chain, identify which hop issues the session cookie, follow all redirects to that hop, then assert.

A verdict of "not a test bug, it is an application-side issue" on an auth failure must be reproduced without the harness before it is accepted. If the issue cannot be demonstrated outside the harness, the harness is the problem.
