---
title: A five-step recipe for safely swapping a filesystem bridge for a durable DB queue
date: 2026-07-10
category: infra
tags: [database-migration, prisma, prod-safety, orm, durable-queue]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

**Rule:** When you need to move an app off a serverless-fatal storage pattern (e.g., writing to the local filesystem in a platform that gives you no durable disk) onto a durable database-backed queue, there's a five-step recipe that gets you there with zero production risk and without resetting anyone's existing data.

**What happened:** The team needed to replace a filesystem-based bridge — code that wrote hand-off files to local disk, which silently breaks the moment you deploy to a stateless serverless runtime — with a durable database queue. The naive move (`prisma migrate dev`, or any tool that diffs live against a shadow database) risks a destructive reset of real data. Instead: (1) generate a pure schema-to-schema diff with no database or shadow-database involved at all; (2) hand-write that diff into a timestamped migration file, making sure the timestamp sorts after the latest existing migration; (3) apply it with the deploy-only command variant, which only ever applies pending migrations and never resets a database; (4) if working in an isolated worktree/branch, give it its own fully independent dependency install rather than a symlinked one — a shared client directory means regenerating the ORM client for the new model can silently pollute the main working tree's client; (5) before running any database command, explicitly unlink or unset whatever points at the production connection string, source only a local/dev connection, and assert the resolved connection host is localhost before proceeding. Only after the schema lands do you cut application code over to the new interface and delete the old filesystem code and its tests.

**How to apply:** Generalize this whenever you're evolving a schema next to data you can't afford to lose: separate "compute the diff" from "apply the diff" so no tool ever gets a chance to auto-reset anything; treat write access to a production-pointing credential as something you must actively and verifiably disable, not just avoid; and isolate any dependency/build step that regenerates a shared client when working in a parallel branch.
