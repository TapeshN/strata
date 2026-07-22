---
title: A name-enumerated security gate is only as strong as its tracked-resource list
date: 2026-07-21
category: guardrails
tags: [security, gating, completeness, owasp-a01]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A completeness-style security gate meant to catch missing authorization checks across a codebase's data models works by scanning for reads of models on an explicit tracked list. A newly-added model's SENSITIVE read — the one actually returning private, unpublished data — went completely unflagged, not because the gate's logic was wrong, but because the new model had simply never been added to the list it enumerates by name. The exact safety net designed to catch this class of regression had a hole shaped precisely like the thing that had just been added.

**The rule:** adding a new model to a codebase means adding it to every name-enumerated gate that's supposed to cover models of that kind, in the SAME commit that introduces it — a gate scanning by name is invisible to whatever hasn't been registered with it, no matter how sensitive the actual read is.
