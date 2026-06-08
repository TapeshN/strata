---
title: Ground plan documents against version control before dispatching builders
date: 2026-06-06
category: orchestration
tags: [verify-dont-trust, dag, parallel-sessions, gating]
confidence: learned
source: private-work
---

A multi-phase plan document becomes stale as agents execute work against it. When asked to execute a plan, ground each lane's definition of done against the version-control system before dispatching builders — verify that the file, test, or export the lane is supposed to produce does not already exist on the main branch.

In a concrete case, all three phases of a plan were already merged to main. Dispatching builders would have redone merged work, producing duplicate commits and confusion.

The plan document is a hypothesis; the version-control state is the fact.

General lesson: before launching builders for any multi-phase handed-down mandate, check whether each lane's deliverable already exists. The plan doc is a snapshot from a point in time; agents may have executed past it.
