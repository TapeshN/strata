---
title: A negative predicate over a nullable column evaluates to unknown, and the row silently leaves the result set
date: 2026-08-23
category: guardrails
tags: [database, determinism, fail-closed, review-loop]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A work queue needed to exclude machine-generated items, and the exclusion was written as the negation of a compound condition: not (the marker column is unset AND (the title matches a marker OR the body matches that marker)). The body column is nullable.

For any row with no body, the body comparison is UNKNOWN rather than false, the conjunction containing it is unknown, and the negation of unknown is still unknown — which does not satisfy a filter. So a legitimate row with an empty body silently dropped out of the queue. Nothing errored. Work simply stopped being claimable for one row shape, which is the worst kind of fail-closed stall: invisible, data-dependent, and reproducible only by the exact record nobody thought to create.

The witness mattered as much as the fix. The defect only surfaced when a delta review ran against a real database through the PRODUCTION writer — the one that stores an explicit null when a specification is empty. Every fixture that always populated the column agreed with the buggy code's own assumption and proved nothing.

Three rules follow. Any negative predicate over a nullable column needs an explicit "is not null" leg inside the same clause, so the expression can never evaluate to unknown. Any test for such a predicate needs a positive control in which that column is actually null and the row must still appear. And the review loop applies to the coordinator's own hand-written fixes exactly as it applies to an agent's: this defect was introduced by the coordinator patching a reviewer's earlier finding by hand, and it was the next review round that caught it.
