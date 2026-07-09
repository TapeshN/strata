---
title: A merged schema migration is not applied to production unless the deploy pipeline explicitly runs a migrate step
date: 2026-06-29
category: infra
tags: [release, ci, rollback]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A deploy build that only regenerates the ORM client and builds the application, without a dedicated step that applies pending database migrations, will happily merge and deploy code that references a brand-new table or column while production's actual schema never receives it. The failure surfaces only the moment code tries to touch the new structure — a runtime error reporting that the relation does not exist — even though the migration file itself was reviewed, merged, and sitting in version control the whole time.

Reading the local environment file, or confirming auth and other unrelated functionality still works in production, is not evidence the schema is current; those checks can all pass while the specific new table is silently absent. The only reliable signal is the live database's own migration-history table compared against what has actually merged to the main branch.

The generalizable fix: any application backed by a migration-based schema must have an explicit migrate step wired into its deploy pipeline, not merely a client-generation step — otherwise every merged migration is inert until someone manually remembers to apply it, and that manual step will eventually be forgotten. Before trusting that a schema change has "shipped," verify it against the live database's own migration history, never against git history or a doc's claim that it was deployed.
