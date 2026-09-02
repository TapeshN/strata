---
title: Four verification checks in one session, each unable to tell "the thing is absent" from "I failed to observe it"
date: 2026-09-02
category: guardrails
tags: [verification, dns, absent-vs-unobserved, degraded-state, extraction-pipeline]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

**1. A split-horizon DNS name resolves differently depending on which network path answers it.** A private mesh network's own name resolver failed to resolve a hostname that a public-facing ingress in front of the same service served correctly, from both the machine hosting the service and a separate coordinating machine on the same mesh. A bare lookup from either host reported the service as down. The fix was to probe through the actual public path — forcing the connection to the known public IP, or resolving from an outside network — before calling anything an outage. The mesh's own name resolution and the public ingress are two different answers to "is this reachable," and only one of them is the one a real visitor uses.

**2. Two different counters of "how much work is queued" can disagree, and a report must say which one it read.** An automated reminder surfaced one count of pending items; the actual work file it was supposedly summarizing held a different, much smaller count. The two data sources measure different things — a periodic nudge versus the live ledger — and had silently drifted apart. Any report of "the queue" must name which source produced the number, or the report itself becomes a second source of confusion layered on the first.

**3. A witness for a failure state must hold that state for the whole capture, not just the moment before.** A screenshot meant to document a degraded UI state was lost because the underlying service was restarted concurrently with the browser session capturing it — the restart raced the capture and the evidence never existed. Any capture of a transient or degraded state needs the state held stable, or reproduced deterministically, for the full duration of the capture, not assumed to persist because it existed a moment earlier.

**4. A deterministic text-extraction pipeline can silently drop structure it doesn't recognize, and the failure looks like a clean success.** An automated step that pulls a short lesson out of a longer numbered note picked up only the leading sentence and silently discarded every trailing sub-clause, and separately emitted a piece of its own internal formatting as if it were a content tag. Neither failure raised an error; both produced well-formed-looking output. A publish pipeline for auto-extracted content needs its own shape validation on the output — does every extracted item still read as a complete thought, do emitted tags look like tags — because a confident, well-formed, incomplete result is worse than an explicit failure: it looks done.
