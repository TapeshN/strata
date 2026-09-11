---
title: A mechanical text-extraction step can silently drop a source's sub-points, and only a check that reads the actually-published output will catch it
date: 2026-08-31
category: guardrails
tags: [publish-gate, silent-data-loss, quality-vs-safety, automated-summarization]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

An automated pipeline distilling longer written notes into short published summaries worked by pattern-matching one recognized lead-in shape in the source text and extracting whatever followed it. Where a source note's real content lived in several numbered or lettered follow-on points that came after that lead-in but outside the exact shape the extractor recognized, the extractor produced a lead-in sentence with nothing behind it: a complete-looking, well-formatted published entry whose actual content had silently disappeared. The same run showed two smaller symptoms of the same underlying looseness — a formatting artifact bleeding into a machine-readable field, and several numbered lessons reduced to bare fragments with no supporting prose.

An extractor built around one recognized shape for "the important sentence" should either be taught to capture a source's full sub-structure, or should refuse to publish a lead-in whose body it could not find. Publishing a confident, well-formatted, empty entry is worse than publishing nothing, because it reads as finished work while carrying no content. A gate that only checks a candidate entry for leaked secrets or private references is half a gate: "safe to publish" is not the same claim as "worth publishing," and a mechanical extractor's characteristic failure mode is exactly this shape — confident and well-formatted, but empty. Any quality check protecting a publish step should read the text that would actually be published, not the richer source document it was derived from, because those two can diverge silently and the divergence is invisible from the source side alone.
