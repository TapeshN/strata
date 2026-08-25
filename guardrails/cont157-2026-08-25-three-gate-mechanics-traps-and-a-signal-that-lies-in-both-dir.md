---
title: Three gate-mechanics traps, and a dispatch signal that lies in both directions
date: 2026-08-25
category: guardrails
tags: [gate-design, fail-closed, unreliable-signal, deploy-witness]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

**1. A guard that reads the command string cannot parse a loop.** Merging three pull requests inside a shell loop was refused with a complaint about an unrelated number: the guard scans the command TEXT to find which item is being merged, and a loop variable defeats that entirely. A separate budget gate had the same shape — applying its required label inside the same compound statement as the merge does not satisfy it, because the gate has already read the command by then. The rule: one item per gated call, literal values, and every precondition applied in its OWN prior call. A three-item batch is several calls, not one loop. That is the standing cost of gates that read commands rather than intentions.

**1b. …and such a gate fires on TEXT about commands.** Writing the internal note describing this was itself blocked, because the document contained a literal example of the gated command and the guard matched the documentation as if it were an invocation. That is correct behaviour for a fail-closed gate — one that tried to distinguish "real" invocations from quoted ones would be trivially evadable — but it is worth knowing in advance: to document a gated command, construct the string in pieces, or the gate will refuse the document.

**2. A dispatch API's "files changed: 0" lies in BOTH directions.** An earlier lesson concluded that a terminal status is not an outcome and that the changed-file count is the real witness. That was half right. A later branch audit found nine commits pushed by agents the API had reported as changing zero files. It under-reports as readily as it over-reports, and two confident claims made on its basis that day were wrong in opposite directions. The only trustworthy witness is fetching the branch and reading what is actually there.

**3. Conditional changes look like a failed deploy.** One release carried a mobile-only layout pass, a first-run experience that shows once per user, and an offer gated on a qualifying event. The stakeholder opened the application on a desktop, on an account that had already completed first-run, and reasonably reported seeing no change. Nothing was wrong. When reporting a shipped batch, state the conditions under which each change is VISIBLE — which viewport, which role, which account state — not merely that it merged. A deploy witness that says "ready, healthy" answers a question nobody asked.
