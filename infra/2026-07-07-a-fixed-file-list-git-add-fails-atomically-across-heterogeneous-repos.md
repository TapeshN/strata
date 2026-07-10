---
title: A git add with an explicit file list fails atomically the instant one path is missing
date: 2026-07-07
category: infra
tags: [git, multi-repo, worktree, continuity]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Staging a commit across several repositories that share a common set of branding/config files (a license, a readme, a shared config) using the same explicit list of filenames for every repo seems safe when the list is copy-pasted once. It is not: if any single repo in that set is missing even one of the named files, the staging command fails as a whole for that repo and stages nothing — not even the files that DO exist. The visible symptom downstream is confusing: a "nothing to commit" state, and a failed attempt to open a pull request because there is no difference between the branch and its target.

The fix in the moment was simply to stage each repo's actual, present files individually.

The general rule: when committing across multiple repositories (or any situation with a generated or uncertain file list) whose file sets are not perfectly uniform, never stage with a fixed, explicit list of filenames that assumes every one of them exists in every target. Stage everything, with narrow excludes for things that should never be committed (dependency directories, build output), so a missing optional file in one target never blocks the whole commit.

A related, same-session lesson: a mid-session handoff between two different models or agents working the same task is itself a boundary event, similar to a context-compaction boundary — the outgoing agent's job is to leave a complete, self-contained handoff (a full snapshot of decisions made, work in flight, and next steps) and to close out any open loops (merge or explicitly park anything half-finished) before handing off, so the incoming agent can continue without needing to reconstruct anything from the prior conversation.
