---
title: A reasoning-style local language model can silently break a low-latency streaming chat that reads only the direct-answer field
date: 2026-07-06
category: agents
tags: [local-llm, streaming-chat, model-selection, cost-latency-eval]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

When comparing candidate local models for a low-latency, streaming client-facing chat, a head-to-head test surfaced a failure mode that a one-shot completion test would never catch. A plain instruct model answered directly and quickly. Two reasoning-style ("thinking") models of similar or larger size returned an empty visible reply on the same prompt and token budget: they emitted a long internal reasoning block into a separate field first, consuming the entire output-token budget before producing any user-visible text. A streaming integration that only forwards the direct-answer field's deltas to the browser will show the user a long "typing" indicator followed by silence or a truncated cutoff, because the model spent its whole budget on reasoning nobody sees.

The general lesson: model selection for a latency-sensitive streaming surface must exclude reasoning/thinking-mode models by default, reserving them for latency-tolerant surfaces where a longer wait is acceptable and their reasoning quality is worth it. Any model-governance or selection layer should flag or refuse a thinking-mode model for a client-facing streaming tier. Just as important, a candidate model must be verified on the actual production code path it will run through — the specific field the integration reads and the actual token budget in play — rather than validated only through a generic one-shot prompt-and-response test that doesn't exercise streaming or budget exhaustion.
