---
title: A liveness check is not an authority check for a shared coordination lock
date: 2026-07-10
category: guardrails
tags: [coordinator-lock, liveness-vs-authority, autonomy, hitl, boundaries]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A shared coordination role protected only by a process-liveness check ("is the holder's process still alive") can be silently seized by a session that is technically alive but structurally unable to act as coordinator — for example, a background or auxiliary-mode session that has no channel to ask a human for input. First-boot-wins plus a liveness probe is not a claim policy: whichever process starts first and stays alive keeps the role indefinitely, even if a fully-capable session boots later and needs it.

The fix is to add an authority discriminator on top of liveness: before auto-claiming an unheld role, a candidate checks whether it is actually equipped to hold it (does it have an interactive/approval channel, is it running in a mode that permits taking this responsibility), and refuses the claim rather than silently taking over when it isn't. When a refusal happens, it should surface the current holder's identity (what kind of session it is, how long it's been running, whether it looks capable) so a human or a later session can judge whether a takeover is warranted — and any deliberate takeover should be an explicit, logged action, not an emergent race outcome.

The general rule: for any single-owner coordination resource, "is it alive" answers a different question than "should it be the owner" — a claim/lock mechanism needs both, and the second one is easy to omit until the wrong kind of process wins the race.
