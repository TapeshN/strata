---
title: "The agent-routing grant is written where the tool's cwd resolves, not where the guard reads"
date: 2026-09-12
category: agents
tags: ["agent-routing", "ledger-path", "worktree-vs-primary"]
confidence: learned
source: private-work
---

the grant tool should resolve the ledger through the same `$CLAUDE_PROJECT_DIR` rule the guard uses.
