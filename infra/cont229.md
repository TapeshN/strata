---
title: "I designed a production write from the seed file; the live tenant did not look like the seed"
date: 2026-09-06
category: infra
tags: ["live-shape-vs-seed", "findFirst-singular", "production-read-before-write", "self-authored-fixture"]
confidence: learned
source: private-work
---

before writing a script that mutates a live system, READ THAT SYSTEM'S SHAPE — not its schema, its actual distribution. Uniqueness that no constraint enforces is not uniqueness, and a seed file is a statement about intent, never about what accumulated.

the giveaway is a singular in the code (`findFirst`, "the owner", "the admin") for something the schema permits many of. Grep your own script for singular nouns and check each against a live count.

my tests all passed because I wrote both the code and the world it ran in. That proves internal consistency, not correctness.
