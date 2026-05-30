# guardrails/

Notes on enforcement patterns: what to make unbypassable, what to make configurable, and how to implement gates mechanically.

## What belongs here

- Hard vs soft guardrail distinction (when something must never bypass vs when it can at higher autonomy)
- Gate structure patterns (trigger → checks → decision → record → surface)
- Mechanical enforcement (hooks, pre-commit scripts, CI gates)
- IP boundary enforcement approaches
- Autonomy tier design (L0–L4 patterns)
- What happened when a guardrail was missing vs when one saved the day

## What doesn't belong here

- Notes on evaluation rubrics → `evals/`
- Notes on agent role boundaries → `agents/`

## Frontmatter reminder

```yaml
category: guardrails
```
