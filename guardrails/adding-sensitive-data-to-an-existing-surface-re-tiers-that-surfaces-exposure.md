---
title: Adding sensitive data to an existing surface re-tiers that surface's exposure
date: 2026-07-16
category: guardrails
tags: [boundaries, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A surface that was previously low-stakes — an internal operational dashboard reachable only on a local network, protected by nothing more than obscurity — becomes a real exposure the moment a change adds sensitive content to it (financial figures, personal data, credentials), even when nothing about its network binding, authentication, or caching changed in that same commit. The risk did not move because the surface changed; it moved because what flows through the surface changed.

The generalizable rule: any change that adds money, personal data, or other sensitive content to an already-existing surface must re-audit that surface's whole threat model in the same change — bind address, authentication requirement, cache headers, and who can actually reach it — rather than inheriting the old, lower-stakes threat model by default. That audit belongs in the same change that adds the sensitive data, not a follow-up, because the surface is exposed the moment the data lands, regardless of when the audit eventually happens.
