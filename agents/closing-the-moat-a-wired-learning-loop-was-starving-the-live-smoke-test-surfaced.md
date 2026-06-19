---
title: Closing the moat: a "wired" learning loop was starving; the live smoke-test surfaced producer + append gaps that unit tests and a soft brief hid
date: 2026-06-17
category: agents
tags: [the-moat, learning-loop, cursor-dispatch, wired-not-working, live-smoke-test, agentic-brief-contract]
confidence: learned
source: private-work
---

**Trigger:** an honest orchestration audit found the cross-class learning loop (keystone connector, merged earlier) "wired but never closed once" — all prior Cursor dispatches returned `pr_url:null`/`tokens:0`, `evals/learnings.jsonl` did not exist, Check was dark for lack of a gate-ledger. Building the Check-consume leg + fixing dispatch, then a LIVE one-dispatch smoke-test, exposed what 8 passing witness tests could not.

an agentic dispatch brief must SPELL OUT the deliverable contract (open a PR; emit THIS JSON schema as the final message) — a soft sentence yields nothing. The `pr_url` parser must read the actual PR the agent opened (any branch), not assume the dispatch branch. `appendLearnings` must fire on the Executor path too (or every dispatch must route through Route). Also: park/clear the dispatch OUTBOX before `npm run execute` — a stale envelope gets re-fired; and `needsHitl = autonomy_level < acceptAutonomy`, so a same-level `--accept-autonomy N` dispatches without Slack.

a wired pipe is NOT a working pipe — verify the DATA flows end-to-end with a LIVE run, not just that the code compiles + unit-tests pass (the keystone passed 8 witness tests while reading an empty file). For any producer→consumer loop the DoD is "a real artifact traversed the whole chain once," proven live. Capture remaining gaps as the loop's OWN first learnings.
