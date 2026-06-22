---
title: A hook or doc that describes a scheduled action is not evidence the schedule exists
date: 2026-06-10
category: guardrails
tags: [scheduling, verify-dont-trust, autonomy, lifecycle]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A stop hook fired every turn for hours describing a pending daily scheduled action: the message promised that learnings would be staged automatically at a fixed time. An audit found no corresponding scheduler entry in any scheduler the system used, and the scheduled script was unable to complete its task in that environment regardless — a dependency it needed was absent at the relevant execution context.

The hook was narrating a design intention, not reporting installed state. Every time it fired, an operator could reasonably believe the automation was live. It was not.

The class of error: a hook, README, or comment that *describes* a future state (a schedule that will be installed, a feature that will be added, a gate that should be wired) conflates intention with fact. The document is a hypothesis; the installed state is the fact.

Two rules follow:

- **Claims about scheduled or automated behavior must be derived from the scheduler's state**, not from a description in a prompt. The correct form is: list the scheduled tasks actually registered, then report on them. A hook that cannot query the scheduler should say so honestly rather than forwarding the description.
- **When you arm a scheduled action, verify the arm independently.** "The script is there and the schedule text was dropped in" is not evidence the schedule will run. Evidence is: the task appears in the scheduler's task list, the required credentials are present at the scheduled execution context, and a dry-run at the intended time fires cleanly.

This is the same principle that makes "gates that are never run are fiction" extend to "schedules that are never verified are fiction." The test is always the same: does the described thing actually happen?
