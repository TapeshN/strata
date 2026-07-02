---
title: A task brief written for a named agent persona must be checked against that persona's own standing floors before it is issued, not after
date: 2026-07-02
category: agents
tags: [roles, autonomy, contracts]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A coordinator wrote a task brief for an agent whose own role definition carried a hard, standing floor forbidding a specific command class (in this case, anything that would bootstrap or spend against a metered API credential, since that agent was meant to run entirely on a flat-rate plan). The brief itself instructed the agent to run exactly that forbidden command, because the coordinator had not re-checked the target persona's floor before writing the instruction — it assumed the command was safe based on its name (see the sibling "safety-named flag" learning).

The agent caught the conflict, self-corrected, and reported the deviation honestly rather than silently complying or silently refusing without explanation.

The generalizable fix: when briefing any named persona with its own standing floors (a role definition, a guardrail set, a contract), the brief inherits the persona's floors — never the other way around. Before issuing an instruction, check whether it falls inside a floor that persona is defined to never cross. And treat an agent's honest, well-explained deviation from a flawed instruction as the system working correctly — the fix belongs in the instruction or the underlying tool, not in silently overriding the agent's own judgment next time.
