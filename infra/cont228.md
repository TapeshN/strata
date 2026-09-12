---
title: "Membership is not rank: one set served two questions and answered the second one wrong"
date: 2026-09-06
category: infra
tags: ["authorization-model", "membership-vs-rank", "policy-pinning-test", "ruling-vs-code-drift"]
confidence: learned
source: private-work
---

when one collection answers two different questions ("what may I hand out" and "whom may I act upon"), it will eventually answer one of them wrongly. Give the second question its own predicate.

the tell was writing a test comment that explained why the surprising `true` was acceptable ("a peer director is within a director's assignable set"). A test that has to argue with the ruling it implements is pinning a bug.
