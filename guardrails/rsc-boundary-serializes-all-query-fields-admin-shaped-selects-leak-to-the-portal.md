---
title: React Server Components serialize all query fields across the server-client boundary — a data function shared by an admin and a portal path leaks admin-only fields to the browser
date: 2026-06-29
category: guardrails
tags: [boundaries, isolation, contracts, interfaces]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a framework-level server component data function is shared between an administrative path and a client-facing portal path, every field in its return value — including fields that no rendered component in the portal displays — is serialized into the server-client payload and is readable in browser developer tools. The assumption that "unrendered fields do not cross the boundary" is false for React Server Components.

The failure class is an information disclosure where admin-internal fields (user identifiers, internal timestamps, administrative state flags) silently reach every portal visitor's browser because the database query was written for the admin's needs and the portal component was wired to it without a projection step.

The correct pattern is structural separation: when a data-access function serves both an admin caller and a portal caller, the portal must receive a separately typed projection that omits admin-only fields. The type discipline — using an explicit omit or a dedicated portal return type — enforces the contract at every call site rather than relying on render trees to act as a security boundary.

The audit surface is any data-access function that appears in both an admin route and a client-facing route. Each shared function is a candidate for projection divergence and must be reviewed as a potential information-disclosure path.
