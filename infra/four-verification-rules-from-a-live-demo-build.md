---
title: "Four verification rules from a live demo build: served trees, closed vocabs, env precedence, front-door seeding"
date: 2026-08-09
category: infra
tags: [verification, environment-config, product-ux, typescript, worker-briefs]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

# Four verification rules from a live demo build

Four small, mechanically applicable rules banked from one day of iterating a client demo with parallel build agents.

**1. Never run a production build inside a worktree a dev server is serving.** Build and dev share the framework's build directory; the running dev process starts failing on missing chunk modules and **holds broken in-memory state until killed** — deleting and rebuilding the directory does not heal it. A live demo served errors for a quarter hour because a well-meaning agent ran the build gate in the served tree. Worker briefs for served worktrees must carry an explicit no-build line; the coordinator runs build verification after pausing the server, or in a separate checkout.

**2. Adding a member to a closed string-union passes every gate while partial maps silently misrender it.** Typecheck and the whole test suite stayed green when a new role joined the union — yet one surface labeled the new role with the fallback branch of a partial conditional. Only exhaustive `Record<Vocab, …>` maps get compiler protection. When a closed vocabulary gains a member, grep **every** switch/map over that vocabulary in the same change, and convert partial maps to exhaustive Records so the *next* addition fails typecheck instead of a human's eyes.

**3. A database CLI can follow the env file's secondary connection variable even when the primary is overridden inline.** The throwaway-database pattern ("point the CLI at a scratch DB via an inline env var") silently resolved to a live database because the tool preferred the env file's *direct* connection URL over the overridden *pooled* one. Override the **entire family** of connection variables, and gate CLI write-verbs whenever the effective env resolves to a remote database. Observed twice; treat env-file-beats-inline-override as a standing class, not a one-off.

**4. Populate an experience-review demo through the front door, not the API.** A reviewer asked "what happened to the slider?" because the demo state had been created via direct API calls — the exact UI flow under review was never exercised, so its distinctive controls never appeared in the walkthrough story. When the deliverable is an experience review, seed the walkable state **through the UI flows being reviewed**, or state explicitly which flows the seeded data bypassed.
