---
title: A containerized observability tool lies by omission about host state (worktree tile read 0 against 24+ real worktrees)
date: 2026-06-14
category: infra
tags: [[observability], [docker], [container-truth], [mount-scope], [endpoint-naming], [diagnose-the-right-signal]]
confidence: learned
source: private-work
---

the mount + git land in a PR (dashboard-redesign wave). Endpoint-naming confusion is the deeper trap — `workers` vs `worktrees` are different data sources sharing a prefix.

when a CONTAINER reports a host-derived count as 0/empty, FIRST verify the mount actually covers the host source (a sibling-of-root dir is NOT under a root mount), and confirm WHICH process/endpoint the tile reads before trusting it. An observability image that shells to git-dependent tooling must ship git. And: a "rebuilt" container that still serves stale behavior may be a *different compose project* — check `docker ps` image/project name, not just "up".
