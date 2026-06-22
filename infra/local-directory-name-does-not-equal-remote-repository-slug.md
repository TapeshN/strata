---
title: A local directory name does not equal the remote repository slug — verify with git remote before referencing
date: 2026-06-07
category: infra
tags: [ci, boundaries, determinism, release]
confidence: learned
source: private-work
---

A local checkout directory is named by whoever cloned or created it, independently of the repository's remote URL. Assuming the directory name matches the GitHub repository name is wrong when the two were chosen independently.

A concrete case: a repository whose local directory was named with a prefix (for example `agents-foo/`) pushed to a remote named without that prefix (for example `TapeshN/foo`). Any tool invocation that constructed the remote URL from the directory name — such as `gh --repo owner/agents-foo` — silently targeted a non-existent repository and returned a "could not resolve" error. The fix was to read `git remote -v` or the PR URL, which give the canonical remote name, rather than inferring it from the directory.

The same assumption appears in CI configuration: a workflow that hard-codes the expected repository name from the local directory name will misfire when the names diverge.

Prevention: never derive the remote repository owner/slug from the local directory name. Read it from `git remote -v` or from the URL returned by `gh repo view`. This is especially important in tooling that generates `gh` commands, webhook configurations, or CI badge URLs programmatically — the source of truth is the remote, not the local path.
