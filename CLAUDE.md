# strata — Claude Code session rules

> Public paraphrased-learning journal for TapQuality.ai / tapeshnagarwal.
> Receives deposits via the /deposit and /goodnight skills (automated from the control-plane).
> DO NOT: paste raw LEARNINGS.md entries, include machine paths, client names, blocklist terms, or unpublished prompts.

## What this repo is

Strata is the public face of the engineering learning loop: distilled, paraphrased insights from real
delivery sessions, safe for public consumption. Each entry is a standalone learning — written so it
can be understood without context from the private workspace.

## Deposit protocol

- Deposits arrive via `/goodnight` or `/deposit` from the control plane
- Each is written to a date-organized file (e.g. `2026/06/entry-001.md`)
- Recorded in `agents-inbox/strata-sync.jsonl` at the control-plane level for verifiability
- Gate: blocklist=0, no raw LEARNINGS verbatim, no prompts/configs, no private names

## Session rules

- All work happens in worktrees (the worktree guard applies to the primary checkout)
- PRs are merge commits (not squash) to preserve deposit history
- Branch naming: `deposit/YYYY-MM-DD-N` for deposit branches
- Commit format: `deposit(strata): {short learning title}`
- NEVER commit: .env, machine paths, API keys, client names, raw internal logs

## What SHOULD be in deposits

- General engineering principles (not company-specific)
- Tool/framework quirks with public names (TypeScript, Cypress, Prisma, etc.)
- Process patterns (extract-before-compact, worktree isolation, eval-before-claim)
- Paraphrased without naming the source project or client

## Repo structure

```
2026/
  06/
    entry-001.md
    entry-002.md
README.md
CLAUDE.md (this file)
```

## Cross-references

- Control plane: Automation_Projects/LEARNINGS.md (private, append-only)
- Deposit tracker: agents-inbox/strata-sync.jsonl (private)
- /goodnight skill: runs deposit at end of each session
