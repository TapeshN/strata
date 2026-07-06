---
title: Stashing before a pull can silently carry away uncommitted rows from an append-only log that a live dashboard is reading from disk
date: 2026-07-06
category: infra
tags: [stash-ledger-loss, append-only, dashboard-stale, worktree-mount]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

To fast-forward a dirty working copy before pulling new remote history, stashing the working set (including untracked files) is a common reflex. But when part of that dirty state is uncommitted rows freshly appended to a runtime, append-only log file — the kind a monitoring dashboard or status panel reads live from the working tree, not from a database — the stash removes those rows from the file the dashboard is mounting. After the pull completes, the working tree reflects the pulled commit's version of that log, and the just-appended rows are gone from the live view even though they still exist inside the stash object. The dashboard then renders as if nothing is happening: no active session, no elapsed time, no accumulated counters, because it is honestly reporting what the file on disk now contains.

The general rule: any log file that a live process reads directly from a working directory — rather than from a database or an API — is not safe to blanket-stash before a pull. If a stash is unavoidable, diff the stashed version of that specific file against the live version afterward, identify which rows exist in the stash but not in the post-pull file, and re-append exactly those rows rather than discarding them, since an append-only log must never lose entries. Treat runtime state files differently from ordinary source files during any stash-then-pull workflow.
