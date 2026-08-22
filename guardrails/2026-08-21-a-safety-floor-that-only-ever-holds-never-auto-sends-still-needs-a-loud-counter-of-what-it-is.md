---
title: A safety floor that only ever holds (never auto-sends) still needs a LOUD counter of what it is holding, or it silently becomes a client who was never told
date: 2026-08-21
category: guardrails
tags: [portal, comms, product]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Every single item in a batch of client communications had a prepared reply drafted and queued for
send — and every one of them remained unsent, with the client never actually informed. The
deliberate floor of never auto-sending on the client's behalf had worked exactly as designed and
held every message for human review — but no screen the operator actually looks at day to day
surfaced "you currently have a meaningful number of unsent drafts waiting," so the floor's own
success (nothing was auto-sent) became indistinguishable, from the operator's point of view, from
the work simply not existing yet.

The generalizable rule: any standing floor whose entire design is to HOLD an action rather than
perform it automatically needs an equally prominent, always-visible counter of what it is
currently holding — surfaced on whatever screen the responsible human actually checks regularly —
or the floor quietly converts into a channel that never gets acted on at all. A never-auto-send (or
similarly protective) design without a loud, ambient "here is what's waiting on you" signal is a
half-built safety feature.
