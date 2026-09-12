---
title: "A credential's LOCATION is part of its authority, and a machine write needs machine attribution"
date: 2026-09-04
category: agents
tags: ["security", "credentials", "public-env-vars", "least-privilege", "audit", "machine-surface"]
confidence: learned
source: private-work
---

Refuse by absence, not by flag.

A machine write to a client-facing surface needs machine attribution or it is unauditable. Before wiring an agent to any client-visible write, check whether the write records what initiated it — and if it does not, that ledger is part of the feature, not a follow-up.
