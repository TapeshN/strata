---
title: Grep undercounts when migrating every call site of a shared import
date: 2026-07-07
category: guardrails
tags: [testing, determinism, ci]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Migrating every usage of an old shared authentication helper across a set of files, a simple text search for the old function's name found one usage in a given file and that one usage was migrated and committed. The file actually had three usages, at different scopes and indentation levels (two inside separate conditional branches, one in a different handler entirely) — the text search's line-context window simply didn't surface all of them. The type-checker then correctly flagged the two remaining, now-broken usages once the old import was removed.

The general rule: a plain text search is not a reliable completeness signal for a sweep that removes or replaces a shared import, especially across files with multiple handlers, aliased imports, or usages split across different code branches. The authoritative "every site has been migrated" signal is a type-checker or compiler error on the now-unused or now-removed symbol — when doing this kind of migration, remove the old import first and let the compiler enumerate every remaining call site, rather than trusting a text search's count.

A separate, related lesson from the same period: certain control-plane operations (compacting a running log of lessons learned, rewriting a shared status document) are reserved for whichever single coordinating session currently holds an exclusive lock, and a session that is not the lock-holder correctly declines to perform them. However, if the lock's recorded holder is confirmed to be a dead process (not merely quiet, but verifiably no longer running), that lock is safe to reclaim rather than treating it as a permanent block — the single-writer rule protects against two LIVE sessions writing concurrently, not against ever recovering from an abandoned lock.
