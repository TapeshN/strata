---
title: Branch and PR naming convention for an agentic workspace
date: 2026-05-30
category: infra
tags: [docs, multi-repo, versioning, release]
confidence: learned
source: private-work
---

Consistent naming across branches, PRs, and commits matters more in an agentic workspace than in a solo project — because multiple agents and sessions are reading the git log to understand state. A PR title that says "updates" is useless when four agents return handbacks at once. A branch name that describes its scope lets the coordinator know at a glance whether two tracks will collide.

The convention that works across a multi-repo, multi-agent org:

**Branches** follow the pattern `<type>/<scope>`. Type matches the kind of work (layer for new content, infra for structure, agents for role definitions, skills for tooling). Scope is a short description of what specifically is changing. This makes `worktree list` output readable without opening each branch.

**PR titles** mirror the branch type and describe what the reader will find, not what the author did. "layer: worktree guard triggers on directory existence" tells a future reader exactly what they are about to merge. "fix worktree bug" does not.

**Commit messages** use conventional commits format: `note(<category>): title` for content deposits, `chore: description` for maintenance, `feat(<scope>): description` for new capabilities. One concern per commit — a deposit commit contains exactly one entry, never two entries bundled together because they came from the same session.

**Why this matters for agents specifically:** agents reading the git log to understand project state rely on commit messages as structured data. A consistent format means a future Fetch or Log agent can parse recent history without needing to read every file. The log becomes queryable, not just browsable.

**Source code maintenance corollary:** the same discipline applies to any repo where agents are committing — not just strata. An agent that commits "various fixes" is generating noise that degrades every future agent's ability to reason about what changed and why.
