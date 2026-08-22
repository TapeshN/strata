---
title: The pull-generate-restart deploy ritual also applies to a dev-mode server, not only to production containers
date: 2026-08-16
category: infra
tags: [release, verification, infra-truth]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A development-mode server backing a live demo crashed after several source pulls with no
accompanying schema-push, client-regeneration, or restart — the "pull, regenerate, restart" deploy
discipline is usually framed around production containers, but it applies identically to a
long-running dev-mode process relying on hot-reload, which cannot silently absorb a schema change
the way a fresh container boot can. Compounding the outage: the process supervisor entry for that
dev server had been disabled at the OS level, so a routine crash became silent, indefinite
downtime instead of an automatic restart — the supervisor's own status command reported "service
not found" until the entry was explicitly re-enabled.

The generalizable ritual for any dev-mode demo process: pull, then provision the schema against
that environment's own (often throwaway) database rather than assuming a migration history exists,
regenerate any derived client code, then explicitly restart via the process supervisor — and add
that supervisor's own enabled/running status to the regular health sweep for demo infrastructure,
since a disabled supervisor entry looks identical to a healthy one until something actually needs
to restart.
