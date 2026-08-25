---
title: A stricter read-path validation than the write-path breaks previously-accepted data
date: 2026-08-25
category: guardrails
tags: [validation, boundaries, contracts, evidence]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A system that stores user-submitted files accepted a batch of images through its ingest path under one set of size constraints. Later, a separate read path — built independently, for a different original purpose — re-validated the same stored bytes against a stricter per-dimension limit before serving them, and rejected several of the very files the ingest path had already accepted and stored. The visible symptom was a plausible-looking but wrong story: broken image tiles that looked like a rendering bug, when the actual defect was that two different code paths silently disagreed about what a valid file even was.

The general rule: when a system validates a stored artifact more than once across its lifecycle — once to accept it, again to serve it, perhaps again to process it — every one of those validations must call the exact same shared function, not independently re-implement "the same" rule. Two independently-written validators that are each individually reasonable will drift, and the drift only surfaces later, against real accumulated data, as an asymmetric failure: content that was valid when written becomes invalid when read. Any new "validate on read" of previously-stored data should import the writer's validation function by reference rather than restate it, and a round-trip test for stored-artifact handling should push real, previously-accepted data through the actual current read path, not synthetic fixtures sized to pass by construction.
