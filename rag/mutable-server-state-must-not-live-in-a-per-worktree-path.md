---
title: Mutable server state must not live in a per-worktree path
date: 2026-06-05
category: rag
tags: [worktree, isolation, rag, mcp]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

An MCP RAG server that resolved its vector store to a path next to its own source file silently booted an empty corpus in every new worktree. The populated store lived only in the primary checkout; each worktree's server launched fresh with nothing to retrieve. Every query returned zero results even though the session startup hook reported the corpus as current.

The root is a category error: *mutable runtime state* (a populated index that grows over time) was stored as if it were *source code* (a per-tree artifact that travels with a checkout). Worktree isolation is the right default for source; it is exactly wrong for a shared long-lived store.

Two fixes compound to close the class:

- **Path**: store the index at a stable, tree-independent location — a user-home cache directory that every worktree and every server instance share. An env-override for the path is useful for tests; the default must not be relative to `__file__`.
- **Restart awareness**: a server that caches the store at launch will not see ingest runs that happen mid-session. Treat store or config changes as restart-required and document that contract explicitly.

The broader principle is the same one that motivates gitignoring telemetry and lock files: if the content is produced at runtime and consumed across sessions, it belongs in a durable shared location, not in a version-controlled tree. Worktree isolation is a feature for source; applied to mutable state it looks like data loss.
