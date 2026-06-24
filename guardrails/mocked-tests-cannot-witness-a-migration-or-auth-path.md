---
title: Mocked tests cannot witness a migration or auth path — only a real run refutes it
date: 2026-06-23
category: guardrails
tags: [evals, determinism, verify-dont-trust, gating, contracts]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A PR landed with many passing unit tests, clean type-checking, and a clean build. It contained two runtime-fatal bugs: garbage text captured from a CLI's standard output was embedded in a database migration file (causing a SQL syntax error), and a required database field was impossible to populate through the authentication primitive that was expected to set it. Both failures were invisible to the test suite because every test mocked the database layer — the migration was never applied and the real authentication path was never exercised.

Mocked tests assert that the code calls the right functions with the right arguments. They cannot assert that the SQL parses, that the migration applies to a real database, or that the end-to-end flow completes without error. A mocked test shares the code's assumption that the underlying operation is well-formed; only a real run can refute that assumption.

**The rule:** for any change that includes a database migration or an authentication path, the Definition of Done requires a real-database integration test that actually applies the migration and exercises the primary path. A dispatch brief shipping migrations must include "migration applies cleanly to an empty database" as an explicit acceptance witness.

A secondary lesson: generated migration files should be inspected for non-SQL content (CLI notices, progress bars, box-drawing characters) before they are committed. A pipeline that pipes migration output through a generator must not capture standard output alongside the SQL.
