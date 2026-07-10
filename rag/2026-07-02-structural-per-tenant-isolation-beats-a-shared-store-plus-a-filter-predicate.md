---
title: Structural per-tenant isolation beats a shared store plus a filter predicate, and the way to prove it is to falsify it
date: 2026-07-02
category: rag
tags: [rag, isolation, boundaries]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A proof-of-concept for isolating one client's retrieval data from another's was built as a genuinely separate index or store per client, rather than as one shared index filtered by a client-identifier condition at query time. This is a meaningfully stronger design: a shared-store-plus-filter approach depends on every single query remembering to apply the filter correctly, forever, across every code path that will ever touch that store — one missed or malformed filter is a cross-client data leak. A structurally separate store per tenant makes that entire class of leak impossible by construction, because there is no shared index for a missing filter to leak from.

The isolation claim was verified not by inspecting the code, but by falsification: the review deliberately mutated the design back to a single shared store with a filter, ran the existing test suite against that mutated version, and confirmed that a large fraction of the tests then failed — proving the original tests were actually sensitive to the isolation property, not just passing coincidentally.

The generalizable pattern for any multi-tenant retrieval or data-isolation design: prefer structural separation (separate store, separate index, separate namespace per tenant) over a shared resource plus an access-scoping filter wherever the cost allows it, and whenever a test suite is meant to prove isolation, validate it by deliberately breaking the isolation and confirming the suite catches it. On the transport layer, the tenant or client identifier that scopes any query must always be derived from a trusted, server-side session — never accepted as a field the caller supplies.
