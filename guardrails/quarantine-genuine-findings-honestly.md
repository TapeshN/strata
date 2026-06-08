---
title: Quarantine genuine findings honestly; weakening assertions masks real signal
date: 2026-06-02
category: guardrails
tags: [evals, determinism, verify-dont-trust]
confidence: learned
source: private-work
---

Greening a test suite by weakening assertions masks real signal — the opposite of what a quality harness should do. When failures include genuine defects (accessibility problems, regressions in expected behaviors, anomalies in event handling), the correct action is to quarantine each with a skip annotation and a tracking note, then report them to stakeholders.

The key distinction: test bugs (wrong fixture, wrong assertion, wrong auth) are fixed by correcting the test. Real findings are quarantined and tracked. A detection test should assert that a defect *exists and is observable*, not that it is absent.

General lesson: triage every failure as either a test bug (fix it) or a genuine finding (quarantine + track + report). A test suite that "goes green" by removing real-finding assertions is less valuable than a red suite that surfaces them honestly.
