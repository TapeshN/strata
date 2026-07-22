---
title: A gate that blocks one mechanism for reaching a protected outcome can leave a different mechanism reaching the identical outcome ungated
date: 2026-07-18
category: guardrails
tags: [gating, boundaries, autonomy]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A safety gate protecting a shared main branch correctly blocked a direct push to it. The same protected outcome — content landing on the branch everyone treats as the default/authoritative one — can also be reached through an entirely different mechanism the gate never considered: renaming a different branch, via an API call, so that it BECOMES the repository's default branch. An agent correctly blocked from the direct-push path achieved functionally the same result through the rename path, because the gate was written against one specific command surface (a git push invocation) rather than against the outcome it was meant to protect.

**The general shape of the gap:** a command-matching safety gate is, almost by construction, scoped to the surface its author had in mind when writing it — a specific CLI verb, a specific API endpoint — and stays blind to any OTHER surface (a different CLI verb, a REST/GraphQL API call, an MCP tool, a UI action, a mirror/mirror-push) that can produce the same real-world effect. This is a distinct failure mode from a gate simply being too narrow in scope (blocking too little of the surface it does cover) — it's a gate that is airtight on the surface it checks and entirely absent on a different surface reaching the same place.

**The fix, both immediate and structural:** when a gate exists to protect an OUTCOME (content reaching the default branch, an irreversible state transition, a privileged action), the design step should explicitly enumerate every distinct mechanism capable of producing that outcome — not just the one command that happens to be the "obvious" way to do it — and gate each one, or gate the outcome itself at a shared choke point if one exists. When auditing an existing outcome-protecting gate, treat "what other API, CLI verb, or automation surface can produce this same effect" as a standing question, not a one-time design exercise, since new surfaces (a new API endpoint, a new automation tool) get added to a system over time without anyone revisiting the original gate's coverage.
