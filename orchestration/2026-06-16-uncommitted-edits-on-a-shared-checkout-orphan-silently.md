---
title: Uncommitted edits on a shared checkout orphan silently when other branches come from remote main
date: 2026-06-16
category: orchestration
tags: [git, multi-agent, shared-checkout, worktrees, protected-branch]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When multiple automated agents (or humans) share one checkout of a repository, never let durable notes or state live only as uncommitted edits in that shared working tree — they will silently orphan and vanish from the team's history.

What happened: a team ran many parallel automation sessions against a single git repository. One checkout was treated as a "shared primary" that different sessions would open and edit directly, appending entries to a running log file. Several days' worth of entries were appended straight to that shared checkout but never committed. Meanwhile, other sessions did their work correctly in separate branches cut from the remote's main branch, and those branches got merged in via normal pull requests. Because a protected main branch cannot be committed to directly, the uncommitted block sitting in the shared checkout had no path to reach the remote — and because later branches were cut from the remote (not from the shared checkout's local disk state), they never inherited those uncommitted lines either. The result: a multi-day chunk of log entries existed only in one machine's disk cache, invisible to `git log`, and was one `git checkout`/reset away from being lost outright. Ironically, one of the lost entries described exactly this failure mode.

How to apply: treat any shared/reusable checkout as read-mostly. If a session needs to add durable state (docs, logs, config), do it on a fresh branch cut from the remote's current main, commit immediately, and open a pull request in the same session — never leave the edit sitting uncommitted in a shared directory "for later." Periodically diff a shared checkout's working tree against its own HEAD to catch drift before it accumulates. If your workflow already forbids direct commits to main, make sure there is always a same-session path (branch → commit → PR) available, not just a rule saying "don't edit the primary."
