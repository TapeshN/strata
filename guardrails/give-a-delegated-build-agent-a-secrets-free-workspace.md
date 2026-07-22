---
title: A delegated build agent working on a repo whose .env reaches production should get a secrets-free workspace, not just an instruction not to touch prod
date: 2026-07-20
category: guardrails
tags: [isolation, boundaries, autonomy, hitl]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A repo's checked-in environment configuration points at a real hosted production database. A feature was delegated to a build agent to implement in a fresh, isolated workspace that was deliberately created without copying that environment file over. As a direct consequence, any database-migration or database-touching command the agent might have run was impossible to execute at all — not merely discouraged by a written instruction, but structurally absent the credential it would need.

General rule: when delegating a build task to an agent (or to any less-trusted executor) on a codebase whose default environment configuration reaches a production system, prefer to construct the delegated workspace WITHOUT the production-reaching secrets in the first place, in addition to stating the prohibition in the task's own instructions. "Impossible by construction" is a strictly stronger guarantee than "prohibited by instruction" — the former holds even if the instruction is misread, ignored, or the delegate reasons its way around it; the latter depends entirely on compliance. Where the delegate genuinely needs a subset of write access, provision a narrower credential scoped to only what the task needs, rather than the full production credential the primary workspace normally carries.
