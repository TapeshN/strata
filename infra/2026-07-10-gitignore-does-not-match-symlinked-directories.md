---
title: .gitignore's directory pattern does not match a symlink of the same name
date: 2026-07-10
category: infra
tags: [git, gitignore, symlink, node_modules, pre-commit, worktrees]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A `.gitignore` entry like `node_modules/` uses a trailing slash to match a *directory* — but when `node_modules` in your working tree is actually a symlink (pointing at a shared cache, a hoisted install, or another worktree's copy), that pattern silently fails to match it. Git sees a symlink, not a directory, so the ignore rule doesn't apply, and a broad staging command like `git add -A` happily stages the symlink (and, depending on git version and follow-symlink settings, sometimes its resolved contents) into the commit.

**What happened:** In a workflow that uses git worktrees with a symlinked `node_modules` (to avoid reinstalling dependencies per worktree), this bit twice in a row — the same commit picking up a staged `node_modules` symlink both times, despite `.gitignore` looking correct on inspection. The fix each time was reactive: `git rm --cached node_modules` right before committing. That's a workaround, not a guarantee, because it depends on remembering to run it every time.

**How to apply:** If your setup uses symlinked or otherwise non-standard `node_modules` (or any other normally-ignored directory) — common in monorepos, worktree-based workflows, or shared dependency caches — don't trust `.gitignore`'s directory-slash pattern to cover it. Add a mechanical pre-commit check: `git ls-tree -r HEAD --name-only | grep node_modules` (or a pre-commit hook running the equivalent against the index) should always return empty. Treat any non-empty result as a hard stop before the commit lands, rather than relying on `.gitignore` or on remembering a manual `git rm --cached` step. The general lesson: ignore-file patterns are filesystem-type-sensitive, and symlinks are a common blind spot — verify ignore behavior empirically for any non-regular-file path in your tree, don't assume it "just works" the same as a real directory.
