---
title: A rename migration must sweep config and hooks, not just docs
date: 2026-05-31
category: infra
tags: [multi-repo, config, boundaries, interfaces]
confidence: learned
source: private-work
---

Renaming a set of local directories was treated as a documentation problem — an agent converged all the prose. Two non-doc references silently broke: a tool-config file still pointed an absolute path at a now-dead directory (so those tools failed to load), and a hook's hard-coded allow-set still listed the old directory name (so a renamed control-plane dir was misclassified and subjected to scanning meant for other repos).

Root cause: absolute paths and identifier sets live in config files, hook logic, and ignore-files — none of which show up in a prose grep. Untracked or ignored config is especially invisible because it isn't in the committed tree.

General lesson: a rename's blast radius includes every place a directory name is hard-coded. The migration checklist must grep the old name across config, hooks, and ignore-files — not only docs — ideally via a single rename tool that reports every hit across all of them before the move.
