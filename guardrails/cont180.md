---
title: The strata paraphraser silently drops sub-lessons, and only a judge that reads the PUBLISHED text catches it
date: 2026-08-31
category: guardrails
tags: [strata, publish-gate, silent-data-loss, quality-vs-safety, measure-the-output.]
confidence: learned
source: private-work
---

the extractor must either capture a lesson's full sub-structure or REFUSE to emit a lead-in whose body it could not extract. Publishing a content-free sentence is worse than publishing nothing, because it looks like a finished entry.

a publish gate that only checks IP safety is half a gate — "contains nothing secret" is not "is worth publishing", and a mechanical extractor's failure mode is confident, well-formed, empty output. The judge must read the text that would ACTUALLY be published, not the source it was derived from. Note the near-miss: the queued entry was one keystroke from being marked pass to silence a recurring stop-hook nag; the nag was right that action was owed and wrong about what the action was.
