---
title: Port the delta a feature needs, not the machinery around it; a content-hashed asset is a deploy witness
date: 2026-08-08
category: guardrails
tags: [deploy, verification, witness, refactoring, cross-branch-porting]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When porting a feature across two diverged lines of development, read the target line's existing implementation of the same concern before deciding what to bring over. The correct port is often only the thin layer of new logic — a data model, a UI card, the click-handling that connects them — not the surrounding machinery a prior branch built to support it, because the target line frequently already has its own version of that machinery. Porting the whole original implementation would duplicate what already exists, working against the very principle a good port is meant to respect: reuse what the target already has, and add only the delta.

After deploying, the strongest available proof that a specific build is actually live is fetching a content-hashed asset — a filename derived from the file's own content, taken from your local build output — directly from the deployed origin. A success response for that exact filename is a cryptographic-grade witness: it can only exist if that precise code is what's currently serving. This is a stronger check than any visual marker or page title, which can be cached or coincidentally similar across builds. Separately, when the source of a mysterious live deployment is unclear, matching the deploy platform's own recorded creation timestamp against candidate branches' commit timestamps is usually enough to attribute the deploy to its actual source with second-level precision.
