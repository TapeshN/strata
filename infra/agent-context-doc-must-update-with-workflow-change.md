---
title: Agent-governing context documents must be updated in the same PR as workflow changes
date: 2026-06-02
category: infra
tags: [docs, release, multi-repo]
confidence: learned
source: private-work
---

When an automated workflow (such as a CI-triggered publish pipeline) is added to or changed in a repository, the agent-governing context document for that repository must be updated in the same pull request. These two artifacts are always coupled: if the workflow changes how a task is performed, the context document that instructs agents to perform that task is now stale.

Any agent following the old instructions will attempt the old process, which will fail by design in the new system. This is especially harmful when the new process is not manually runnable (for example, a tokenless pipeline that only works inside a CI context).

General lesson: when adding or changing a publish workflow or any automated task runner, include the governing context document update in the same PR. Treat them as a coupled unit, not separate concerns.
