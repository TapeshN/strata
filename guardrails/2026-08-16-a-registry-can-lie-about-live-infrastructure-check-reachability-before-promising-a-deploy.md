---
title: A registry can lie about live infrastructure, and "I can deploy there" needs a reachability check first
date: 2026-08-16
category: guardrails
tags: [gating, boundaries]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A status field inside a registry or config file (an `enabled: false` flag, a stale port
number) is a claim about the world, not the world itself, and it drifts. Reporting an
environment as down or disabled because a config file says so — without checking the
actual running process — can be exactly backwards: one investigation found a service
reported "disabled" in its registry entry was in fact healthy and serving, on a
different port than the stale entry recorded. Any "is X up or down" claim needs to be
verified against the live process (something listening on the port, a container
actually running) rather than trusted from a config file alone — the same failure mode
as a stale document asserting a shipped state that nobody re-checked against reality.

A second, related trap: before promising to perform a write, deploy, or push on someone
else's behalf, check whether the actual target path is reachable with the tools
available. An agent's write access can be scoped out of specific directories by
OS-level permissions in a way that is invisible until the write is attempted — a source
checkout that looks identical to any other in a file listing may in practice be
unreachable for the operations being promised. Naming that constraint honestly up front
("I can't reach this path, this step is yours") is better than promising a capability
and silently failing partway through it.
