---
title: "An unattended dispatch loop can complete having done nothing, three different ways"
date: 2026-08-25
category: orchestration
tags: [dispatch, autonomy, subagents, exit-conditions, unattended]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

**1. A loop's exit condition must assert the actual guarantee it exists to provide, not a proxy that usually correlates with it.** A dispatch loop was written to run "until the queue is empty," intending that to mean "until every pending item has actually been sent out." A prior pass had already moved every item out of that queue into a holding area without ever dispatching it, so the loop found an empty queue on its very first check and exited immediately, having sent nothing — technically satisfying its literal exit condition while completely failing its actual purpose. The general fix: state the real guarantee explicitly (here, "every item now carries a live external identifier confirming it was actually sent") and check that directly, rather than checking that a queue or directory is merely empty, which only tends to correlate with the goal most of the time.

**2. Instructions handed to a remotely-dispatched agent must be self-contained, or independently verified against that agent's own environment.** Two dispatched tasks referenced a file path for further instructions that existed in the dispatcher's own working environment but not in the separate environment the dispatched agent actually ran in. Both agents had nothing to do and produced no output. The fix is either to inline the full instructions directly into the dispatch payload, or — if referencing a path — to verify that the path actually resolves inside the target's own environment, never inside the environment the dispatcher happened to be sitting in while writing the instructions.

**3. When one of several parallel channels is reliably producing and another reliably is not, reallocate the work rather than spending time debugging the failing channel.** Several parallel unattended lanes were dispatched for one overnight run; one channel worked reliably throughout the night while the others each failed for distinct reasons, none diagnosed until morning. In hindsight, the cheapest correction available for hours was simply routing the pending work to the channel already demonstrated to be working, rather than spending that same window diagnosing why the others weren't — a real-time triage principle for any unattended run with more than one execution path: prefer the channel with a live positive signal over investigating a channel with a negative one, especially when the clock itself is the scarce resource.
