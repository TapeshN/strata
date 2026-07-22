---
title: A path that is both git-tracked and continuously runtime-mutated makes its checkout permanently unable to fast-forward
date: 2026-07-22
category: guardrails
tags: [control-plane, refresh, drift, stale-code, git]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A shared control-plane checkout carried tracked, append-only log files that automated hooks wrote to on every action. An automatic refresh routine correctly refused to fast-forward over any uncommitted change to a tracked file, as a safety measure — but because these particular files were rewritten continuously by the runtime itself, they were almost never in a clean state long enough for the refresh to fire. The checkout drifted many commits behind its remote and, as a direct consequence, ran stale versions of its own automation — recently merged fixes to its own hooks were simply not active there, because the checkout that would have picked them up could never catch up. Committing the drifted state closed the gap for only a few minutes before the same hooks dirtied it again, including from the very session that had just committed it.

The durable fix is not "commit more often" — that is a treadmill against a process that mutates faster than any human-paced commit cadence can keep up with. It is an architectural decision: either the refresh routine gets an explicit ignore-list for paths that are known to be runtime-mutated (accepting that those paths simply won't auto-refresh and must be reconciled some other way), or the path itself gets untracked from version control and moved to an archived/append-elsewhere pattern. The general rule: a path should never be simultaneously (a) tracked in version control, expected to stay in sync with a remote, and (b) mutated by the running system on every cycle — pick one, because trying to satisfy both guarantees produces exactly this kind of permanent, self-inflicted drift.
