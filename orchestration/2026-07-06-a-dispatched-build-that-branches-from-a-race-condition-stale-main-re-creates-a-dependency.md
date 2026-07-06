---
title: A dispatched build that branches from a race-condition-stale main re-creates a dependency it was told to consume, and a green CI check cannot catch it
date: 2026-07-06
category: orchestration
tags: [cursor-dispatch, stale-base, spec-conformance, re-creation, model-by-task]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Dispatching a dependent build immediately after merging its prerequisite created a timing race: the dispatch's starting reference resolved to a commit from just before the merge landed, so the new build's base did not actually contain the schema, migration, or helper it was instructed to reuse. Told to "consume" files that were, from its own point of view, simply absent, the agent did the only consistent thing available to it and re-created them from scratch — re-deriving the same models, the same migration, and the same gate logic under the same names. The resulting pull request compiled cleanly and every automated check passed, because nothing in continuous integration checks for "did this branch invent a duplicate of something that already exists on the true current main" — that is a semantic property of the diff's relationship to the dependency graph, not a syntactic one a compiler or test runner can see.

Two structural fixes follow. First, any dispatch that depends on a just-merged prerequisite must resolve its starting point to the current remote head at dispatch time, and when a dependency merge is genuinely fresh, wait for and branch from the confirmed post-merge commit rather than racing it. Second, a returned build needs a conformance check that specifically asks "does this diff touch a file, model, or migration that already exists upstream and was described as something to reuse" — passing tests is orthogonal to that question.

When a build like this is discovered, the safest recovery is to salvage the genuinely new, non-duplicated pieces into a fresh branch cut from current main, rewrite the correctness-critical logic by hand rather than trusting the same agent to redo it consistently, and discard everything that duplicates what the base already has. Re-dispatching the same task against the same stale assumption tends to reproduce the identical failure.
