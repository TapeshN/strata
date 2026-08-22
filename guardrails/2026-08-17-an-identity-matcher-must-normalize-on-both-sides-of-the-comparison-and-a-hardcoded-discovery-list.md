---
title: An identity matcher must normalize on BOTH sides of the comparison, and a hardcoded discovery list repeats the same invisible-new-item trap
date: 2026-08-17
category: guardrails
tags: [import, identity, gate-design]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

An import pipeline's refusal-on-ambiguity logic for matching incoming records to existing ones was
defeated by simple case and whitespace variants — a reviewer reproduced a wrong-record overwrite
this way. The fix required normalizing (lowercasing, trimming) on BOTH the database query that
fetches candidate matches AND the in-memory key used to group and compare them; normalizing only
one side still leaves the other half of the same defect, because a JS-only normalization can never
see a sibling record the query itself failed to return, while a query-only fix still buckets
already-fetched rows separately if the comparison key stays unnormalized. Any matcher deserves this
same question for every normalization step: which HALF of the pipeline does it live in — the fetch
predicate, or the comparison key — and both halves need testing against a deliberately
non-normalized sibling record planted in advance.

Separately, a security-relevant scanning gate maintained a hardcoded list of files or locations to
check, and a newly-added file using the exact vulnerable pattern the gate existed to catch passed
straight through it, simply because the new file was never added to the list. Even after fixing
the list into a broader pattern-based search, one more location was missed because it satisfied the
vulnerable condition indirectly, without literally containing the searched-for text. Any
source-discovery pin that is meant to catch a class of defect should be built to discover its
subjects dynamically in BOTH directions — finding the dangerous pattern wherever it appears, and
confirming every known caller of the safe alternative still fails closed — and should assert that
it actually found its known test subjects, so that a pattern silently matching nothing can never
read as a passing gate.
