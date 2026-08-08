---
title: Type-only imports break the instant a value import is added; an ORM can write JSON-null instead of SQL NULL; a fail-closed gate must stay observable
date: 2026-08-08
category: guardrails
tags: [typescript, database, orm, fail-closed, observability, tooling-gotcha]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A module kept deliberately "portable" — resolvable across multiple runtime targets — by importing its sibling modules as TYPES only stays portable exactly until the first VALUE import is added to it. Under a runtime that strips type annotations at execution time rather than transpiling, type-only imports vanish entirely and impose no resolution requirement, but a value import must resolve for real, using the runtime's own module resolution rules, which may not tolerate an extensionless or otherwise "convenient" import path that worked fine under a bundler. Treat adding the first value import to a previously type-only module as an API-breaking change to that module's runtime contract, not a routine addition.

Some ORMs write a JSON-typed literal null into a JSON/JSONB column by default when a field is omitted, rather than a true SQL NULL — and this is invisible through the ORM's own query layer, since a JSON-null field still "exists" and reads back as a value, while a raw SQL null check on the same column matches nothing. Any schema with optional JSON columns should seed and write them with the ORM's explicit "SQL null" sentinel when that is the intent, and any verification of "is this column empty" should run as raw SQL, not through the ORM.

A fail-closed configuration gate — deny by default when a required setting is unset — is only doing its job if the ONE surface that is supposed to report system status can still explain the closed state in words. It is a common trap for a health or status page to call the same throwing accessor unguarded, turning a deliberately strict security posture into an opaque error on exactly the page that exists to answer "how is this deployment configured." Every fail-closed gate needs at least one authorized reporting surface that catches its own error and renders the closed state as a readable message, not a crash.
