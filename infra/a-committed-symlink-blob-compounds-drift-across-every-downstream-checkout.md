---
title: A dependency-directory symlink accidentally committed to the shared branch compounds drift across every downstream checkout
date: 2026-07-18
category: infra
tags: [git, worktree, multi-repo, isolation]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A symlink standing in for a normally-ignored dependency directory (for example, `node_modules` pointed at a shared install) got committed onto the shared main branch. The immediate cause is a known gap — a `.gitignore` directory pattern with a trailing slash matches a real directory but not a symlink of the same name — but the more useful lesson is what happens DOWNSTREAM once that symlink is already sitting on the shared branch, because that's where it actually compounds.

Once the symlink is tracked on origin, every existing checkout that already has its own local `node_modules` (as a real directory, or its own separate symlink) reads as permanently "dirty" the moment it fetches the change, because the tracked path conflicts with local state. A loss-safe automated refresh routine — one deliberately designed to refuse touching anything dirty or uncommitted, rather than risk clobbering in-progress work — correctly refuses to fast-forward any checkout in that state. That refusal is the SAFE, correct behavior of the tooling; the actual problem is that the checkout stays permanently behind, silently, because the thing making it "dirty" is never going away on its own. Left unnoticed across several merges, this meant a live, long-running process kept executing against stale code, and a recon/audit pass that inspected a local checkout to answer "has this feature shipped yet" reported a freshly-merged feature as still unshipped — because it was reading the stale, un-refreshed checkout instead of checking origin directly.

**Two general lessons.** First, a persistent "primary is dirty and can't be fast-forwarded" warning that keeps reappearing across multiple merges is an incident to investigate (what path, since when), not ambient noise to filter out — a refresh routine repeatedly declining to touch a checkout is exactly the situation its own safety design exists to flag loudly. Second, any automated or agent-driven claim of the form "this feature is missing/unshipped" must be grounded against the shared remote's current state (the actual tip of the main branch), never against a local checkout that could itself be silently stale — a recon pass that trusts its own local `git log` without first confirming that checkout is caught up can produce a confidently wrong answer.
