---
title: Prove a sanitizer worked by scrubbing both the raw and the paraphrased text, not just the final output
date: 2026-07-22
category: guardrails
tags: [ip-gate, sanitizer, witness, proofs]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A publication pipeline that paraphrases private material into a public-safe form is only demonstrably safe if the paraphrasing step can be shown to have actually removed something. Running the sanitizer once, against only the final paraphrased text, and reporting that it came back clean proves nothing on its own — a paraphrase step that silently failed to run, or that never touched the sensitive content in the first place, would produce the exact same clean result as a paraphrase step that worked correctly.

The stronger proof is a paired, differential scrub: run the same sanitizer against the original raw source material first, and separately against the paraphrased output, then compare the two results. When the raw pass flags real hits and the paraphrased pass comes back clean, that specific contrast — dirty in, clean out — is the evidence that the paraphrasing step is the thing that removed the sensitive content, rather than an accident of the content never having been sensitive to begin with. A single clean scrub of only the output is consistent with several very different underlying realities, including a sanitizer that was never meaningfully exercised; a before/after pair collapses that ambiguity and is the only version of "the sanitizer worked" that is actually falsifiable.
