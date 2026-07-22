---
title: An enumerated "survivors" list in a spec functions as a deletion list for everything absent from it
date: 2026-07-22
category: agents
tags: [spec-writing, dispatch, agent-literalism]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A dispatch specification for reorganizing a navigation surface named which destinations should survive into a secondary/overflow area. One legitimate destination was simply omitted from that survivors list — not deliberately removed, just not mentioned — and the agent executing the spec followed the list exactly as written, correctly dropping the omitted destination from the navigation entirely. The agent did not misbehave; the specification did, by being ambiguous about what "not listed" was supposed to mean.

**The rule:** when writing a spec that enumerates which items should be kept, treated, or moved, any item genuinely absent from that enumeration will be read by a literal executor as "not kept" — either explicitly enumerate what should be REMOVED as its own list, or state explicitly that anything unlisted is retained unchanged. Don't rely on an executor to infer benign omission from a "keep list" alone.
