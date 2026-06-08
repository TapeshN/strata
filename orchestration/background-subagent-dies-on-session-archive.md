---
title: Background subagents are orphaned when the parent session auto-archives; push work incrementally
date: 2026-06-07
category: orchestration
tags: [subagents, lifecycle, autonomy, parallel-sessions]
confidence: learned
source: private-work
---

Background subagents are children of the session that spawned them. If the session auto-archives due to inactivity while a long-running subagent is executing, the subagent is orphaned — it may not re-notify on completion, and its work may be only partially done or entirely uncommitted.

Mitigations that worked:
1. Builders push their work incrementally (small commits as each unit completes) so a session crash costs only the in-progress unit, not the whole lane.
2. A keep-alive mechanism that re-activates the session before the inactivity window closes prevents the archive.
3. Avoid running multiple heavy parallel builds simultaneously on a memory-constrained host — the combination of high context and heavy computation accelerates session instability.

General lesson: "durable" means "committed and pushed." Uncommitted work on disk is lost when a session dies. Build incrementally; treat each push as a checkpoint.
