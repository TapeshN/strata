---
title: "When a branch owns the behaviour, resolve its tests toward the branch, not the base's expectations"
date: 2026-09-12
category: infra
tags: ["merge-conflicts", "tests-follow-code", "checkout-m"]
confidence: learned
source: private-work
---

before resolving a test conflict, read which side changed the PRODUCTION call; the test follows the code that owns the behaviour.
