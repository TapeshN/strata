---
title: Auto-union merge resolution is safe ONLY for append-shaped files — code demands semantic resolution
date: 2026-06-11
category: infra
tags: [merge, automation, gating]
confidence: learned
source: private-work
---

A stacked-merge chain auto-resolved conflicts with a regex "keep both sides" union. The changelog unioned fine. The code files did not: both sides' registrations were concatenated (duplicate blocks → CI red), and worse, the union *interleaved try/finally blocks from the two branches and stripped a finally clause* — a SyntaxError that surfaced only at import time.

The rule that came out of it, now absolute:

- **Auto-union is allowed only for known append-shaped files**: changelog "unreleased" sections, JSONL ledgers, and similar append-only formats where both sides' lines are independently valid.
- **ANY conflict in a code file stops the chain for semantic resolution** — by an agent reading both parents, or a human. The repair discipline: per-block comparison against BOTH parent versions, restoring atomic structures (functions, try/finally, registration blocks) whole, each feature surviving exactly once.
- Regex-union on code is *structurally* unsafe, not merely semantically — text-level "keep both" can split syntax constructs that are atomic at the language level. No amount of cleverness in the regex fixes this; the failure is categorical.
- If you already have a canonical merge tool that stops loudly on conflict, inline helpers must match its behavior — never out-clever the conservative path.
