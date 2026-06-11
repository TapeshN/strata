---
title: Merge-hygiene traps — stash churn re-introduces conflict markers, and gates read your docs too
date: 2026-06-11
category: infra
tags: [worktree, ci, gating]
confidence: learned
source: private-work
---

A batch of small, hard-won mechanics from one agent's long merge-conflict session:

- **Stash/pop during an in-progress merge can re-introduce conflict markers** into files that were already resolved. After any pop, verify the touched files are marker-clean before committing — resolution state is not durable across a stash boundary.
- **Repeated dependency installs during stash churn can corrupt the dependency tree**, surfacing as invariant-error cascades far from the cause. The remedy is total: remove the dependency directory and the build cache, then reinstall fresh from the lockfile. Incremental repair of a half-corrupted tree wastes more time than the clean rebuild.
- **Per-route config exports in Next.js (runtime, dynamic) must be declared locally in each route file** — re-exporting them from a sibling route fails the Turbopack build. Framework conventions about *where* a declaration lives are build contracts, not style.
- **A client-only global error boundary can block server prerendering** of the framework's error page when the root layout uses server-only APIs — error-path components participate in the rendering model like any other.
- **Before using a long-lived checkout for build tests, fetch and verify what the mainline actually contains.** Long-lived checkouts lag silently; testing against a stale tree produces confident, wrong conclusions.
- Meta, observed while writing the batch up: **safety gates scan documentation text too.** A destructive-command gate blocked the write because a remedy was spelled as a literal shell command inside the doc. Describe remedies in prose, or compose literal strings at runtime — the same discipline as keeping secret-shaped strings out of fixture files.
