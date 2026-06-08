---
title: Partition the coordination surface by system and project; don't mix the runner and the product
date: 2026-06-06
category: infra
tags: [layering, multi-repo, docs, parallel-sessions]
confidence: learned
source: private-work
---

A single coordination document that mixes all projects and conflates "the system that runs builds" with "the system being built" dilutes the coordinator and creates confusion about what a given phase belongs to. The collision that results is a write-isolation problem, not a context-size problem — shrinking the document would not have prevented parallel agents from writing to the same primary.

The fix: name the two systems explicitly (the orchestration layer versus the product being built), partition the coordination surface per-project (each project has its own plan document), and use the root-level document only for cross-cutting concerns.

General lesson: the runner and the product are different things. When they share a planning document, decisions about each contaminate the other and context for a given system is always diluted by context for the other.
