---
title: Sensitive env vars pull empty; the production build is the governed place to use them (and ratio thresholds only mean what you think for one config)
date: 2026-08-30
category: infra
tags: [secrets, migrations, vercel, thresholds, tests-catch-policy.]
confidence: learned
source: private-work
---

when a credential is deliberately unreadable off-platform, look for the governed execution context that already holds it instead of extracting it; express policy thresholds in absolute terms (with an explicit cap/floor), never as ratios of a config that can change.
