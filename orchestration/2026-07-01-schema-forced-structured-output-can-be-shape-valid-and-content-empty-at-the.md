---
title: Schema-forced structured output can be shape-valid and content-empty at the same time
date: 2026-07-01
category: orchestration
tags: [structured-output, evals, gating, subagents]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

In a large fan-out of parallel agents each required to return findings in a JSON-schema-forced format, a handful of them returned outputs that were fully schema-valid — every required key present, every enum satisfied — while containing essentially no content: single-character or placeholder-word field values that technically satisfy required-string constraints. The schema validated shape (keys present, types correct, enums respected), not substance (no minimum length, no content sanity floor), so degenerate output sailed straight through.

The likely mechanism: a model asked to satisfy a long, rigid schema under a long context can degenerate toward the minimal output that still parses, especially under retry pressure, and a harness that accepts the first parseable response has no signal that the content is hollow. This is the general pattern of a gate that checks the container, not the thing inside it — a schema is a shape gate, not a quality gate.

The practical fix has three parts: add a cheap post-hoc sanity check after any schema-forced parallel call — reject or re-run any result whose serialized length falls under a threshold, or whose content matches an obviously-placeholder pattern; add minimum-length constraints to load-bearing string fields directly in the schema; and for prose-heavy deliverables (reports, audits, narrative findings), consider that a plain-markdown response without a forced schema is often more reliable than a schema-constrained one — reserve strict schemas for genuinely tabular or enum-driven payloads where shape truly is the whole contract.
