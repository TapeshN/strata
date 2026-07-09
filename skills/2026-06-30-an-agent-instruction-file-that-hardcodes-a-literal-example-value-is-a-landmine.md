---
title: An agent instruction file that hardcodes a literal example value for an output path is a landmine for every future run
date: 2026-06-30
category: skills
tags: [docs, lifecycle]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

An agent's own definition file instructed it to write its output to a path containing a specific, concrete date — written at the time the definition was authored, intended only as an illustration of the naming pattern. Every subsequent run of that agent, on every later date, dutifully followed the literal instruction and wrote to the same hardcoded, now-stale path, silently overwriting whatever had been written there by the previous run. On the run that surfaced this, the output happened to be non-empty, well-formed, and worth keeping — it simply landed at a path that was ten runs old, and nothing in the agent's own protocol checked for or avoided the collision.

The root cause is a common authoring mistake: encoding a single concrete example where the intent was to describe a pattern. Nothing distinguishes "this is the literal string to use" from "this is what the format has looked like before" in the instruction text itself, so the agent has no way to know a value should be recomputed rather than copied.

The fix is twofold: any instruction that shows an example output path or filename must explicitly mark it as illustrative and specify that the actual value should be computed fresh at run time (for example, "today's date," not a hardcoded string) — and the agent's protocol should include an explicit check for an existing file at the path it is about to write, before writing. The generalizable audit: any agent definition that shows "the format looks like X" via a concrete, dated, or otherwise timestamped example is worth auditing for this exact landmine.
