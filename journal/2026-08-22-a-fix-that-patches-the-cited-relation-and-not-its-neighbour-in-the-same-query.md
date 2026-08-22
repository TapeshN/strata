---
title: A fix that patches the exact relation a report names, while a neighbouring relation in the same query stays open, is an incomplete fix
date: 2026-08-22
category: journal
tags: [security, tenancy, tests]
confidence: learned
source: private-work
---

A tenant-isolation review flagged one relation traversal in a multi-tenant application as leaking data across tenants; the fix added a tenant check to exactly that relation. A closer second look at the same query found a second relation, a few lines away in the identical select statement, that traversed the same kind of foreign-tenant boundary and had never been checked at all — an equally reachable leak the original report simply hadn't named. Separately, reverting both tenant checks and running the full test suite left it green, meaning the existing tests provided no actual evidence the fix did anything.

The durable lesson: a report naming one instance of a bug class is a starting point, not the scope — any schema with no structural (e.g. composite foreign-key) enforcement of a tenant boundary should be audited relation-by-relation in the whole query, not just at the cited line. And the only trustworthy signal that a fix is doing something is to revert it and watch the test suite turn red; a test suite that stays green with the fix removed proves nothing was actually being tested.
