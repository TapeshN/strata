---
title: "\"That would cost a read per request\" was true of one path and false of the path that mattered"
date: 2026-09-06
category: infra
tags: ["cost-argument-scope", "loadActor", "revocation-immediacy", "already-paying-path"]
confidence: learned
source: private-work
---

before rejecting a check on cost, ENUMERATE the paths and ask which already load the row. A cost argument is only valid for the paths that would actually pay; applied to a path already paying, it is a rationalisation for leaving a hole.

when a codebase already re-reads state on every mutation, adding a new fact to that state is nearly free — and the omission is invisible, because the read looks complete.
