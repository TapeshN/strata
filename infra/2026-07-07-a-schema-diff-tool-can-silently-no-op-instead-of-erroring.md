---
title: A schema-diff tool can silently no-op instead of erroring when it lacks a dependency
date: 2026-07-07
category: infra
tags: [database, migrations, tooling-fail-quiet]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A database schema-diffing tool, when asked to compare two migration states, can return a genuinely empty result with a success exit code even when the underlying schema DID change — because the tool needed a temporary "shadow" database to render the actual SQL difference, and without one configured it fails silently rather than erroring. The empty output is indistinguishable, at a glance, from "there is truly nothing to migrate."

Trusting that empty diff as a positive "no change needed" signal would have meant shipping a schema change with no corresponding migration at all.

The fix: when a diffing/comparison tool no-ops, do not treat the absence of output as evidence of no change. Confirm independently whether the source actually changed (a plain source diff of the schema definition), and if it did, author the migration by hand, verifying by inspection that it is purely additive and safe (adding a column with a default value, for instance, is typically a cheap, non-locking, non-destructive operation on most modern relational databases).

A related lesson from the same review cycle: when an independent review of a change returns an approval but flags a low-severity issue (in this case, a metering/accounting formula that would undercount real usage once a caching feature became active), the right move is to fix it in the SAME change before merging, not to defer it to a follow-up that may never get prioritized — especially when the flagged issue would otherwise quietly seed a wrong number into a system whose entire purpose is to be accurate and auditable.
