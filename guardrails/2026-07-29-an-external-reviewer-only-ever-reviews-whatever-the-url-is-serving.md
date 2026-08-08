---
title: An external reviewer only ever reviews whatever the URL is serving right now
date: 2026-07-29
category: guardrails
tags: [release, gating, contracts]
confidence: learned
source: private-work
implementation_target: agent-guardrails
efficacy: decorative
---

An external review request went out against a live preview while the environment behind that URL still reflected an older build. The reviewer's findings mixed genuinely new problems with items that had already been fixed on a newer, unpublished revision — and the reviewer had no way to know which was which, because all it can ever evaluate is the artifact currently being served.

The generalizable rule: before asking any external reviewer — a person, a separate agent, an automated audit — to evaluate a deployed artifact, first confirm what is actually being served right now. A cheap content marker (a build stamp, a version string, a distinguishing detail unique to the newest revision) is enough to prove the artifact matches the code under review. Only request the review after that confirmation; otherwise the review is contaminated by a prior state and its output cannot be trusted at face value.
