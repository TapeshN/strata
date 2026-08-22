---
title: A schema-diffing provisioning tool cannot materialize a constraint that lives only in raw migration SQL
date: 2026-08-17
category: guardrails
tags: [verification, migrations, money-integrity]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A database-backed test suite ran once against a database provisioned by diffing against the
current schema definition (a common fast path for spinning up test databases) and produced one
unexpected failure: a regression test for a money-critical CHECK constraint that exists only in
the raw migration SQL, not expressible in the current schema-definition language, and therefore
never gets created by a schema-diff-based provisioning tool. Anything that lives only in migration
SQL — CHECK constraints, partial indexes, guarded backfills — is simply invisible to a database
provisioned that way; a test of such a feature either false-fails there, or worse, the feature
silently does not exist while dependent tests false-pass against a database missing it entirely.

The generalizable rule: provisioning method is part of what a test actually verifies. A database
provisioned by schema-diffing verifies the SCHEMA; one provisioned by replaying the full migration
chain verifies the MIGRATIONS. Any feature that is money-critical or otherwise safety-critical and
enforced at the database level belongs in the migration chain itself, and its test must run
against a database provisioned by replaying that chain — never assume the faster schema-diff path
is an equivalent substitute.
