---
title: "An adversarial review of MY OWN script found two blocking defects that my own passing tests had missed"
date: 2026-09-06
category: infra
tags: ["self-review-blindspot", "identity-vs-repair", "canonicalization-seam", "readback-witness", "client-production"]
confidence: learned
source: private-work
---

two reusable rules. (1) A side channel that writes a record the app also edits must split IDENTITY (create-only) from REPAIR (safe every run), or it silently overwrites the humans. (2) Any identifier written by a side channel must be canonicalized by the SAME function the lookup uses, and verified by reading back through the lookup's own unique — not by trusting the write returned.

my tests all used well-formed input and a fresh database, so they exercised the happy path of my own mental model. The defects lived where the script met OTHER writers (the app's edit form) and OTHER readers (the auth route's normalizer) — the seams a self-authored test never visits. Review the seams, not the function.

passing my own tests means my code matches my assumptions; it is evidence about the author, not the system. On anything touching a client's live data, the adversarial pass is not ceremony — it paid for itself twice in one file.
