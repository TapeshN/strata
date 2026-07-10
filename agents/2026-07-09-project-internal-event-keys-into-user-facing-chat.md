---
title: Never let raw internal event keys reach a user-facing chat surface
date: 2026-07-09
category: agents
tags: [chat-projection, event-driven-ui, internal-vs-external-schema, dogfooding, ux-review]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

When a system emits structured internal events (audit-log entries, state-change notifications, webhook payloads) and any of those events are ever rendered in a customer-facing feed — chat, activity timeline, notification center — the rendering layer needs an explicit projection step that maps known event kinds to human-readable copy. Passing internal event objects straight through to the UI, with only a generic "render the message body" path, means any event kind nobody explicitly designed a rendering for shows up as its raw internal identifier (an enum-like key or snake_case field name) instead of a sentence a customer can read.

What happened: a team building a client-facing chat surface discovered, only by manually walking through the live product logged in as a real customer, that a background system event (an internal field-change notification, not something a human typed) had been inserted into the chat feed and rendered as its raw internal key string rather than natural language. Automated tests hadn't caught it because they exercised the human-message path, not the system-event path, and the two share a rendering component with no type-aware branching.

How to apply: any time you have a shared "message" or "activity" data model that mixes human-authored content with system-generated events, do not let both flow through the same renderer with a generic fallback. Build (or audit for) an explicit projector/mapper: known internal event kinds map to curated human copy; anything without a mapping either gets a safe generic sentence or is filtered out of the customer-facing view entirely (and surfaced only in an internal/admin view). Add a test that asserts every event kind the backend can emit has a corresponding entry in the projection table, so a newly added event type fails loudly instead of leaking its internal name into production.
