---
title: A captured spec that never becomes a claimable task ages out silently against newer priorities
date: 2026-07-19
category: orchestration
tags: [coordinator, planning, prioritization, backlog]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A written specification captured from a genuine gap — a UI reorganization plan, an interface redesign, self-tagged as needing follow-up — sat unpicked for weeks behind a queue of newer, more urgent work, even though it had already been through the effort of being written down. Writing a spec down is necessary but not sufficient; without a claimable identifier on a live backlog, it silently loses every ranking comparison to whatever was captured more recently.

**The rule:** a spec captured from any kind of gap analysis must become a claimable backlog item, with an ID, at the moment it's captured — not just a file sitting in a docs folder. And because even a properly-ID'd item can still age out unclaimed, a periodic re-orientation pass over the backlog should explicitly surface anything that's aged past some threshold without being picked up, so it doesn't lose by default to whatever is merely newer.
