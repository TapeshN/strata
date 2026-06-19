---
title: A require-all-secrets check in the build script breaks CI/preview (they lack the secrets)
date: 2026-06-16
category: guardrails
tags: [ci, build, secrets, gates, nextjs]
confidence: learned
source: private-work
---

build-script gates may assert only what's knowable at build time (leak prevention, types); never require runtime secrets in `next build`.
