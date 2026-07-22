---
title: A deploy pipeline's tail step can leave you standing on the protected default branch
date: 2026-07-21
category: guardrails
tags: [git, release, deploy, branch-hygiene]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A deploy sequence that ends by checking out the default branch, pulling, building, and deploying leaves the working tree sitting on that protected branch afterward — so the very next edit, made without thinking about it, lands directly on the protected branch rather than a feature branch. This is exactly what it sounds like it would cause, and it did: a follow-up content change landed on the protected default branch before anyone noticed, and had to be recovered by branching off the accidental commit and resetting the local protected branch back to the remote's version (loss-safe, since the commit itself was preserved on the new branch).

**The rule:** treat "return to a working branch" as the explicit LAST step of any deploy sequence, not an afterthought — or, more robustly, have your editing tools refuse to let you make changes while HEAD is a protected branch, so the mistake becomes structurally impossible rather than something that depends on remembering to check.
