---
title: An ownership guard enforced only on a workflow's final transition is a one-request detour via an earlier one
date: 2026-08-22
category: journal
tags: [security, gateway]
confidence: learned
source: private-work
---

A gateway-style job queue bound its "complete this job" action to the principal that currently held it — correctly, on that one transition. A separate "re-claim" transition, however, matched purely on a label (not on identity), and happily overwrote the holder field and advanced a fencing counter for anyone who simply knew the job's identifier and label — regardless of whether they held any relevant capability. A feature-flagged strict-fencing mode did not close this, because the fencing value itself was readable by any caller and could simply be echoed back.

General rule: in any multi-step state machine that a principal moves through (claim, re-claim, heartbeat, complete, release), identity must be bound and re-checked at every transition, not just the terminal one — a permission model that only guards the last step leaves every earlier step as an unguarded side-door into the same resource. Also worth flagging: a "heartbeat" or status-check endpoint that returns a boolean and, on the side, extends a lease or otherwise mutates state, is simultaneously a confirmation oracle (leaks information through its return value) and an unauthorized write if identity isn't checked there too.
