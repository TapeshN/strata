---
title: A gate satisfiable by a comment is worse than no gate — parse the structure, not the text
date: 2026-06-03
category: guardrails
tags: [gating, verify-dont-trust, ci, preflight]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Two wiring-check scripts verified that safety hooks were registered in the configuration. Both read green. Both were wrong — one for each direction.

The first script did a text search of the configuration file for the hook's name. The hook's name appeared in a comment field inside an otherwise-empty hooks block. A string match is satisfied by any occurrence of the string, including documentation of an intent that was never executed. The hook was "present" in text and absent in the live command table.

The second script checked for the hook entry's structural location but did not verify that the command path resolved to a real executable. The path was registered; the file it pointed to did not exist in the relevant environment.

Both failures share the same root: the verification measured a textual property of the file rather than the runtime property the gate is supposed to protect. The only check that establishes a gate works is triggering it — setting up a condition the gate should catch and confirming it fires.

Rules that close both failure modes:

- **Parse the structure, not the text.** A hook registration check must walk the actual command table in the configuration — the live `hooks.<event>[].hooks[].command` entries — not search for a string anywhere in the file.
- **Verify resolution, not just presence.** The registered path must resolve to a real executable in the environment where it will run.
- **A negative probe is required.** Ship a failure-trigger test that proves the gate fires on the bad input. A gate that has only ever been observed passing has never been verified to be a gate.

The compounding cost: a gate that reads green while doing nothing provides *false* confidence — it is strictly worse than no gate, because it eliminates the action that the absence of a gate would have prompted.
