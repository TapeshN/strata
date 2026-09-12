---
title: "I wrote the \"a ruling that never reaches the artifact is not enforced\" learning, then reproduced it four hours later with the briefs themselves"
date: 2026-09-07
category: guardrails
tags: ["artifact-reachability", "coordinator-defect", "gate-covers-wrong-failure", "recurrence-after-recording"]
confidence: learned
source: private-work
---

the gate I built checks that a brief's BASE resolves; it cannot see that the brief itself exists nowhere the workers look. Those are different failures in the same family — *the artifact is wrong* vs *the artifact is unreachable*. A dispatch is only real once the thing dispatched is on the branch the worker reads; verify reachability from the CONSUMER's ref (`git ls-tree origin/main`), never from the branch you authored on.

passing a gate is not the same as being delivered. The base gate went green on a file that no worker could see, which is the exact "green for the wrong reason" shape banked in an earlier entry — and I was the one who wrote that entry. **Writing a learning does not inoculate you against it**; only a mechanical check does, and only if the check covers the failure that actually happens rather than the one you happened to witness.
