---
title: New client-facing work defaults to owned demo-hosting and the client's own tracked workspace, never a metered host or a private session by habit
date: 2026-08-30
category: guardrails
tags: [demo-first, cost-governance, client-onboarding, doctrine-lookup]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Starting a new piece of client-facing work makes it easy to reach for the most familiar path out of habit rather than checking the team's own standing doctrine. One session planned a brand-new client preview on a metered cloud host purely by reflex, when the actual standing rule was to serve early previews from owned infrastructure (an always-on machine plus a tunnel) and reserve metered cloud hosting for an explicit go-live decision. A related miss in the same moment: routing the client-facing record of the work through a private engineering channel instead of the client's own tracked workspace, so the system the client actually sees never got updated even though the work itself happened.

Both mistakes trace to the same cause — the excitement of a new engagement skipped the deliberate lookup of accumulated doctrine that exists specifically to prevent exactly this. A standing "check what we already know before acting on a new prompt" habit only works if it actually runs before the first action, not after someone points out the miss.

For any new client-facing artifact, treat "which context serves this" and "which system carries the client-visible record of this" as two defaults that must be positively overridden, never assumed: the serving default is owned infrastructure, with metered cloud hosting opt-in at go-live; the record default is the client's own tracked workspace, not a private engineering thread. Checking standing doctrine before acting on a new engagement is part of the task, not an optional nicety.
