---
title: A tracked, absolute-path symlink standing in for a dependency directory deadened every working copy's dependency resolution at once
date: 2026-09-10
category: infra
tags: [tracked-node-modules, ignore-pattern-shape, placebo-gate, absolute-path-in-repo]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A repository carried a committed, tracked symlink standing in for its dependency directory, pointing at an absolute path on one specific machine. On the machine that path had originally been created on, that absolute path resolved back to the very same location — a self-referencing link — so every attempt to resolve dependencies from any working copy failed with a "too many levels of symbolic links" error. The project's ignore file listed the dependency-directory name only in its trailing-slash, directory-only form; that pattern does not match a symlink of the same name, which is exactly how the symlink slipped into a tracked commit in the first place.

Fix at the source: removed the symlink from the tracked index, and the ignore rule was extended to carry both the trailing-slash (directory) form and the bare (symlink) form of the same name — the directory-only pattern alone is not sufficient. One useful side effect of finally fixing this: it was the first time a large fraction of the project's own automated test suite had ever actually executed rather than silently skipping, because the broken dependency resolution had been quietly short-circuiting a whole category of database-backed tests before this point.

Prevention, generalized: an entry for a dependency directory showing up in a routine change review is never a convenience symlink to wave through — treat it as a hard stop until confirmed. And more generally, an ignore pattern written for a name that could plausibly be either a real directory or a symlink needs both forms explicitly, in any language or ecosystem, because the two file-system object types are not interchangeable to a directory-only glob.
