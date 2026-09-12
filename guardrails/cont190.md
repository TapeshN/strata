---
title: "Three ways a check was precise and still wrong (a seed witness, a client complaint, a browser)"
date: 2026-09-04
category: guardrails
tags: ["witness-design", "gate-reads-green", "diagnosis", "client-feedback", "browser-automation", "demo-data"]
confidence: learned
source: private-work
---

A witness that describes the defect faithfully will certify it. Pin the DECLARED intent as a bare constant (`overdueUnclaimedCount !== HISTORY_UNFINISHED_ITEMS`), not a formula over the output, and trigger-test it by producing the state it must refuse. Corollary for demo data: the residue is deliberate — if everything is done the badge is decoration, if nothing is it is noise.

The shape of a complaint locates the bug. Check that the proposed root cause reproduces the DISTRIBUTION the reporter described, not merely the symptom; "some but not all" is itself evidence and usually names a branch.

Driving a production ui has failure modes the ui cannot show. When an agent drives a UI to change state, the DB is the witness and the screenshot is not — verify every mutation out-of-band, and treat repeated invisible failures as the signal to build the machine path rather than to keep clicking.
