---
title: "A second spine replaced the first and did not inherit its obligations; and a cache invalidation aimed at a query that cannot return the row"
date: 2026-09-04
category: evals
tags: ["architecture", "client-notifications", "two-spines", "revalidate-noop", "audit-framing", "obligations-not-features"]
confidence: learned
source: private-work
---

Two spines, one standard applied. When a new surface becomes the primary path for something a previous surface already handled, diff their OBLIGATIONS (who gets told, through what, with what recovery) — not just their features. The old one is the specification, and "the old one still works" is what hides this for months.

A revalidation aimed at a query that cannot return the row is a no-op that reads as wiring. For any `revalidatePath` / cache-bust / refetch, open the target route and confirm its QUERY can actually return the row you just wrote. The call being present is evidence of intent, never of effect.

The strongest counter-evidence is the part worth keeping.
