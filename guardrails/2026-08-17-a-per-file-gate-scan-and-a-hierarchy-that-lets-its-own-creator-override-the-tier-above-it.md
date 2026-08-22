---
title: A per-file gate scan and a hierarchy that lets its own creator override the tier above it
date: 2026-08-17
category: guardrails
tags: [security-floor, gate-design, authorization]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A capability check was removed from only the write-handling verb of a money-mutating API route
while its read-only verb kept the check — the full test suite of many hundreds of tests stayed
green, because the wiring-verification scan only confirmed the check's string appears once
somewhere in the route's file, and the accompanying behavioral test happened to exercise a
different verb than the one that lost its guard. When a single route file hosts multiple HTTP
verbs, "the check appears in the file" is not the same claim as "the check guards every verb" —
gate-scanning tests need to enumerate every route file AND every verb, independently.

Separately, a resource's ownership model let its recorded "creator" field override an admin-tier
role on every governance action once that field was first populated (it had previously always
been empty, so the branch had never actually fired) — the practical effect was that a genuine
administrator was refused control over a subordinate's own resource, and deactivating the creator
(while keeping their membership record) left the resource with NO ONE able to govern it at all,
recoverable only by a direct data edit. The general anti-pattern: an ownership predicate for an
org-level resource should UNION a creator role with the admin tier, never let the creator branch
replace it — and whenever a feature first populates a rights-bearing column that had always been
empty, every authorization branch that reads that column deserves a fresh read, since a previously-
dormant fallback can silently become live, wrong code the moment real data starts flowing into it.
