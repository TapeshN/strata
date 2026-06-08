---
title: Discover and propagate existing standards; don't invent when one already exists
date: 2026-06-02
category: infra
tags: [multi-repo, docs]
confidence: learned
source: private-work
---

Before drafting a new cross-project standard (commit format, pull-request template, contribution guide), check whether the cleanest repository in the workspace already embodies one. If it does, the inconsistency across other repositories is the gap — copy and propagate the existing standard rather than inventing a new one. Inventing a second standard creates divergence and a future reconciliation problem.

The instinct to draft something new when asked to "keep things consistent" is natural but often wrong: the standard already exists in the best-maintained repository, and the task is propagation, not invention.

General lesson: before defining any cross-project convention, read the best-maintained repo in the workspace to see if the convention already lives there. Codify it as the canonical source and propagate; don't draft a parallel one.
