---
title: Two fan-out shapes for parallel builds, and why dashboard artifacts need human-readable names
date: 2026-07-16
category: orchestration
tags: [parallel-sessions, worktree, subagents, docs]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

There are two genuinely different shapes a multi-agent build fan-out can take, and conflating them produces either a fragmented feature or a wasted worktree. When N independent features are being built at once, the right shape is N worktrees, each producing its own pull request, batched to one deploy. When a SINGLE feature is too large for one agent to build in one pass, the right shape is different: sub-agents each fork from and contribute back to one shared integration branch, and a dedicated integration/verification agent resolves the inevitable conflicts and reconciles the parts before that branch becomes the one pull request to the main line. Picking the first shape for a feature that actually needs the second one fragments a coherent feature into a dozen half-implementations that never quite fit together; picking the second shape for genuinely independent features serializes work that could have run in parallel. The distinguishing question to ask before fanning out: do these workstreams share files and state, or are they truly disjoint? Disjoint file ownership up front minimizes conflicts either way, and the integrator (in the split-feature shape) should run the whole-batch verification gate once, on the reconciled branch, rather than trusting each contributor's local green.

A related, smaller-scale but recurring failure: any dashboard, ticker, or status surface that displays in-flight agent work needs a name a human can read at a glance — the feature plus the role (for example, "build: cost-limit fix" or "verify: tenant isolation") — never an opaque run identifier or a randomly generated slug. A card on an operational dashboard that requires clicking through to understand what it represents is a defect in the observability layer, not a cosmetic nit; it directly slows down a human's ability to triage a fleet of concurrent agents at a glance. The fix is cheap and mechanical: name every workflow run, every agent label, and every worktree branch with the feature + role convention from the moment it's dispatched, and render that label — not the underlying harness run ID — on any human-facing surface.
