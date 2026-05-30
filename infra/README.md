# infra/

Notes on workspace organization: multi-repo layout, worktree isolation, parallel session coordination, and docs structure.

## What belongs here

- Multi-repo org patterns (when to split vs keep together)
- Worktree isolation for parallel agent sessions (why, how, tradeoffs)
- Session warm-start protocols (what every agent reads before working)
- Docs organization (what worked, what became clutter)
- Secrets management and IP boundary enforcement at the infra layer
- Hook patterns (SessionStart, PreToolUse, PostToolUse)

## What doesn't belong here

- Notes on MCP server setup → `mcp/`
- Notes on CI/CD pipelines for specific repos → those repos' docs

## Frontmatter reminder

```yaml
category: infra
```
