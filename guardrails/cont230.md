---
title: "Splitting one risky release into two deploys made the dangerous half optional"
date: 2026-09-06
category: guardrails
tags: ["deploy-sequencing", "env-gated-mutation", "one-shot-switch-teardown", "runbook"]
confidence: learned
source: private-work
---

when a release contains both an irreversible-ish data change and ordinary code, gate the data half behind configuration that is absent by default. The merge then becomes reversible in the usual way, the data change becomes a separate decision with its own witness, and the diagnostic runs first.

also verify the teardown, not just the setup — a run with the one-shot switches LEFT SET proved transfer and retirement were idempotent no-ops while an internal helper silently reverted an office edit. That is why each switch is documented REMOVE AFTER rather than merely listed.
