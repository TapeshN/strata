---
title: A fail-closed local dev-login switch lets an agent traverse an auth-gated app without ever typing a password
date: 2026-06-28
category: guardrails
tags: [hitl, autonomy, gating]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

An agent operating under a standing floor that forbids it from ever typing a credential into a login form cannot directly exercise an authenticated, entered experience of an auth-gated application — yet verifying that experience end to end is exactly the kind of review that catches defects invisible to a green test suite. Requiring a human to sit alongside the agent and manually switch between accounts defeats the point of having the agent do the traversal.

The pattern that resolves this without weakening the floor: stand up a disposable local environment — its own database, a fictional (never real) set of seed identities — with a dev-only, fail-closed sign-in switch. The switch is gated by an explicit enable flag that is only ever set outside production, signs the requested identity in server-side using a seed credential the agent never sees or types, and is unreachable (404s) whenever the production flag is set. The agent then moves between roles or accounts by visiting one URL per identity, with no credential ever entering its context.

The gotcha worth naming: many applications' request-routing middleware intercepts API and page routes before the route handler itself runs, and will redirect an unauthenticated request straight to the login page — including a brand-new dev-only route, unless that exact route is added to the middleware's own allowlist. A route that looks correctly implemented can still be silently unreachable because the layer above it never lets the request through. The general lesson: giving an agent safe, credential-free access to an authenticated surface is a structural problem to design for, not a policy to work around case by case, and any new route added for this purpose must be checked against every layer that runs before it, not just its own handler.
