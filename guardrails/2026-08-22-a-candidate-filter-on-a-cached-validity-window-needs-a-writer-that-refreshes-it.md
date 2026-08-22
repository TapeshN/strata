---
title: A candidate filter on a locally-cached validity window is only as true as the writer that refreshes it
date: 2026-08-22
category: guardrails
tags: [billing, integrations]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A batch process selected records to act on using a locally-stored "expires at" field, filtered to only the currently-valid ones. Nothing in the system rolled that field forward when the underlying subscription renewed through the payment processor — there was no handler for the recurring-payment webhook that would extend it. The result: exactly the population billed automatically and recurring every period — the group the filter was meant to include — was the group the batch process silently never touched, because their local validity field had gone stale the moment the first renewal happened outside the app's own write path.

General rule: before trusting a locally-stored "active"/"valid until" filter to select a population, find the specific writer responsible for keeping that field synchronized with the external system of record (a payment processor, an upstream API, another service) — and check that the writer actually fires for every event that should refresh it, not only for the event that originally created the record.
