---
title: Record the agent-to-action join at commit time, or auditing "did a machine touch production?" becomes transcript archaeology
date: 2026-08-23
category: infra
tags: [audit, provenance, gate-design, cost]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two gaps closed in one pass, both instances of the same rule: a policy that lives only in chat or in a memory file is not a policy.

Answering a simple audit question — did this automated builder touch production? — required grepping a near-megabyte conversation transcript by hand, because the join from an agent run to a git action existed only in the ephemeral run journal and never on the commit itself. Machine-authored commits carried a generic co-author trailer and nothing else: no run identifier, no agent role, no stage. Pull-request bodies carried no pointer back to the run journal either. The fix is to write the join at commit time rather than reconstruct it later — a trailer naming the run and the agent role on every machine-authored commit, a journal pointer in the pull-request body, and a checker that reports any machine-authored commit missing the trailer (warning by default, failing under a strict flag). After that, a plain log query answers the audit question in a second, and the provenance survives long after the transcript is gone.

That checker's first version illustrates the trap it was built to close: it recognized machine authorship by exactly ONE tool's co-author string, so commits produced through a different agent tool read as human work, and the gate reported clean over its own branch. A recognizer for "machine work" must enumerate every authoring channel actually in use, and its trigger test must plant one commit from each.

The second gap was model-tier allocation. When a subscription plan hit most of its weekly quota mid-week, stages had to be re-tiered by hand at a stage boundary so the week could finish — and a hand adjustment at eighty-four percent is not a rule. There is no API for plan usage, so nothing mechanical can refuse a spawn on usage alone. What CAN be mechanized: refuse a stage definition that names no model or pins the most expensive tier, warn when a review-labelled stage runs below the reasoning tier, and score a human-appended usage ledger at warning and failure thresholds, with an override that demands a written reason. Both halves of that check needed re-cutting before they meant anything — the first version was satisfiable by the mere presence of a field NAME in a prompt string, and its usage half was structurally always-passing. A gate that a comment can satisfy reads green and protects nothing.
