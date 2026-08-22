---
title: A live process or a duplicated copy can silently diverge from a just-changed source of truth
date: 2026-08-09
category: infra
tags: [cache, boundaries, contracts, rollback]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two independent incidents on the same day shared one root shape: something already running, or something already duplicated elsewhere, kept serving an answer that used to be correct after the underlying source of truth changed — and the stale answer looked exactly as plausible as a correct one.

First: a running application server had a language runtime that loaded a database-client module into its own process memory at startup and never reloaded it. A schema migration plus a client regeneration on disk did not reach the already-running process — its in-memory client still only knew the old columns. The failure signature was deceptive: hot-reloading of application code kept working perfectly, brand-new routes compiled and served fine, and only routes touching a newly added column failed, with an error message that listed the old, pre-migration set of fields as the "available" ones. It read exactly like a code bug and was actually a stale-process bug; only a full restart of the server process fixed it, not merely clearing a build cache. Whenever a schema change lands under a process that is already serving live traffic, restarting that process has to be an explicit, deliberate step in the change — not an assumption that the next natural restart will happen soon enough.

Second: the same underlying geometry was intentionally duplicated in two places — a build-time registry and a runtime database table, kept in sync only by a seed step. An update to the registry rendered correctly wherever the registry was read directly, but a second consumer read the same geometry from the database instead, which the change hadn't touched. The result was a surface that displayed new, correct-looking content sitting on old, now-wrong positions — worse than an obvious break because every individual piece still looked plausible. It was caught only by deliberately measuring the two copies against each other, rather than trusting that the surface "looked right." The generalizable rule: whenever a source of truth is duplicated into a second store for read performance or for a different consumer, changing the source has to include re-syncing every duplicate as part of the same change, and every consumer of that data needs to be enumerated so it is clear which copy each one actually reads.
