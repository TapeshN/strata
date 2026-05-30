# agents/

Notes on agent architecture: how to design roles, govern lifecycles, and prevent sprawl.

## What belongs here

- Role definitions and swim-lane boundaries (what an agent class owns vs delegates)
- Lifecycle patterns (proposal → approval → execution → verification → done)
- Subagent governance (when to create a new agent vs use an existing class)
- Context window discipline for long-running agents
- State management and drift recovery

## What doesn't belong here

- Notes on how agents coordinate with each other → `orchestration/`
- Notes on quality gates that agents enforce → `guardrails/`
- Notes on how agents use retrieval → `rag/`

## Frontmatter reminder

```yaml
category: agents
```
