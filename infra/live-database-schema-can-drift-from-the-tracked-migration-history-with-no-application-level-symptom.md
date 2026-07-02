---
title: Live database schema can drift from the tracked migration history with no application-level symptom
date: 2026-07-02
category: infra
tags: [reproducibility, ci, release]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A routine migration-diff check, run to validate an unrelated schema change, surfaced that a production database's table still carried several columns that the tracked schema no longer declared. Neither the application (which uses the generated client built from the tracked schema) nor an ordinary query against that table would ever reveal the orphaned columns — only a diff between the live database and the tracked schema definition catches it.

The likely cause: a schema change reached the live database out-of-band from the committed migration history at some point, and nothing since then compared the two directly.

The fix is procedural, not one-time: run a schema-diff between the live database and the tracked schema as a periodic or pre-release check, not just incidentally when debugging something else. When an orphaned column is found, make a deliberate decision — adopt it back into the tracked schema, or write a real drop-migration — rather than leaving the two silently diverged. A CI or preflight gate that fails when live schema diverges from tracked schema beyond the pending-migration set closes the gap permanently.
