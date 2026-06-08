---
title: OIDC and OAuth tests must navigate to the application URL, not the identity provider URL
date: 2026-06-02
category: infra
tags: [determinism, reproducibility, ci]
confidence: learned
source: private-work
---

OIDC and OAuth authorization URLs embed a one-time nonce and state value tied to the browser session that initiated the flow. Reusing a pre-generated authorization URL in a different browser session, or after the nonce expires, causes a correlation failure at the identity provider.

The correct pattern for automated tests: navigate to the application's entry URL and let the application generate fresh nonce and state parameters, then let the OIDC flow redirect to the identity provider with a valid, session-matched URL. Never visit a hardcoded identity-provider URL in a test — it will be stale or session-mismatched.

General lesson: in any OIDC or OAuth flow, the application is the authoritative entry point for generating valid auth parameters. Always test via the application entry URL, not via a captured identity-provider URL.
