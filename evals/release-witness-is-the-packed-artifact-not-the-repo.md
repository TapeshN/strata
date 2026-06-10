---
title: Repo-green is not consumer-working — the release witness is the packed artifact installed from a clean directory
date: 2026-06-10
category: evals
tags: [release, consumer-truth, witness-design, packaging]
confidence: learned
source: private-work
---

A published CLI package was dead on arrival for every installer: its executable shim spawned a development-only path that was never included in the published tarball. Every repository-side gate passed — build, tests, type checks — because none of them ever installed the artifact a user actually receives. The defect was caught only by a "user-zero" audit that installed the published package into a clean directory and ran it cold.

The general principle is witness design applied to publishing: the thing under test must be the thing the consumer gets. A release ritual must include at least one consumer-truth smoke test — pack the artifact, install it into a temporary directory with no access to the source tree, and run its entry points. Anything verified only against the repository proves the repository, not the release.
