---
title: Freshest-evidence-wins across ledger SNAPSHOTS; severity only breaks ties
date: 2026-07-18
category: infra
tags: [hooks, ledger, calibration, over-warn, freshest-wins]
confidence: learned
source: private-work
---

any gate that reads N copies of a ledger must compare row timestamps, not just row values; prompt ledger appends after each sync shrink the divergence window.
