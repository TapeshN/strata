---
title: A worktree garbage-collector judging purely on git state can reap the directory a live session is running from
date: 2026-07-01
category: infra
tags: [worktree, parallel-sessions, lifecycle, isolation]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A worktree cleanup tool that reclaims directories once their branch is merged and their tree is clean is, by that logic, entirely correct — merged and clean really does mean "no longer needed" from git's point of view. But git has no concept of "a running process is using this directory as its working directory right now." A coordinating session running from exactly such a worktree can have its own project directory reclaimed mid-task by its own cleanup pass.

The blast radius is severe: any tooling that resolves paths relative to the project directory (hooks, path-anchored scripts) fails immediately with file-not-found, hard-blocking every subsequent action for that session and for any child processes that inherited its environment. Recovery requires an external restart, though any work that had already been pushed or committed to its own branch survives independently of the reaped directory.

The general lesson: a reaping or pruning operation's safety predicate should never be purely git-state-based when the candidate set could include the environment the operation is currently running from. Before running any cleanup that removes directories by criteria (merged, clean, stale), check whether the calling process's own working directory is in the candidate set. The fix belongs in the tool itself — checking real OS process liveness (which processes have which directories as their current working directory) before deleting a candidate, with a loud skip rather than a silent removal when a live process is found.
