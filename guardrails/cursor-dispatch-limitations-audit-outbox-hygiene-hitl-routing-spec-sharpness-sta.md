---
title: Five dispatch hygiene gates that prevent double-dispatch, stale-premise fixes, and silent HITL failures
date: 2026-06-16
category: guardrails
tags: [gating, preflight, hitl, autonomy, idempotency, determinism]
confidence: learned
source: private-work
---

A cluster of related dispatch failures surfaced during the first sustained live-run of a multi-agent dispatch system. Each failure mode is distinct but all share a common cause: the dispatch path assumed manual discipline where mechanical gates were needed.

**Outbox idempotency.** A leftover envelope and an accidental duplicate nearly triggered two concurrent agent runs for a single task. The executor claimed work oldest-first, so a post-hoc manual park raced the claim. The correct fix is structural: every task must carry a stable, unique key, and the dispatch path must deduplicate and clean the outbox atomically before any agent is started. Relying on an operator to tidy the outbox by hand is not a process; it is a latent double-dispatch bug.

**HITL routing is a flag, not a bypass.** An autonomy gate that requires human approval will either skip silently or block waiting for a channel reaction unless the dispatch call explicitly signals that the approval has been obtained. An operator saying 'go ahead' in chat does not satisfy the gate — the approval must flow through the correct flag or parameter so the gate itself records the authorization. A dispatch runbook is owed that makes this the default path, not an exception.

**Verify dispatch at the source of truth, not via local output.** Piped command output buffers until process exit, so 'watching the logs' gives no real-time confirmation that an agent was actually started. Confirmation must come from querying the orchestration layer directly — checking that the target agent transitions to an active state — not from parsing local stdout.

**Spec sharpness determines fix quality.** A vague task description — 'fix the bug in module X' — gives an agent enough room to write a failing test, call it done, and return success. Dispatch specs must identify the exact artifact and location, state the acceptance criterion precisely, and explicitly rule out partial completions ('a test alone is not the fix'). Observed outcome: one agent given a sharp spec delivered schema change, loader fix, test, and manifest update; another given a vague spec returned only a failing test.

**Verify the premise before dispatching a fix.** A bug that was live when the task was created may have been resolved in the interim. Dispatching a fix agent against a stale premise wastes capacity and can introduce regressions. Before any fix dispatch, an explicit recon step should confirm the defect still exists in the current production or integration state. Operator re-authorization of a dispatch does not reset the staleness of the underlying premise — the premise itself must be re-verified.

Taken together, these five gates form a minimal preflight checklist: build shared dependencies first, deduplicate and clean the outbox, pass the HITL authorization flag explicitly, verify agent activation at the orchestration layer, and confirm the bug premise is still real. A credential-validity check alone is insufficient; build freshness, outbox cleanliness, and premise currency are equally load-bearing.
