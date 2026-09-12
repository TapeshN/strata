---
title: "I sent an agent to audit a file that was empty, because control-plane state lives in the PRIMARY checkout and I gave it the worktree"
date: 2026-09-06
category: agents
tags: ["primary-vs-worktree-state", "agent-dispatch-paths", "empty-file-reads-as-done", "judge-must-record", "strata"]
confidence: learned
source: private-work
---

any control-plane STATE file (queues, ledgers, watch markers) is primary-checkout state; only the tracked documents are worktree state. When dispatching an agent that touches control-plane state, resolve the primary root explicitly (`git worktree list --porcelain | awk '/^worktree /{print $2; exit}'`) and pass BOTH roots with a sentence saying which is which.

the tell is a queue/ledger that reads as empty while a hook insists it is not. Believe the hook and check the other root before concluding the work is done — an empty file is indistinguishable from a finished one, and an agent given the empty one reports success.
