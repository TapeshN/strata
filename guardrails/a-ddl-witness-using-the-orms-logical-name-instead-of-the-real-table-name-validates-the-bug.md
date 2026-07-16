---
title: A DDL witness that uses the ORM's logical model name instead of the database's real physical table name validates the exact bug it exists to catch
date: 2026-07-14
category: guardrails
tags: [reproducibility, proofs, contracts, schema-mapping, migrations]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

An ORM that lets a model declare a different physical table name than its logical name creates a trap for any hand-written DDL or migration: a fix written against the logical model name can compile, apply without error, and still target a table that does not exist.

A production seat/entitlement bug took three attempted migrations to actually resolve. The first two both dropped an index or constraint scoped to the ORM's logical model name; both applied cleanly and did nothing, because the real physical table used a different name declared via the ORM's table-mapping directive. Confirming the table's real name required querying the database catalog directly.

The most damaging part was not the two failed fixes — it was that the verification test for the second attempt also used the wrong, logical name: it created a scratch table under that name, ran the fix logic against it, and reported success. The proof shared the exact same incorrect assumption as the code it was meant to validate, so it could never have caught the mismatch. Only when the fix and its witness were both rewritten against the actual physical table and column names did the migration take effect.

Three rules follow. First, before writing any raw DDL or migration against an ORM-mapped schema, check every model's table-mapping directive and use the physical names, never the logical ones. Second, a DDL witness fixture must construct its scratch objects under the same physical names the real migration will touch — a witness built from the logical name inherits the bug instead of catching it. Third, when a fix reports "verified" in a test but the underlying problem persists in production, suspect the witness fixture itself before re-reasoning about the fix logic; a passing test whose fixture was built on the same false premise as the bug is not evidence of anything.
