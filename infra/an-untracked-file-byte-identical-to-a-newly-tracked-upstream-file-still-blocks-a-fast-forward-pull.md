---
title: An untracked file byte-identical to a newly-tracked upstream file still blocks a fast-forward pull
date: 2026-07-22
category: infra
tags: [git, worktree, refresh, operational]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

After a pull request landed upstream that added new files to version control, a local checkout that already had matching untracked copies of those same files on disk refused a fast-forward pull with a "local changes would be overwritten" error — even though every other signal (zero commits ahead, some commits behind, a clean tracked working tree) said the fast-forward should be trivial. Git's fast-forward safety check considers any untracked file that collides with an incoming tracked path a conflict, regardless of whether the file's content is actually identical to what is about to be checked out.

The practical fix is to diff each colliding path against the upstream version before touching anything, and only remove the local untracked copy once it is confirmed byte-identical — never assume identity from the fact that the pull is merely refusing to proceed. A checkout can look clean by every conventional measure (nothing staged, nothing modified, branch fully caught up on commits) and still be blocked by files that were never tracked in the first place; "clean" and "fast-forwardable" are not the same guarantee.
