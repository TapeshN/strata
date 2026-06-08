---
title: Tooling must resolve its workspace root dynamically; hardcoded paths break on any other machine
date: 2026-06-04
category: infra
tags: [ci, reproducibility, multi-repo, worktree]
confidence: learned
source: private-work
---

Tooling that scans the workspace must resolve its root path dynamically at runtime — not hardcode a home-relative path. A hardcoded path that exists on the developer's machine will fail immediately on any other machine: a CI runner, a colleague's workstation, a container.

The resolution chain: explicit environment variable override, then derive from the script's own location, then ask the version-control system for the repository root, then a sensible default. Degrade to a no-op rather than crash or scan the wrong tree. Tests for the resolver must use temporary fixtures, not the real on-disk machine layout — a test that asserts the real home path re-encodes the original bug.

General lesson: CI on a different machine is the witness that catches hardcoded paths. You cannot catch this on the machine that has the path. Run the root-resolving tool in CI to get that witness.
