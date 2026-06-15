---
title: A findings or audit doc is a point-in-time snapshot — always re-verify each item against live main before building
date: 2026-06-13
category: orchestration
tags: [preflight, gating, docs, rollback]
confidence: learned
source: private-work
---

A findings document (crawl output, audit report, issue list) is accurate at the moment it is authored. If other branches land between authoring and execution, some or all items may already be fixed on the current tip of the main branch. Building straight from the doc without re-verification risks re-applying (and conflicting with) fixes already live.

**The scan-act-verify pattern:** before acting on any item from a findings doc, the scan step must re-verify each item against the current state of the main branch. Items confirmed already-fixed are not a failed scan — they are the gate working correctly. The correct pivot is to a regression-witness (a test that guards the now-fixed behavior) rather than a duplicate fix.

**Practical discipline:**
- Stamp every findings document with its audit date and the commit SHA at which it was generated. Staleness is then visible on first read.
- The re-verification step should be explicit in the lane's preflight, not optional. "Does this still exist at HEAD?" is a one-liner that prevents duplicate work and merge conflicts.
- A scan that returns "already fixed on main" is a positive outcome: it means the gate caught a would-be duplicate before any code was written.

**Extends to uncommitted WIP:** the same principle applies to stale work-in-progress branches. Before resuming an old branch, check whether the capability it was building has since shipped via a different lane — check for the component, function, or test-id on main, not just whether the branch has an open PR.
