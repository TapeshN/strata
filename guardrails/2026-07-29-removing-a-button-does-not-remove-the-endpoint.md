---
title: Removing a button does not remove the endpoint behind it
date: 2026-07-29
category: guardrails
tags: [security, boundaries, interfaces]
confidence: learned
source: private-work
implementation_target: agent-guardrails
efficacy: decorative
---

A hardening pass added guards to a dangerous write path and shipped clean through a first review. A second, independent review caught what the first missed: older code paths implementing the same dangerous operation, whose UI entry points had been removed long ago, were still exported and directly callable — bypassing every new guard the hardening pass had added.

The root cause was scope: "guard every sink" was read as "every sink the new feature touches," not "every sink that performs this operation anywhere in the codebase, including legacy ones nobody remembers wiring up." A server-side handler compiled into the build is a live, remotely invocable entry point the moment it exists — regardless of whether any UI still calls it.

The fix is a full-tree sweep: whenever a dangerous operation gets a new guarded implementation, grep the whole codebase for every other implementation of the same verb against the same data, and either delete or reroute each one through the new guard. This is exactly the kind of finding that only shows up on a second, independent review — the author who added the new guard is the same person who scoped it to "the new feature," and won't independently think to look elsewhere.
