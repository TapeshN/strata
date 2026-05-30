# evals/

Notes on evaluation frameworks: how to measure quality for non-deterministic outputs.

## What belongs here

- LLM-as-judge patterns (rubric design, bias avoidance, model separation)
- Golden dataset curation (what makes a good golden case)
- Eval pipeline design (input → judgment → score → ledger)
- Regression detection (when a score drop should block merge)
- Cost and latency as eval dimensions (not afterthoughts)
- Self-optimizing maturity loops (how eval scores feed back into improvement)

## What doesn't belong here

- Notes on mechanical test runners → `infra/`
- Notes on retrieval quality specifically → `rag/`

## Frontmatter reminder

```yaml
category: evals
```
