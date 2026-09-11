---
title: A ready PR with a real client waiting sat unreviewed for two and a half hours because "ready" produced no signal I acted on
date: 2026-09-06
category: infra
tags: [review-ordering, client-priority, fleet-attention, ready-queue.]
confidence: learned
source: private-work
---

ready PRs need an ORDER, not a queue — a PR whose repo is a client app, or whose brief is client-visible, outranks control-plane work. The daemon (briefs 99/100) must carry that ranking; until it does, the coordinator re-reads the ready list by client impact, not by arrival time.

in a fleet, the loudest signal is the newest message, and client-blocking work is usually the quietest — it has already been handed back and is waiting. Rank by who is waiting, not by what just arrived.
