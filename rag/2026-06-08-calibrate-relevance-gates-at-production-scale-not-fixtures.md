---
title: Calibrate retrieval relevance gates at production scale, not on a tiny fixture corpus
date: 2026-06-08
category: rag
tags: [retrieval-augmented-generation, relevance-gating, evaluation, semantic-search, lexical-overlap, corpus-scale]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

When you add a relevance gate in front of a retrieval-augmented system, validate it against a corpus that matches production scale and topic diversity — not a handful of hand-picked fixture documents. A gate that cleanly separates relevant from irrelevant content on a small, curated test set can fail badly once the real corpus grows, and the failure mode is easy to miss because the offline test still looks green.

What happened: a team built a lexical-overlap relevance gate (require at least N shared terms between a query and a candidate chunk before injecting it as context) and validated it on a two-document fixture corpus, where it worked perfectly. Once wired against the real corpus — over a hundred chunks, all drawn from the same general domain (engineering process notes) — the gate started passing irrelevant chunks through. The reason: with more chunks, off-topic queries have a higher chance of hitting two or more incidental shared words, and a topically uniform (monoculture) corpus means almost any two chunks share vocabulary regardless of actual relevance. Measured end-to-end, the system went net-negative: it correctly helped on genuinely relevant, uncertain questions, but it also actively hurt unrelated questions by injecting misleading context, and the harm outweighed the benefit. Switching the gate from lexical overlap to an actual semantic check (an embedding-similarity model, or a cheap LLM asked "is this relevant?") fixed it — the LLM check correctly rejected off-topic chunks that the lexical method admitted, and the harm on unrelated queries dropped to zero.

How to apply: before shipping any threshold-based filter (relevance gates, dedup, moderation cutoffs), stress-test it against a corpus that's the right order of magnitude and topic mix as production, and include deliberately irrelevant control cases in the evaluation — not just positive examples you expect to pass.
