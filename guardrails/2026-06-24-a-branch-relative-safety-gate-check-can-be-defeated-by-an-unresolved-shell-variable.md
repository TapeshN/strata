---
title: A branch-relative safety-gate check can be defeated by an unresolved shell variable in the command it inspects
date: 2026-06-24
category: guardrails
tags: [gating, worktree, boundaries]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A destructive-operation safety gate that inspects the shell's current working directory's branch, to decide whether a command is a protected-branch commit, can be defeated by a `cd` whose target is a shell variable rather than a literal path. The static parser backing the gate cannot expand a variable at analysis time, so it falls back to evaluating the shell's default working directory — which, in a long-running session, is often the protected branch itself. A perfectly safe worktree commit, written as "assign a path to a variable, then cd into it and commit," is therefore false-flagged as a commit on the protected branch, purely because the gate never resolved the variable.

The workaround is mechanical: always use a literal absolute path in the `cd` (or the equivalent path-scoped flag most version-control tools support) for any git operation inside an automated or scripted flow, rather than an intermediate variable. The deeper fix belongs in the gate itself — before evaluating the current branch, it should first try to resolve a leading directory-change in the command being inspected, including simple variable assignments, rather than assuming the shell's ambient working directory is authoritative.

The general lesson: a safety gate that keys its decision off ambient session state (current directory, current branch) rather than the literal command text is vulnerable to any command form that changes that state within the same line. Any gate design should enumerate the syntactic forms its own users will legitimately write, including variable indirection, before trusting a snapshot of ambient state as ground truth.
