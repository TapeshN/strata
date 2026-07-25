---
title: A machine projection that re-syncs over a user-editable store makes the edit UI a facade
date: 2026-07-20
category: guardrails
tags: [facade, idempotency, determinism, layering]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A background sync function guarded only against same-request races (it re-read a fresh baseline at the start of its own request and compared against that). That guard is invisible to a slower-moving conflict: a separate, periodic projection process that recomputes a derived record from upstream data and writes it back into the same store a human had just edited by hand. The projection's write silently clobbered the human edit on the very next page load — the UI still showed a "saved" confirmation, but the value reverted the next time the page rendered.

This was only caught because someone drove the real edit surface directly instead of describing the intended change to an agent that would apply it via the backend. A memory- or narration-driven change would never have exercised the specific sequence (edit → background projection run → reload) that exposed the bug.

The general rule: whenever a machine-computed projection and a human edit can write to the same field in the same store, an in-request race guard is not sufficient — the two writers are not racing within one request, they are racing across the record's whole lifetime. The durable fix is per-field provenance: track who (or what process) last wrote each field, and have the projection refuse to overwrite a field a human touched more recently than the projection's own source data changed. Any fix for this class of bug should ship with a regression test that reproduces the exact failing sequence (edit, then a full projection pass, then re-read) and is proven to fail against the unfixed code before it's proven to pass against the fix — otherwise the test may be validating the wrong invariant.
