---
title: Land the design system first; fan out per-surface agents that consume, not redefine
date: 2026-06-22
category: orchestration
tags: [multi-agent, layering, dag, isolation, contracts]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When a redesign spans many surfaces simultaneously, the natural move is to fan out one agent per surface. That move reliably fails: each agent independently guesses the shared tokens, header components, and global stylesheets, so they collide on those files at merge time and produce an incoherent result — a premium surface bolted onto untouched inner pages reads worse than no redesign at all.

The pattern that works is sequential at the design-system layer, parallel at the surface layer:

1. Land a foundation commit first: shared tokens, global stylesheet, header, footer, card skeleton. Merge it before any surface agent starts.
2. Fan out per-surface agents off that merged foundation. Each agent's brief must include an explicit "consume, do not redefine" clause naming the shared files they must not touch. Prefer new scoped components over editing shared ones.
3. Merge surfaces one at a time, rebasing between each. Never race two agents that touch the same page.

The foundation-first ordering eliminates shared-file conflicts entirely, because by the time surface agents start, the hotspot files are already settled on main.

Budget a verification pass per surface: any global-token change regresses accessibility contrast across every surface that inherits it, and existing behavioral tests (navigation targets, structural invariants) break silently. The fix pass belongs in the same work scope as the redesign, not as a surprise after merge.
