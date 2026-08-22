---
title: A .dockerignore file is a property of the build context, not of one Dockerfile — a second packaging pipeline sharing the tree inherits it
date: 2026-08-22
category: infra
tags: [docker, demo-infra, release]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A repository added its own "start closed, then re-include" `.dockerignore` file to support a new Dockerfile it introduced for its own container packaging. A separate, pre-existing pipeline that packages the same repository for a different purpose — using a different Dockerfile and a plain "copy everything" instruction — began failing its build immediately after, because a file the second Dockerfile needed was now excluded by the first Dockerfile's ignore rules.

The root cause: `.dockerignore` is scoped to the build context (the directory tree handed to the Docker daemon), not to any one Dockerfile. Two Dockerfiles that build from the same tree share exactly one ignore policy, whichever `.dockerignore` sits at the root of that context. A green CI run for the repository that added the file proves nothing about a foreign pipeline building from the same tree with different assumptions.

General rule: when a repository gains its own container packaging (or any build tooling that introduces exclusion rules on its source tree), re-run every other pipeline that also builds from that tree before merging — a passing repo-local CI check does not exercise, and cannot catch, a foreign consumer's build.
