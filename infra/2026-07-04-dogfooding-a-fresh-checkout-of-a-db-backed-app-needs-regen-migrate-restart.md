---
title: Dogfooding a database-backed app on a freshly-updated checkout needs client regeneration, a local migration, and a full server restart — in that order
date: 2026-07-04
category: infra
tags: [worktree, ci, gating]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Dogfooding a database-backed application against a freshly pulled main branch produced blank authenticated pages while unauthenticated/public pages rendered fine. Two independent, compounding faults were responsible. First, the ORM's generated client was stale relative to the fresh schema — several migrations had landed since it was last regenerated — so any query touching the newly-added fields failed validation before it could return data. Second, the local development database itself had not had those migrations applied, so even a regenerated client would be querying a schema the actual local data didn't match. A long-running development server compounded the confusion by staying in a degraded state that made "restart and retest" look like it should have already fixed things when it hadn't actually restarted cleanly.

Public routes rendered because they had no database dependency at all — which masked the severity of the problem and made "everything is blank" look like a much bigger failure than the actual root cause.

The reliable recipe for dogfooding a fresh checkout of a schema-backed app: confirm the worktree is actually at the current remote head; regenerate the ORM client from the current schema; check the local database's migration status and read which host it's pointed at (never apply a migration without confirming it targets the local/dev instance, not a shared or production one); apply any pending migrations to that confirmed-local database; then fully kill and restart the development server rather than trusting an existing long-running process. Diagnose "blank" by exercising an authenticated route specifically — a public route returning 200 proves nothing about whether the app actually works for a signed-in user.
