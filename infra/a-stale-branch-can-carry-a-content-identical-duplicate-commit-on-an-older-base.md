---
title: A stale branch can carry a content-identical duplicate of your commit on an older base — diff before you reconcile
date: 2026-07-21
category: infra
tags: [git, branch-hygiene, reconciliation]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A remote branch that looked like it had diverged ("ahead by several commits, behind by one") turned out, on inspection, to carry a commit whose actual net content — the same schema change, the same diff — was identical to a commit already produced independently on a different, newer base. Merging that stale branch back in would only manufacture pointless conflict noise over changes that already exist; force-pushing over it to make the histories match is a destructive-class operation that should be avoided entirely.

**The rule:** before choosing how to reconcile two branches that appear to have diverged, diff the actual NET CONTENT of the two commits in question rather than assuming divergence from the ahead/behind counts alone. If the content is genuinely equivalent, deliver your work from a fresh branch off the verified-good history and let the stale, now-redundant branch be cleaned up separately — never force-push to resolve a divergence you can simply route around.
