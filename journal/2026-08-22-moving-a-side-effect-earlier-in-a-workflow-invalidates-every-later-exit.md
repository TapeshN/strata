---
title: Moving a processor side effect earlier in a workflow (to fix its timing) silently invalidates every later exit path
date: 2026-08-22
category: journal
tags: [money, billing, state-machines]
confidence: learned
source: private-work
---

A pricing workflow moved its payment-processor price swap from a later "apply" step to the earlier "approval" step, correctly fixing an invoice-timing bug. Nothing else in the workflow was re-derived for that change: the cancel path still only cleared local database state, so an approved-then-cancelled batch left the payment processor billing every affected customer at the new (now-cancelled) price going forward, with no compensating action anywhere. A separate audit event existed that, in principle, recorded this exact desync — but nothing in the system ever read it, so it functioned as write-only logging, not monitoring.

General rule: when a side effect against an external system of record moves earlier in a workflow to fix a timing bug, every later exit from that workflow (cancel, retry, re-approve, timeout) needs to be re-derived and given its own compensating action with its own test — the side effect no longer happens at the point those exits were originally designed around. And an audit/log event with no consumer reading it isn't monitoring; before trusting that "we log it so we'd notice," grep for an actual reader of that event.
