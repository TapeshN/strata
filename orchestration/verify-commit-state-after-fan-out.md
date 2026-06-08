---
title: Verify each track's commit and pull-request state after a fan-out; don't infer from a handback
date: 2026-06-04
category: orchestration
tags: [fan-out, verify-dont-trust, subagents, gating]
confidence: learned
source: private-work
---

After a parallel fan-out, a track whose builder encountered an error near the end may have left work uncommitted and unpushed with no pull request. An error handback, or a missing handback, carries no evidence that a commit or push occurred. Sibling tracks landing cleanly does not imply this track landed.

In a concrete case, a builder hit an overload error at its final step. Its files were complete and tested on disk — but untracked. The handback was the error string. The coordinator found the work by checking git status and then committed, pushed, and opened the pull request.

Prevention: after any fan-out, check each track's actual version-control state independently — committed, pushed, pull request exists. "Work exists on disk" and "work is landed" are distinct claims.
