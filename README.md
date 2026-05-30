# strata

> Layers of learning from building a governed agentic engineering org — deposited by the agents, readable by anyone.

This repo is a living record. It mirrors the folder structure of an agentic codebase — `agents/`, `mcp/`, `rag/`, `orchestration/`, etc. — but instead of code, each folder holds pattern notes and learnings.

It starts empty. It fills itself over time via a Claude Code skill (`/deposit`) that drops a structured layer whenever a pattern proves itself, a guardrail saves a session, or a wave of work completes.

## How it works

1. A skill (`/deposit`) generates a properly-labeled entry and commits it.
2. The root workspace config instructs agents to use this skill at natural moments — wave completions, pattern discoveries, guardrail events.
3. Over time the strata build up: a public cross-section of how a governed agentic engineering practice was assembled, layer by layer.

## How to read it

- **[schema.md](schema.md)** — the frontmatter contract every entry follows
- **[agents/](agents/)** — agent architecture: roles, lifecycle, governance
- **[mcp/](mcp/)** — MCP server design and tool patterns
- **[rag/](rag/)** — retrieval-augmented generation approaches
- **[guardrails/](guardrails/)** — enforcement patterns (hard gates vs soft warnings)
- **[orchestration/](orchestration/)** — multi-agent coordination (DAGs, hedging, loops)
- **[evals/](evals/)** — evaluation frameworks (judge models, golden datasets)
- **[infra/](infra/)** — workspace and multi-repo org setup
- **[skills/](skills/)** — Claude Code skill patterns (including `/deposit` itself)
- **[journal/](journal/)** — timestamped wave summaries and surprises

## What this is not

- Not a framework to install (yet — see the journal for the MCP roadmap)
- Not documentation of any specific private system
- No prompts, no client data, no implementation code

## Confidence levels

Every entry declares its confidence honestly:
- `learned` — observed in practice, held up under pressure
- `hypothesis` — plausible reasoning, not yet proven
- `speculation` — interesting idea, no evidence either way

The value of the strata depends on that field being accurate.
