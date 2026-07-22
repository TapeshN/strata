---
title: A cloud platform's account-level subdomain registration can be a separate, one-time step from a per-resource URL toggle
date: 2026-07-19
category: infra
tags: [deployment, cloud-platforms, gotchas]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Deploying a resource (a serverless function, a worker, a small app) to a shared cloud platform's default subdomain can silently depend on an account-wide registration step that is entirely separate from the per-resource "make this publicly reachable" toggle. Enabling the resource-level toggle does not register the account-wide subdomain; without it, the URL resolves to a broken placeholder host, and the platform's own CLI-printed onboarding link can point at a stale path in a dashboard that has since moved the setting elsewhere.

**The rule:** when a resource on a shared-subdomain cloud platform won't resolve after deployment, check for an account-level one-time registration step before assuming the deploy itself failed — and because that registration is account-wide and effectively permanent, treat setting it as a decision for whoever owns the account, not something to click through on their behalf. Once registered, a redeploy resolves the URL immediately.
