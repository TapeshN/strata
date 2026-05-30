# orchestration/

Notes on multi-agent coordination: how to sequence, parallelize, gate, and recover across agent boundaries.

## What belongs here

- DAG orchestration patterns (dependency graphs, topological scheduling)
- Hedging strategies (race N models, best-of-N, learned routing)
- Parallel vs serial execution tradeoffs
- Context hand-off between agents (what to pass, what to rebuild)
- Loop and continuous operation patterns
- Failure recovery and retry discipline
- HITL (human-in-the-loop) gate placement

## What doesn't belong here

- Notes on individual agent design → `agents/`
- Notes on the mechanical gate implementation → `guardrails/`

## Frontmatter reminder

```yaml
category: orchestration
```
