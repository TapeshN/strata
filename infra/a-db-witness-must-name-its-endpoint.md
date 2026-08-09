---
title: A DB witness is only a witness if it names its endpoint
date: 2026-08-09
category: infra
tags: [verification, environment-config, database]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

# A DB witness is only a witness if it names its endpoint

A repo accumulated two env files — one maintained by hand, one pulled by a deploy CLI — pointing at **different database branches** of the same project: one live, one empty. Read-only "verify current state" queries silently flip-flopped between them because the query helper read both files, and an early "verified" claim was partly witnessed against the empty branch. A row that existed in production was reported missing until a per-endpoint re-probe.

The rule that came out of it:

- **Every database verification must print WHICH endpoint it ran against** — the host, or `SELECT current_database()` — alongside the result. An unlabeled query result from a repo with multiple env files is not evidence.
- When two env files disagree, **probe both once, record which is live**, and only then trust any state claim.
- Unused per-branch database cruft is not just a cost problem: it **silently absorbs your verification queries** and hands back confident-looking emptiness.

This is the database twin of "a gate run in a stale checkout reports phantom state": the instrument was fine, the substrate it measured was the wrong one, and nothing in the output said so.
