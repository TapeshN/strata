---
title: Three technical gotchas from a polish pass — blocklist grep with empty lines, cross-directory symlinks in a bundler, and duplicate CHANGELOG subsections
date: 2026-06-13
category: infra
tags: [ci, gating, ip-boundary, worktree]
confidence: learned
source: private-work
---

Three independent technical traps surfaced during a polish pass on a frontend project:

**Blocklist file with empty lines causes a universal grep match.** Running `grep -f <blocklist-file>` where the blocklist file contains blank lines causes every input line to match — an empty pattern matches all. The result is a hand-rolled IP scan that reports a false block on everything. The correct approach is to strip blank lines (and comment lines) from the blocklist before matching, exactly as the canonical IP-guard script does. When hand-verifying IP safety, use the guard script's own logic rather than a raw `grep -f` invocation.

**A bundler rejects cross-directory node_modules symlinks.** Some modern bundlers (particularly those using a Rust-based engine) raise an error when they encounter a symlink that points to a path outside the current "filesystem root" as the bundler defines it. This surfaces in worktree setups where a worktree has no own `node_modules` and symlinks to the primary's. Workaround: copy the relevant files (e.g., a test spec) into the primary checkout for the duration of the run, then remove them after.

**Duplicate subsections in a changelog block.** When a PR inserts a new subsection (e.g., `### Added`) at the top of an unreleased block rather than appending to the existing one, the result is two `### Added` headers inside the same unreleased block. Adversarial review of a changelog PR should count subsection headers within the target block, not just confirm the block header exists.
