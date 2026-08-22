---
title: A service health check must assert reachability AND artifact identity AND that a critical embedded component actually mounted — HTTP 200 alone is not a health signal
date: 2026-08-22
category: infra
tags: [monitoring, demo-infra]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Three externally-reachable demo environments all returned a healthy HTTP status from their standard health endpoint. One of them was nonetheless missing an embedded feedback widget entirely — a separate release had broken it for that one consumer (see the SRI-pinning lesson from the same review), and the health check had no way to notice, because "the server responds" says nothing about whether the specific build running is the one expected, or whether a client-side component that depends on a separate asset actually mounted in the page.

The fix: a per-consumer health observation that checks three independent things together — the endpoint is reachable, the build/version stamp actually running matches what the deployment registry expects, and (via a headless check) the specific embedded component's script tag is present, its integrity hash matches what's actually being served, and it visibly mounts in the rendered page. Any one of the three failing is a health alert.

General rule: for any system composed of an independently-deployed shell plus embedded/pinned sub-components, "the shell responds with 200" is necessary but nowhere near sufficient as a health signal. Build health checks around the specific properties that can silently drift out of sync with each other — served build identity, and whether a dependent embedded component is present and actually initialized — not just process liveness.
