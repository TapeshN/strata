---
title: A "redeploy" is a five-verb pipeline, and overriding a script's own internal variable from outside silently no-ops
date: 2026-08-30
category: infra
tags: [deploy, ci, idempotency, verification, shell]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A demo environment showed stale content twice in one review cycle, and both times every visible signal reported success. First, an operator exported an environment variable intending to redirect which source a sync step pulled from, but the sync script assigned that same-named variable internally partway through its own body — the external export was simply overwritten, and the script's own success output (a file count, a content hash) reported cleanly against the wrong source. Second, forcing a container to recreate pulled a week-old cached image rather than a freshly built one, because "recreate" only reinstantiates a container from whatever image already exists locally — it is not the same operation as "rebuild." A third, adjacent trap in the same pipeline: even a genuinely fresh image can still serve old data if pending schema migrations and seed changes were never applied against the persistent target database.

The common root cause: no single primitive owned the full meaning of "deploy." Sync, build, migrate/seed, recreate, and a final content check are five distinct verbs, and each one can exit cleanly on its own terms while the thing a human actually sees on the page stays unchanged. A healthy container status or a clean script exit is not evidence that served content changed.

The fix is architectural, not procedural: wrap the full sequence — sync, then build, then migrate/seed when schema or seed data changed, then recreate, then verify — behind one script per target, so a partial run can never be mistaken for a full one. Never let a step's internal variable be overridden from the outside; if the routing needs to change, edit the variable's assignment inside the script itself, with a dated comment, rather than exporting a same-named environment variable and assuming it wins. Most importantly, the only trustworthy witness that a redeploy actually worked is grepping the live served page for a marker of the specific content change — never a healthy process status or a clean exit code alone.
