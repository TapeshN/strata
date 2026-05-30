---
title: Strata — inception of the self-populating learning journal
date: 2026-05-30
category: journal
tags: [docs, multi-repo, skills, sml, rag]
confidence: learned
source: private-work
---

## What landed

- Public repo created with 9 category folders (agents, mcp, rag, guardrails, orchestration, evals, infra, skills, journal), each with a README stating what belongs, what does not, and the frontmatter reminder
- Root README and schema.md define the entry contract: frontmatter fields, confidence taxonomy, IP rules
- CHANGELOG stub initialized
- `/deposit` skill drafted — wires every session to contribute without manual overhead

## What surprised me

The worktree guard picked up the new repo as a registered primary checkout immediately after the directory was created — before a single file was committed to GitHub. Mechanical enforcement keys on filesystem presence, not upstream registration. The bootstrap window (git init → first push) requires the intentional bypass flag.

The auto-mode classifier blocked every write to the Claude commands directory independently of explicit user approval in conversation. Self-modification gates operate at the tool level; conversational consent does not propagate to them. The correct path is to add an allow rule to settings first, then write the file.

## What I would do differently

- Add the commands-directory write permission to settings before creating a skill that needs it — not after hitting the classifier wall three times
- Name the repo from the start. The rename from the original name to strata was cheap but added an extra bypass-commit to the history

## Docs and org decisions this wave

Strata replaces the scattered memory and handoff approach for learnings that should persist publicly. The mental model: private repos record what happened; strata records what it means and what generalizes. Private repos stay focused on code; strata is the exobrain. It is also the seed corpus for the RAG pipeline — frontmatter fields become embedding metadata, the confidence field weights retrieval results.

## What is next

- Wire the /deposit skill (terminal command ready; needs allow rule in settings first)
- First non-journal deposits: the worktree-guard and classifier patterns documented this wave
- When /deposit is live, dog-food it immediately with the skills entry for the skill itself
- Roadmap: MCP plugin → marketplace after 10+ entries exist
