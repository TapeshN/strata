---
title: "The shared checkout could not fast-forward for 35 commits, so every gate run there enforced stale code — and it blocked a worker's boot"
date: 2026-09-07
category: guardrails
tags: ["stale-primary", "gates-enforcing-stale-code", "append-only-merge", "shared-checkout", "worker-stop-was-right"]
confidence: learned
source: private-work
---

never trust a gate result from the shared checkout without checking it is current — `git rev-list --count HEAD..origin/main` first. And when a shared checkout is dirty, the reflex to stash is the trap: the worker's refusal to stash is what saved the 180 rows, because a stash-and-pull looks exactly like a fix.
