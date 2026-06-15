---
title: A retrieval pipeline must be relevance-gated; indiscriminate injection can harm more than it helps
date: 2026-06-08
category: rag
tags: [rag, evals, judge, cost]
confidence: learned
source: private-work
---

When wiring a retrieval-augmented pipeline (fetch context → inject → decide), build a measurable A/B gate before assuming retrieval helps. In practice, retrieval improves decisions on relevant, uncertain inputs but harms quality on off-topic ones: an unfiltered corpus injects incidentally-overlapping chunks into any prompt that shares common vocabulary, flipping good decisions to bad.

**Calibrate relevance thresholds at production scale, not on fixtures.** A lexical-overlap gate (keyword co-occurrence, character n-grams) that passes cleanly on a small fixture corpus typically fails at real scale: a monoculture corpus (e.g., all engineering-process prose) shares common terms with almost any software prompt, so near-zero similarity scores look meaningful under the fixture distribution but are noise at production scale. Threshold tuning must use a corpus representative of real diversity and volume.

**A semantic pre-check outperforms lexical methods on a monoculture corpus.** When all entries share a genre, cosine similarity converges on a narrow band (e.g., 0.71–0.76) for everything. A lightweight LLM relevance pre-check (classify "does this chunk actually inform this question?") correctly rejects off-topic chunks that lexical filters admit. Once the relevance gate is semantic, the retrieval pipeline can deliver net-positive quality improvement across the full run — including reliable harm-prevention on control inputs.

**The honest bound:** the quality upside from relevant retrieval appears mainly when the model is uncertain about the answer without context. When it is already confident, injection adds noise. A good A/B harness uses deliberate control questions the corpus cannot inform, because these expose the harm case that a relevance-only test set would miss.

**Shared-worktree verifier race:** when multiple adversarial verifiers run against the same checkout, one verifier's mutation test can be observed by another mid-flight. Give each verifier its own isolated checkout, run them serially, or verify read-only against a committed HEAD.

**Cross-repo runtime coupling in tests:** a test that imports or drives a tool from a sibling repo hard-fails in isolated CI where that sibling is absent. The fix is a conditional skip (`skip if dep absent`) that keeps the hermetic behavior assertion unconditional (the fail-open property must be proven in isolation, not skipped entirely). With the dep present the full witness runs; the skip hides nothing from a reader who understands the conditional.
