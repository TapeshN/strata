---
title: A parallel work stream through a different tool is a real, invisible collaborator — check for it before merging
date: 2026-08-16
category: orchestration
tags: [parallel-sessions, multi-repo]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Work was built for a stretch of time in fresh branches off the mainline, blind to a
second, concurrent stream of changes landing directly on the branches a set of deploy
targets actually build from — commits made through a different tool entirely, while the
usual capacity for this agent was temporarily unavailable. One of those branches turned
out to be well over a dozen commits ahead of, and dirty relative to, the mainline;
merging the new work into the mainline then diverged it further from what the deploy
targets were actually running.

The generalizable lesson: whenever an operator mentions switching tools, running low on
capacity, or working through a different channel, treat any branch a deploy target
reads from as a potentially-owned-by-someone-else surface, not an assumption-safe base.
At session start, and again before any merge or deploy, diff each relevant branch
against the mainline and read its recent commit history — a branch sitting ahead of the
mainline is unmerged work by a real collaborator, human or otherwise, and the fix is to
reconcile and integrate it, never to silently overwrite or ignore it by converging
everything onto a branch that collaborator isn't watching.
