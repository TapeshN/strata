---
title: A read-site filter that relies on a write-time convention is fragile — a nullable enum needs an explicit OR verified against the ORM's generated types
date: 2026-07-10
category: guardrails
tags: [boundaries, isolation, contracts, security]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A new read path filtered a table on a single boolean visibility column, relying on the fact that the only write path in use today happens to also set a companion "audience" column to the value that boolean implies. The pairing — "this boolean and this audience value always travel together" — was never enforced by the schema or a database constraint; it held only by convention at one write site. The safer read-site bound checks the audience column explicitly at query time rather than trusting an incidental correlation created by how the current writer happens to populate the row — a second write path added later is exactly how that kind of assumption breaks silently.

A second, sharper issue surfaced in the same fix: the audience column is a nullable enum, and the ORM's "value is one of a list" operator cannot match a null value on a nullable column, so rows with a null audience were silently excluded from a query that should have included them. The fix required an explicit OR across both states ("equals this value" OR "is null") — and because a careless OR placed next to a tenant- or ownership-scoping key is exactly the kind of change that can silently widen a query instead of narrowing it, the reviewer independently confirmed, by reading the ORM's own generated type definitions, that a top-level OR clause composes as an AND with its sibling scoping keys rather than replacing or loosening them.

Two generalizable rules follow. First, an invariant that holds only because of how one current write path happens to behave should be enforced explicitly at the read site, not assumed to hold forever. Second, whenever an OR clause is introduced anywhere near a tenant- or ownership-scoping filter, verify its composition semantics against the ORM's actual generated types before trusting it — the difference between "ANDs with its siblings" and "replaces the whole condition" is invisible by inspection of the source alone but decisive for whether the change silently breaks isolation.
