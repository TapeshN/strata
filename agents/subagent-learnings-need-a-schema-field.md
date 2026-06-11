---
title: Subagent learnings need a schema field — absence must be explicit, not silent
date: 2026-06-11
category: agents
tags: [subagents, contracts, lifecycle]
confidence: learned
source: private-work
---

An audit prompted by a simple operator question — "are we capturing what the subagents learn?" — found the answer was: only by luck. Externally dispatched agents had a mechanical capture path (their run results are parsed by a sink), but in-session subagents reported through result schemas that had no learnings field at all. Learning-shaped content rode along in "notes" or "remaining risks" and evaporated unless the coordinator happened to notice and distill it by hand.

The fix is a contract change, not a discipline change: every lane's result schema carries a learnings list, and an end-of-wave coordinator step collects the lanes' learnings into the dated ledger batch. Because the channel lives in the schema, an agent with nothing to report must return an empty list — absence becomes explicit data rather than silence.

Same principle as routing-at-the-producer: the agent that *produced* the insight labels it and carries it home. A learning loop whose intake depends on the coordinator's attention is not a loop; it's a hope.
