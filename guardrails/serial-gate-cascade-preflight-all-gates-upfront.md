---
title: A serial gate cascade surfaces one failure per round; satisfy all gates upfront rather than paying one round each
date: 2026-06-22
category: guardrails
tags: [gating, preflight, ci, release]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

When a repository runs its gates serially — type-check, then changelog, then import-availability, then schema validation — each CI round reveals exactly one failure. An agent brief that says "fix the failing gate" costs one dispatch round per gate, even when every remaining failure was knowable in advance.

The expensive lesson: a test suite that runs 2000+ checks blocked for four consecutive rounds on four sequentially discovered problems, each trivially fixable if the brief had enumerated them upfront.

The pattern that avoids the cascade:

Before a build agent starts, enumerate the full gate list for that repository (grep the CI workflow file). For each gate, assess whether the current change satisfies it. Common cascade members: a changelog entry for every feat or fix commit, a recognized document type field for any new document, a lazy import for any runtime dependency not on the CI runner, and no duplicate subsection headers in append-only files.

A worker brief that pre-satisfies all of these before writing a line of change code eliminates the cascade entirely. A narrow-fix subagent told to repair only one named issue reaches for broad context-gathering commands and runs live side-effects, bundling changes outside its nominal scope. Forbid it: name the exact file and the exact change, and explicitly prohibit running regen/sync/build-all or committing files outside the named scope.

An agent that stalls after pushing a commit may have left a broken bundle on the remote. Always inspect what it pushed before treating the branch as abandoned.
