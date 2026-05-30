# mcp/

Notes on MCP (Model Context Protocol) server design and tool patterns.

## What belongs here

- Tool schema design (naming, input/output contracts, idempotency)
- When to build an MCP tool vs a CLI vs a Claude Code skill
- Server lifecycle (startup, auth, session management)
- Patterns for exposing existing CLI tools as MCP tools
- Cost and latency implications of tool round-trips

## What doesn't belong here

- Notes on skills that call MCP tools → `skills/`
- Notes on RAG tools specifically → `rag/`

## Frontmatter reminder

```yaml
category: mcp
```
