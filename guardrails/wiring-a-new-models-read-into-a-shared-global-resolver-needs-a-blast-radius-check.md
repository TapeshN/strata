---
title: Wiring a new model's read into a globally-rendered shared resolver turns a missing migration into a whole-product outage
date: 2026-07-21
category: guardrails
tags: [architecture, blast-radius, migrations, reliability]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A small feature gate — deciding whether to show one new navigation item — called a query against a brand-new data model from inside a shared navigation component that renders on literally every page of an application. Had that new model's underlying table not yet existed in a live environment when this code shipped (a plausible sequencing accident with any new-model rollout), the failure mode wouldn't have been "the one new feature is unavailable" — it would have been every single page throwing, because the failing query sits inside a resolver every page depends on.

**The rule:** before wiring a new model's query into any globally-shared resolver (navigation, layout, shell, a site-wide header), explicitly ask "what breaks if this specific query throws?" A feature-local failure and a whole-product outage look identical in the code until you trace exactly how broadly the resolver that hosts the new query is actually depended upon.
