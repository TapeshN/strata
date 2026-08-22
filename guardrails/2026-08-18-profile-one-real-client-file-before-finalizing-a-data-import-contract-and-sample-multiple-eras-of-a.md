---
title: Profile ONE real client file before finalizing a data-import contract, and sample multiple ERAS of a long-lived client corpus before deriving a taxonomy from it
date: 2026-08-18
category: guardrails
tags: [import, client-grounding, verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A member-data import contract was finalized over several careful iterations, refined against a
detailed guide with dropdowns and validation rules. When the operator then shared the client's
ACTUAL export file, essentially every single row would have been refused by the finished contract:
birth years were universally absent, join dates used two-digit years, role values were
inconsistently capitalized, an organization name was entered as loose free text, some rows carried
data the contract's rules explicitly refused, and many fields carried stray whitespace or
inconsistent casing. The contract had been designed outward from an idealized domain model; real
client data is shaped by years of a completely different prior system's habits. Before an import
contract is considered done, it should be profiled against at least one real client file, counting
actual refusals — and the fix belongs on the importing side (accepting subsets, case-insensitive
values, a first-class "year unknown" state), never in asking the client to reformat their own data.

Separately, deriving a content taxonomy from a long-lived client content corpus by sampling only
the newest entries returned a completely different vocabulary than the corpus's older, structurally
distinct core material — the newest entries were generic and editorial, while the bulk of the
actual subject matter lived in an older, differently-structured era entirely. A single recent
sample of a long-lived corpus is not a representative sample; any taxonomy or contract derived from
a client corpus should be checked against the newest, the oldest, and the middle of that corpus,
and should record which era each observed pattern actually came from.
