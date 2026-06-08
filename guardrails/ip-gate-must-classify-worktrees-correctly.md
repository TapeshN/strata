---
title: An IP safety gate must distinguish coordination-layer worktrees from venture-repo worktrees
date: 2026-06-05
category: guardrails
tags: [ip-boundary, worktree, gating, isolation]
confidence: learned
source: private-work
---

A safety gate that classifies file paths as "venture" versus "coordination-layer" based solely on their presence under a shared worktree root will misclassify the coordination-layer repo's own worktrees as venture. The fix: distinguish worktrees of the coordination-layer repo from worktrees of venture sub-repos using the immediate parent directory name, not just the root path.

An over-firing safety gate — one that flags legitimate files — trains operators to dismiss it, eroding its protective value. Gate-scope bugs get corrected, never bypassed.

Also learned: diagnosing a gate's behavior from a hand-executed reproduction that uses different matching rules than the gate itself is unreliable. Ground the diagnosis in the gate's actual source code before concluding it has a bug.
