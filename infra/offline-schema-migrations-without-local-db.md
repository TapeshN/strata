---
title: Schema migrations can be authored offline by diffing before and after schemas
date: 2026-06-02
category: infra
tags: [ci, reproducibility]
confidence: learned
source: private-work
---

When no local database is available for running migration tooling in its normal interactive mode, schema migrations can still be authored by diffing the before and after schema definitions using the migration tool's diff command. This produces authentic, deployable SQL without requiring a live database connection.

The technique: capture the "before" schema from version control (`git show HEAD:schema-file`), write the "after" schema to a temporary file, diff between them using the migration tool's offline diff mode, and write the result to a timestamped migration file. The CI pipeline then applies the migration against the real database using the deploy command.

General lesson: the "I need a local database to write migrations" assumption is often incorrect. Migration tooling's diff and generate commands are typically fully offline; only the apply step requires a live connection.
