---
title: Check a background task's own state before re-dispatching it — a pasted prompt is ambiguous between "FYI" and "please do this"
date: 2026-07-18
category: orchestration
tags: [subagents, autonomy, hitl, idempotency]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When an operator interacts with a system that supports both a clickable background-task queue (spawning its own session per item) AND a live chat interface, pasting the same task description into chat is genuinely ambiguous: it can mean "for your awareness, this is already queued elsewhere" or "please act on this right now." A coordinator that treats every pasted prompt as an instruction to dispatch, without first checking whether that task already exists as a pending or in-progress background item, can end up running the same task twice — two independent builders working the identical task, unaware of each other, converging on redundant or conflicting output.

**The fix is a standing reflex, not a one-off correction:** before dispatching any task that could plausibly already exist as a queued or in-flight background item, probe that queue first. A successful "claim/dismiss" against the queue (meaning nothing was already running) is the green light to dispatch; a response indicating the item was already started means another session already owns it, and the correct action is to NOT dispatch a duplicate — the existing owner's output is what should be reviewed. This turns an ambiguous natural-language signal into a deterministic state check before committing dispatch resources.

**Secondary practice worth keeping regardless:** when a duplicate dispatch does happen despite the check (or before the check exists), name the dispatch after the shared task's tracking identifier in whatever ledger or log records dispatches, so that a twin becomes visually obvious at review/merge time — two entries against the same task ID are trivially spotted, where two differently-named branches or PRs covering the same underlying work are not.
