---
title: High-throughput well-gated shipping can still be peripheral; checkpoint on leverage, not just velocity
date: 2026-06-17
category: journal
tags: [loop, multi-repo, docs]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

After a sustained shipping run — eleven pull requests merged, each CI-verified before merge, every gate green — an honest coherence audit found that everything shipped was control-plane tooling: zero revenue impact, zero moat progress. The two strategic priorities stalled, one actively decaying into a merge conflict, while coordinator state accumulated uncommitted.

The trap is structural. An open-ended "keep shipping" directive optimizes throughput. The safest and most verifiable work is rarely the highest-leverage work. Doing it well produces a green dashboard and feels like progress while the strategic needle-movers sit blocked on harder or human-gated steps. A wired-but-starving integration amplifies the illusion — the code exists, the tests pass, but nothing flows.

The reflex to add after a velocity burst is a leverage audit: for each thing shipped, ask whether it moved a stated strategic priority or only improved the machinery around it. Ship control-plane work, but surface the ratio: when control-plane PRs outnumber product PRs by a wide margin, the coordinator is busy but not effective.

Preserving at-risk uncommitted state is time-critical. A seven-day accumulation of uncommitted coordinator documents is one accidental checkout from loss. The moment an audit surfaces that risk, snapshot it before anything else.
