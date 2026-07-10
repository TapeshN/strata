---
title: A new write of an already-gated class of data must mirror the codebase's existing authorization gate
date: 2026-07-07
category: guardrails
tags: [security, gate-consistency, dispatch-spec-guardrail]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a codebase already reserves a specific class of write — flipping a document to a client-visible or published state, for example — for a particular authorization tier, any NEW code path that performs that same class of write must thread the same authorization check, not just call the underlying data-write function directly. In one instance, a newly-built helper set a "visible to the client" flag with no role check at all, reachable from an action that itself required elevated privileges, and could have let an intermediate-tier user trigger a client-visible publish that the codebase's model reserves for a higher tier. This was caught by an independent review, not by any automated test, precisely because the write compiled fine and matched every existing type signature.

The generalizable fix for anyone specifying this kind of work up front: when a new feature will write a flag or field that an existing function already gates (published, approved, visible, an explicit state transition), the spec for that work should explicitly say to mirror the existing authorization pattern for that write class — find the sibling function that already gates the same kind of write and copy its check. An agent or developer building the feature will not reliably infer an unstated authorization convention; it has to be named.

A related, distinct judgment call: "safe to merge because nothing reads this data yet" is a real and legitimate verdict, separate from "this is complete." A backend change that writes data no user-facing surface currently displays can be safe to ship even with a known, deferred access-control gap — but only if that gap is explicitly tracked against the specific trigger that would create real exposure (the day a reader for that data ships), not left as a vague someday. This is the honest middle ground between fixing every finding before any merge (which can over-block a legitimate, still-undecided design question) and shipping a known gap behind an untracked "follow-up" that quietly never happens.
