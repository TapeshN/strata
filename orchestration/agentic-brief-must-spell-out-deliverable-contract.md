---
title: An agentic brief that softly requests a PR and a report gets neither; spell out the deliverable contract step by step
date: 2026-06-22
category: orchestration
tags: [multi-agent, contracts, interfaces, loop]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A dispatch brief that says "open a PR when done" or "emit a learning report" produces those artifacts in roughly zero cases out of many. Agents complete the technical task and stop. The soft instruction is ignored not because the agent is malicious but because the deliverable contract competes with the primary task and loses.

A brief that works spells out the contract as sequenced steps with explicit verifiable outputs:

- Name the branch the PR must be opened on.
- State the commit prefix and message format.
- Require the PR to be opened before the run is considered done — name the command or action.
- If a structured output is required (a JSON report, a learning record), include its exact schema inline and state it must appear as the final message.

Confirming the contract was honored requires reading the remote, not trusting the agent's terminal message. A PR URL that the agent "should have opened" needs to be confirmed by listing open PRs on the remote; a learning record needs to be confirmed by reading the file it was supposed to write.

A related trap: the persistence step may only be wired into one execution path. If a second code path produces the same artifact (direct execution vs. routed execution), the persistence write that lives only on the routed path silently skips whenever the direct path is used. The fix is to move the persistence to the shared seam that every path passes through, and make it idempotent so double-execution does not duplicate records.
