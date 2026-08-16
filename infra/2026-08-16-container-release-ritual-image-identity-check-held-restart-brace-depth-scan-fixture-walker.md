---
title: A container release ritual needs an identity check, a held restart window, a brace-depth scan, and a fixture walker
date: 2026-08-16
category: infra
tags: [release, ci, reproducibility]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Four small, concrete disciplines for releasing a containerized service, surfaced in the
same stretch of work.

A successful build command is not proof that the running container is serving the new
image. After any release, compare the running container's actual image identity against
the just-built tag — an image-digest or ID comparison — rather than trusting that "the
build succeeded" means "the new code is live." A stale-but-still-running container had
served a two-day-old image after an earlier build step's own false-positive; only a
rendered check of the live page, which was missing an expected new element, caught it.

Restarting a live service is not a neutral operation if someone has an open session on
it — identifiers minted per build (session or request IDs tied to a specific server
process) can go stale the instant that process restarts, breaking the very next
in-flight action for anyone using the app at that moment. Stage and build a new image
whenever convenient, but hold the actual restart or cutover for a window when no one is
actively using the service, or coordinate it explicitly.

Resolving a git merge conflict by concatenating both sides' hunks can, for a multi-line
CSS construct such as an animation block, split the construct exactly in the middle —
producing a stylesheet that is syntactically wrong but that a lenient parser (the one
used in local development, which never reads compiled CSS at all) accepts silently. A
stricter parser used only by the production build was the first thing to actually catch
it, well after the conflict had already been marked resolved and other checks had
passed. After resolving any conflict in a block-structured file, run a structural
sanity check — count opening versus closing braces, confirm the depth never goes
negative and returns to zero — rather than trusting that a conflict-free merge means the
result is still syntactically valid.

Introducing a strict ordering invariant — a later stage can only be reached once every
prior stage has genuinely been satisfied — broke existing test fixtures that had been
written to jump straight to a late stage by writing that stage's record directly,
skipping the ones before it. Those fixtures were faithful to the old rules but became
invalid the moment the new invariant shipped. The fix that keeps a fixture set both
useful and honest is a walker, not a wider jump: replay every prior stage through the
actual production path in order, skipping only stages already present in the fixture,
until the target stage is reached — preserving any deliberately-seeded state exactly as
recorded while guaranteeing every other prior stage was genuinely satisfied through the
real mechanism the new invariant checks. When a new invariant enforces an order over
what used to be independent states, update the fixture-generation path to walk the real
sequence rather than widening the invariant to tolerate old jump-fixtures.
