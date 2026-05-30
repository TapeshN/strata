# Entry Schema

Every `.md` file in this repo (except `README.md`, `CHANGELOG.md`, and `schema.md` itself) must begin with this frontmatter block.

```yaml
---
title: Short, plain-English title
date: YYYY-MM-DD
category: agents | mcp | rag | guardrails | orchestration | evals | infra | skills | journal
tags: []          # pick from the taxonomy below
confidence: learned | hypothesis | speculation
source: private-work | first-principles | reading | conversation
---
```

## Field definitions

**`confidence`** — the honesty field. Be accurate.
- `learned` — I ran this, observed the outcome, and it held up
- `hypothesis` — plausible reasoning, but I haven't proven it in practice yet
- `speculation` — interesting idea, no evidence either way

**`source`** — where the insight came from.
- `private-work` — distilled from real project experience (IP-clean, no proprietary details)
- `first-principles` — derived by reasoning from known constraints
- `reading` — from a paper, post, or doc
- `conversation` — from a discussion, pair session, or review

## Tag taxonomy

Use one or more. New tags are fine — add them here when you coin one.

```
# Scale / performance
cost, latency, tokens, throughput, cache

# Architecture
layering, isolation, boundaries, contracts, interfaces

# Agent behavior
context-window, hitl, autonomy, subagents, roles, lifecycle

# Quality / correctness
determinism, idempotency, reproducibility, evals, golden-sets, judge

# Workflow
gating, preflight, rollback, release, versioning, ci

# Organizational
docs, multi-repo, worktree, parallel-sessions, ip-boundary

# Patterns
dag, hedging, rag, sml, loop, proofs
```

## IP safety rules

Every entry must pass this check before committing:
- No prompts (describe shape, not text)
- No client or entity names (use "an entity" / "a client")
- No internal IDs (no GL-*, NQ-*, ORCH-* etc.)
- No implementation code (prose, pseudocode, diagrams only)
- Derivable from first principles by any thoughtful AI engineer

These are enforced by grepping staged files against the workspace IP block-list.
