---
title: Derive generated names from a unique id segment, never a fixed-length suffix
date: 2026-07-06
category: infra
tags: [dispatch, naming, branch-collision, unique-id, automation]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

When you auto-generate a name (a branch, a temp file, a queue key) from part of a longer identifier, taking a fixed-length trailing slice is unsafe if that identifier has a constant suffix. The slice ends up identical for every item, and everything collides onto the same name.

What happened: an automation pipeline generated per-task git branch names as a prefix plus the last 12 characters of each task's id. Every id in the system ended in the same literal suffix (a fixed tag appended by the dispatch system, e.g. "-worker-job"), so the last 12 characters were always that constant string regardless of which task produced the id. Two unrelated tasks running in parallel were both handed the exact same branch name. The second task to push found the first task's commits already sitting on that branch and, in the course of trying to produce a clean diff against the base branch, reverted the first task's work outright — then failed to open a pull request at all, silently destroying real completed work with no visible error beyond a vague failure status.

How to apply: whenever a generated name is derived from an identifier by slicing or truncating, verify the sliced portion is actually unique per item — check whether the ID format has a shared prefix or suffix baked in by convention. Prefer deriving from a field guaranteed to vary per item, such as a timestamp segment (down to the second) or a random/incrementing counter, not "the last N characters." Add a regression test that constructs two ids differing only outside the slice window and asserts the derived names differ. More generally: any time multiple concurrent workers can independently generate a resource name, treat name collision as a class of bug worth a dedicated test, because the failure mode (one worker silently clobbering another's output) can look like unrelated flakiness rather than a naming defect.
