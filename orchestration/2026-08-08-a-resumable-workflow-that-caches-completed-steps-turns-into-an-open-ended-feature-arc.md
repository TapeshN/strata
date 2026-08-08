---
title: A resumable workflow engine that caches completed steps turns into an open-ended feature arc
date: 2026-08-08
category: orchestration
tags: [workflow, resume, caching, cost, orchestration-pattern]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A durable workflow engine that caches every already-completed sub-agent call, keyed on its exact input (the same prompt and options, byte-for-byte), makes it possible to append a new phase to a long-running script and resume it, re-running nothing that already completed. This turns what would otherwise be many separate workflow runs — and many re-paid setup costs — into ONE workflow with an ever-growing tail. To exploit this reliably: keep every already-completed step's call site byte-identical across edits, so only the surrounding control flow may change (for example, converting an early return into a variable assignment further down); always append new phases before the final return rather than restructuring earlier ones; and apply small, direct fixes to the working branch between phases rather than routing them through a mid-flight agent that might race the next resume. The broader pattern this enables: treat a genuinely long feature arc as ONE workflow with appended waves and a single integration branch, rather than spinning up a new workflow, and a new PR, for every round of feedback.
