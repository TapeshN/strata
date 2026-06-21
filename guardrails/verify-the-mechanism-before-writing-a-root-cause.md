---
title: Verify the mechanism before writing a root cause into a record that will outlive you
date: 2026-06-11
category: guardrails
tags: [verify-dont-trust, docs, gating, determinism]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A root cause written into a LEARNINGS entry, an error message, or a handoff document has a reach beyond the session that wrote it. Every future engineer who encounters the same symptom reads the recorded cause and acts on it. If the cause is wrong — plausible but unverified — you have seeded every future debugger with a misleading frame.

In a concrete case, a recorded root cause and a generated error message both cited a duplicate environment variable as the reason a placeholder value was winning. A peer session with a different entry point discovered the actual mechanism: the framework's variable loader was never even reading the file in that path — so a second definition at any line could never have influenced the result. The plausible story was wrong; the diagnostic guidance it generated would have sent every future reader down the wrong path.

The verification step that was missing: before writing a root cause, confirm the proposed mechanism is actually plausible under the real execution path. For environment variable loading: confirm which file the framework loads and in what order. For any system: confirm the thing you say is causing the symptom is actually in the execution path that produces it.

Three discipline points:

- **Correlation is not mechanism.** Two things appearing together (a duplicate definition, an unexpected value) is not proof that one caused the other. Ask: "by what specific mechanism would A produce B?" and verify that mechanism.
- **Error messages carry causal claims.** A message that says "the placeholder won because of a duplicate definition" will be read and believed by the next person who sees it. A message with a wrong root cause misdirects longer than the session that wrote it.
- **Recorded root causes are hypotheses until witnessed.** Tag any mechanism you haven't directly observed as `HYPOTHESIS — verify against the live execution path` rather than encoding it as established fact.
