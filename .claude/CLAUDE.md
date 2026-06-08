# strata — agent notebook

> This file is the configuration primitive for the strata workspace.
> It defines the agents that maintain this journal, their roles, and the rules they share.
> Think of it as the governance layer for a system where agents — not humans — do most of the writing.

---

## What strata is

A living public journal of learnings from building a governed agentic engineering org.
Folder structure mirrors a real agentic codebase. Content is patterns and observations, not code.
Every entry follows the frontmatter contract in `schema.md`.

---

## Agent roster

Four agents maintain this journal. Each owns a distinct part of the cycle.

| Agent | Role | File |
|---|---|---|
| **Log** | Journalist — captures and deposits learnings | `.claude/agents/log.md` |
| **Build** | Architect — extends structure, schema, categories | `.claude/agents/build.md` |
| **Check** | Auditor — validates entries, enforces IP gate | `.claude/agents/check.md` |
| **Fetch** | Librarian — retrieves and surfaces relevant patterns | `.claude/agents/fetch.md` |

---

## Shared rules (every agent follows these)

**IP contract — non-negotiable:**
- No quoted prompt text
- No client or entity names (use "a client" / "an entity")
- No internal system IDs
- No runnable code — prose, pseudocode, and ASCII diagrams only

**Confidence is the honesty field.** Every deposit declares one of:
- `learned` — observed in practice, held under pressure
- `hypothesis` — plausible reasoning, not yet field-tested
- `speculation` — interesting idea, no evidence either way

**One concern per commit.** A deposit commit contains exactly one entry.
Structure commits (schema, README, agent definitions) are separate from content commits.

**Branch and PR naming:**

| Work type | Branch | PR title |
|---|---|---|
| New entries | `layer/<category>` | `layer: <what was deposited>` |
| Schema / structure | `infra/<what>` | `infra: <what changed>` |
| Agent definitions | `agents/<what>` | `agents: define <name>` |
| Skills / tooling | `skills/<what>` | `skills: <name>` |

**Commit format:** `note(<category>): title` for entries · `chore: description` for structure · `feat(<scope>): description` for new capabilities.

---

## Autonomy tiers

Agents operating in this workspace follow a simple two-tier model:

| Tier | What it means |
|---|---|
| **Read** | Fetch and Check operate freely — no approval needed for reads or reports |
| **Write** | Log and Build require a human to merge the PR — never auto-merge to main |

Main branch is protected. All writes land via PR. Draft PRs are acceptable for work-in-progress deposits.

---

## The deposit cycle

```
observation or event
      ↓
  Log Agent drafts entry (frontmatter + prose)
      ↓
  Check Agent validates (schema + IP gate)
      ↓
  commit: note(<category>): title
      ↓
  PR opened → human reviews → merge
      ↓
  entry lives in strata, publicly readable
```

The cycle is intentionally slow. A learning that hasn't been paraphrased carefully enough to pass the IP gate isn't ready to be public yet.

---

## Implementation status

The cycle above is the **design contract** — the intended architecture. The current depositor is **simpler than the roster implies**: a deterministic publish step approximates Log's classify + paraphrase and Check's schema/IP gate in code, then opens the draft PR. The four agents define the intended roles and IP discipline; wiring them in as live subagents — and adding Fetch's retrieval arc so the journal feeds *back* into decisions — is still in progress.

Until then, read the roster as the **spec** and this note as the honest **current state**. (Confidence: `learned` — that the gap between a *defined* agent and a *wired* one is real, and worth saying out loud, is itself one of the patterns this journal exists to record.)
