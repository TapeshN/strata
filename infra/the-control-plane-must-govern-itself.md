---
title: The control plane has to govern itself — compact docs, honest monitors, scoped gates
date: 2026-05-31
category: infra
tags: [docs, monitor-design, gating, alarm-fatigue, governance]
confidence: learned
source: private-work
---

Three coupled control-plane bugs surfaced at once, each a case of the governance machinery failing its own standards.

1. **Living docs grow unbounded because refresh ≠ compact.** A working-set doc was only ever *appended* to; nothing was evicted, so it became an archive re-parsed every session. Fix: treat version-control history as the archive — working docs can evict shipped/superseded items freely, so compaction is lossless. Keep exactly one append-only ledger.

2. **A monitor must measure the live quantity it claims to.** A "context filling up" warner estimated from cumulative transcript bytes, which only grow — so it warned forever and never reset after a compaction. An always-on alarm is the same as no alarm. Fix: measure the live quantity (bytes since the last compaction boundary), so the signal resets and means something.

3. **A safety gate that over-fires trains you to disable it.** A boundary gate fired dozens of false hits on a doc that merely *named* the things it protects. The answer to an over-firing gate is to *scope* it (and tighten its term policy), never to bypass or delete it — precision is what keeps a gate trusted.

General lesson: the system that enforces discipline is not exempt from it. Apply the same compaction, honest-measurement, and precision-scoping standards to your own tooling.
