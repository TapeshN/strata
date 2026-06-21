---
title: Union-resolve merge strategy is correct only for append-shaped files
date: 2026-06-11
category: orchestration
tags: [dag, parallel-sessions, multi-repo, worktree, release]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

During a serial merge sweep of sibling branches, a regex-based keep-both union was applied to all conflicting files. Changelog files unioned cleanly because they are append-only by nature. Code files did not — both sides of every conflict were concatenated, interleaving function definitions, duplicating class registrations, and in one case stripping a `finally` block from inside a `try/finally` pair. The result was a syntax error that surfaced only at import time, well after the merge appeared to succeed.

The structural reason this always fails on code: a union driver has no concept of scope or block structure. It keeps all lines from both sides, which can produce syntactically valid but semantically incorrect files, or files that are not syntactically valid at all. Any merge conflict in a code file requires the two sides to be compared semantically and one correct version to be chosen — there is no mechanical shortcut.

The safe allowlist for automatic union-resolve is narrow: append-only documents whose schema makes all additions non-conflicting, such as changelogs with a clear section structure and append-only records. Any file that is not provably append-shaped must stop the merge chain and wait for human or agent semantic resolution.
