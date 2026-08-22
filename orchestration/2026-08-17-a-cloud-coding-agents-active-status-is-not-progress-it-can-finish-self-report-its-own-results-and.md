---
title: A cloud coding agent's "active" status is not progress — it can finish, self-report its own results, and then zombie for hours
date: 2026-08-17
category: orchestration
tags: [dispatch, false-green, durable-execution]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A cloud-hosted coding agent was reported as "active" for roughly twelve hours straight, prompting
concern that the dispatch had hung. In fact the agent had pushed its final commits — a complete,
sizeable deliverable with genuine self-reported test and type-check results in its pull-request
description — within the first few minutes, then simply never transitioned its own status field
out of "active" for the remaining ten-plus hours. A completed cloud agent can leak "active"
indefinitely; the status field itself is not a reliable signal.

The fix: judge a long-seeming cloud dispatch by the branch's LAST-COMMIT timestamp and the pull
request's own body, never by the agent-status field or by elapsed "active" time. A long-running
"active" status paired with a last commit from minutes into the run means a finished-then-zombied
agent, not an in-progress build — route it straight to review. (Deliberately terminating a zombied
agent is itself a destructive-class action best left to a human, but leaving it idle costs nothing.)
