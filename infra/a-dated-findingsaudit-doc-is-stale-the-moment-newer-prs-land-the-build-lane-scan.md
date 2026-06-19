---
title: A dated findings/audit doc is stale the moment newer PRs land — the build-lane SCAN must re-verify "already exists" against live main
date: 2026-06-13
category: infra
tags: [scan-first, stale-findings, re-verify-at-build, duplicate-work-prevention, scan-act-verify]
confidence: learned
source: private-work
---

the reusable scan-act-verify workflow's scan prompt already mandates per-item re-verification against current main — this lane VALIDATED that gate paid off; lane intent reinforced to carry the findings doc's audit date and re-check each item vs HEAD.

never build directly from a dated findings doc — the SCAN re-verifies each item against live `origin/main` first; stamp findings docs with their audit sha/date so staleness is visible. A scan that returns "already fixed" is the gate WORKING, not a wasted scan.
