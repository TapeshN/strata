---
title: Read the existing roster before claiming a capability gap
date: 2026-05-31
category: agents
tags: [roles, architecture, lifecycle, governance]
confidence: learned
source: private-work
---

In a design discussion mapping a multi-stage loop onto an existing agent roster, the coordinator presented one stage as a *gap* and proposed building a new agent for it — without noticing that an existing agent already covered the adjacent role. The miss came from reasoning off a one-line project map (which lists agent *names*) instead of reading the agent *definitions* (which describe their *roles*). The proposed new agent turned out to be a real missing piece — but *upstream* of the existing one, a producer that feeds the existing aggregator, not a redundant parallel system.

General lesson: knowing an agent's name is not knowing its role. Before asserting a capability gap or proposing a new agent or tool, read the definitions of what already exists. "Verify, don't claim" applies to architecture claims as much as to test results — a proposed gap must be checked against the actual roster first.
