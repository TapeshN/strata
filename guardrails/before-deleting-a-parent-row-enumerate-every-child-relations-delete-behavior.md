---
title: Before deleting a parent row, enumerate every child relation's delete behavior — including relations with no foreign key at all
date: 2026-07-25
category: guardrails
tags: [referential-integrity, verification-design, migrations]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A delete that completes without error is not proof that it cleaned up correctly. Before removing a parent record from a relational schema, the full safety picture requires enumerating, for every table that references it, exactly which delete behavior applies: cascade (children are removed too), nullify (the child survives with its reference cleared), restrict (the delete is blocked), or — the easy one to miss — no foreign-key constraint at all, where the database has no awareness of the relationship and nothing happens to the "related" rows on either side. In a real case, of several dozen referencing tables roughly a third used cascade, a third used nullify, none used restrict, and a further handful carried what was logically a reference column with no foreign key recorded at all. A naive delete would have succeeded silently while leaving authentication-capable records attached to no owner still active, plus orphaned rows in the FK-less tables — exactly the outcome a clean exit code hides.

A related point: a verification query written after a destructive operation must encode WHY a row is wrong, not merely what a wrong row looks like. A check for "the reference column is empty" will also match records that are legitimately unowned by design (an internal/staff record, say), producing false alarms at precisely the moment — right after a destructive change — when you are least able to safely dismiss them. The predicate needs to combine the shape (empty reference) with the additional condition that actually distinguishes a real defect from a valid state.
