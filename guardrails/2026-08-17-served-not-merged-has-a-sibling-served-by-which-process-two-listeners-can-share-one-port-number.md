---
title: "Served, not merged" has a sibling: served by WHICH process — two listeners can share one port number
date: 2026-08-17
category: guardrails
tags: [deploy, served-not-merged, infra-truth]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A demo environment was refreshed repeatedly (pull, provision, regenerate, restart) after every
merge, and a local health probe against the demo's port kept returning a healthy response — yet an
external viewer reported the demo looked stale for an entire day. The external tunnel serving that
viewer was in fact routed to a completely different process bound to the SAME port number (a
containerized release, in this case) than the local development server the refresh ritual had been
restarting; the two processes coexisted on the same port via different network interfaces, so a
same-machine probe against the port kept hitting the wrong one while the tunnel kept hitting a
container whose build predated the day's entire body of work.

The generalizable rule: "served, not merged" (a merge landing on the main branch is not the same
as it reaching a live viewer) has a sibling failure mode — served by WHICH process. Whenever a
port could plausibly have two independent listeners (for example a containerized release bound to
one network interface and a dev server bound to another), a bare local probe against that port is
ambiguous. The only unambiguous witness is to check state INSIDE the process that actually backs
the externally-reachable path, or to hit the external URL itself directly — never a same-machine
probe that could silently resolve to either listener.
