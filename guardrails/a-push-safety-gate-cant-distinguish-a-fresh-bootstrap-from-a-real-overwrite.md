---
title: A destructive-push safety gate that matches command TEXT can't tell a fresh-repo bootstrap from a real overwrite
date: 2026-07-19
category: guardrails
tags: [gating, git, safety-gate-calibration, bootstrapping]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Creating a brand-new, empty remote repository and pushing its first commit to the default branch is the standard bootstrap sequence — there is no shared history to clobber and no branch protection yet. A safety gate designed to block a force-push or an overwrite of a protected branch can't distinguish that legitimate case from a real destructive push, because it matches on the command's TEXT ("push ... main"), not on the remote's actual state.

This is correct, calibrated behavior for the gate (over-blocking a rare legitimate case beats under-blocking a real one) but it costs a manual round-trip on every new-repo bootstrap. The fix is a state-checked exception, not a text-pattern hole: allow a first push to a branch IFF that branch does not yet exist on the remote (a cheap, empty-result check against the remote's own ref list) — never weaken the gate for the general case, only add a narrow, provably-safe exception for the one where the destination is provably empty.
