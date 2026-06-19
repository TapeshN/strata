---
title: A red CI with a runner-startup-death signature is infra/billing, not code — don't fix-by-bumping-actions
date: 2026-06-16
category: infra
tags: [ci, github-actions, billing-cap, runner-startup-death, red-herring, diagnose-before-fixing]
confidence: learned
source: private-work
---

**Fix (at source) / Prevention:** the signature "job fails ~10s, zero steps, no logs, `system.txt` ends at *about to start running on the hosted runner*" + "public repos pass, private repos blocked, Actions status operational" = a **billing/quota wall**, not a code/action-version problem. Download the run-log zip and read `system.txt` (the failed-step log is "not found" but system.txt shows the runner handshake); cross-check sibling public-vs-private repo CI to localize. Never bump actions to "fix" a runner-startup death.
