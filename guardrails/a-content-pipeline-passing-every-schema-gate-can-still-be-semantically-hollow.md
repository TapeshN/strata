---
title: A content-generation pipeline that passes every schema gate can still be semantically hollow
date: 2026-07-19
category: guardrails
tags: [evals, llm-judge, gating, quality]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A pipeline stage that paraphrases raw notes into a structured document format was producing entries that passed every format check — correct frontmatter, correct field types, non-empty body — while several of those bodies simply echoed the entry's own title back as prose, adding no real content. No schema validator catches this, because "non-empty" and "matches the title's topic" are trivially satisfied by an echo.

**The rule:** a human (or a separate, adversarial review step) reading actual output before publish is not ceremonial — it is the only layer that catches format-valid-but-content-empty output. When automating a paraphrase/summarize pipeline, add an explicit check that a body isn't just a near-restatement of its own title, and don't treat "it passed the schema gate" as equivalent to "it says something."
