---
title: A relevance gate calibrated on a small fixture corpus overfits and fails at production scale
date: 2026-06-08
category: rag
tags: [rag, evals, relevance, calibration, ab-testing, corpus-scale, retrieval]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

An evaluation meter that includes a control arm — questions the corpus cannot inform — is required to prove that context injection actually helps. Without a control group, a retrieval pipeline that injects irrelevant context will appear to improve results on relevant questions while silently degrading unrelated ones.

A lexical-overlap relevance gate calibrated on a small, two-lesson fixture corpus separated relevant from off-topic questions cleanly in offline tests. When deployed against a real production corpus of over 160 chunks, the gate failed: more chunks meant off-topic prompts found enough incidental overlapping words to exceed the threshold. A monoculture corpus — where all content shares a vocabulary domain — makes lexical overlap a weak relevance signal because common words create spurious matches.

Three generalizable lessons:

First, calibrate relevance thresholds against a corpus that is representative of production scale and diversity, not a fixture set. A gate that passes on two examples and fails on 160 is not a gate — it is a local approximation that happens to work on the examples it was designed against.

Second, a lexical signal cannot provide topical relevance on a monoculture corpus. When all content shares a common vocabulary, a character-n-gram or term-overlap score distributes too uniformly to discriminate. Semantic embeddings or a trained classifier are required.

Third, an A/B experiment must include deliberate control questions the corpus cannot help answer. Without a control arm, a net-negative pipeline reads as a net-positive, because the relevant-question improvement masks the irrelevant-question degradation. The control arm is what falsifies "this helps."
