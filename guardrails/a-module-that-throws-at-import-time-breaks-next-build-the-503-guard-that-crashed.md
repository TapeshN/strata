---
title: A module that throws at import-time breaks `next build` (the 503-guard that crashed the build it meant to make graceful)
date: 2026-06-16
category: guardrails
tags: [[nextjs], [module-load-side-effects], [build-is-the-witness], [tsc-isnt-build], [completeness-critic-blindspot], [lazy-init]]
confidence: learned
source: private-work
---

any route-imported module must defer env-dependent throws to request time, never module scope.

a route/page module must NEVER throw (or do env-dependent work) at import — guard lazily. The witness for this class is a real `npm run build` (it imports every route under prod), NOT `tsc --noEmit` (type-checks without executing module init). Add "run `npm run build`" to any builder prompt adding a route that imports a singleton client. "Compiles" ≠ "builds".
