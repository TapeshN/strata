---
title: A hook that resolves its state file relative to the current worktree can read a different file than the CLI tool that wrote it from the primary checkout
date: 2026-08-21
category: infra
tags: [hooks, worktrees, gates]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A command-line tool wrote a permission grant into a state file located under the PRIMARY checkout's
own working directory. An automated pre-action hook, running later from a linked worktree of the
same repository, resolved the "same" state file relative to that worktree's own working directory
instead — a different physical path — and so reported the grant as never having happened, even
though the CLI tool had reported success moments earlier.

The generalizable rule: any runtime state file that is written by one tool and read by a gate or
hook must have BOTH the writer and every reader resolve its location through the exact same
root-finding logic (for example, the repository's shared git directory, which is identical across
every worktree of the same repo) rather than each independently assuming "the current working
directory." Any gate of this shape deserves a trigger test that specifically runs the writer and
the reader from two DIFFERENT linked worktrees of the same repository, since that is exactly the
condition under which "resolves from cwd" silently breaks.
