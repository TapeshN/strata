---
title: A single-item lookup is the highest-risk sibling of a scoped list query
date: 2026-07-07
category: guardrails
tags: [security, idor, byok, distribution-boundary, ip-boundary]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a feature exposes both a filtered LIST of records (correctly scoped to the current tenant/owner) and a single-record GETTER reached by a direct identifier or slug, the single-item getter is actually the higher-risk surface: an attacker never has to go through the list UI to reach it, they can guess or enumerate the identifier directly. Any scoping predicate enforced on the list query (tenant, audience, ownership) must be enforced INSIDE the single-item query's own lookup as well — not assumed to be redundant because "the list already filters it." A related, generalizable check: whenever a role- or tier-based gate branches which records a query is allowed to return, confirm the branching condition is derived from the server-verified session on every call site, not passed in as a parameter that some future caller could set incorrectly — trace it back to the actual authorization check, don't stop at a function's type signature.

A separate but related lesson concerns any software that ships with a "bring your own credentials" model, where every user supplies their own API key or account and the software itself never spends money on their behalf. Auditing that model for fund safety (no hidden credential, no ability to silently drain a user's account) is necessary but not sufficient for a piece of software meant to be publicly redistributed. The same shipped artifact can still leak the operator's own identity and private infrastructure details through the boundary — absolute file paths that only exist on the original author's machine, internal organization or workspace identifiers, references to a private sibling project as a dependency, or a changelog claiming a clean handoff while the actual leaked strings remain in the tracked files. A "we scrubbed it" claim is only as good as a grep-proof against the tracked tree, not a memory of having done the cleanup. The durable structural fix for this class of leak is to generate the distributed copy from a single canonical source (stamped as "generated, edit upstream") and keep any per-project state workspace-local rather than synced downstream, so identity and path details cannot silently re-accumulate in hand-edited copies over time.
