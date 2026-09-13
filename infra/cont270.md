---
title: "Two workers built opposite models of the same transition; the merge, not the build, found it"
date: 2026-09-12
category: infra
tags: ["state-machine-fork", "sibling-briefs", "hold-not-guess"]
confidence: learned
source: private-work
---

briefs that touch a shared state machine name the transition table they assume; the coordinator diffs those tables across in-flight briefs BEFORE dispatch; sibling merge-forwards run the OTHER branch's tests, not just their own.
