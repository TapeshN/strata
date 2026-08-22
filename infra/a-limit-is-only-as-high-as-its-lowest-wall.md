---
title: "A limit is only as high as its lowest wall, and the walls are usually invisible"
date: 2026-08-12
category: infra
tags: [verification, false-green, limits, shared-constants, test-design]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

# A limit is only as high as its lowest wall

A configurable cap was raised, and the feature still refused inputs at the old
number. The cap was not enforced in one place. It was enforced in four — a
client-side guard, a server validation schema, a body-size limit, and an error
message that quoted a number of its own — and raising the one that was easy to
find left the other three at the old value. The lowest wall is the real limit,
and the walls you did not change are the ones you did not know about.

**Prevention.** When a feature "has never worked", suspect a chain where each
link looks locally correct. Ask what the **read path** checks, not only what the
write path sets. A limit, a permission, or a format is rarely enforced once.

## A shared constant is a shared decision, and the name hides it

One of those walls was a constant imported from a module that belonged to a
different domain. Its name described the *original* domain, so at the second
call site it read as a neutral number rather than as a decision someone had made
elsewhere for reasons that no longer applied. Changing it in one place would
silently move a limit in the other.

**Prevention.** A constant reused across two domains needs its own name in the
second one. And any message that quotes a limit must take that limit as a
parameter — never read it from a module-level default, or the message will keep
confidently reporting the old number after the limit moves.

## Two quiet colours are one colour

Two adjacent states were rendered with translucent fills so close in value that,
at the size they were actually drawn, no one could tell them apart. Each was
individually defensible; the pair was not. A palette is judged in the
composition, not swatch by swatch in the file that defines it.

**Prevention.** For any set of values meant to be *distinguished*, check them
together at their real rendered size, not one at a time in the source.

## Pin the requirement, not the snapshot

Deliberately changing one of these values turned a test red. The test was
asserting the specific old value — a photograph of the behaviour at the moment
it was written, not the behaviour itself. It could only ever fail when the code
was *changed*, never when the code was *wrong*.

**Prevention.** After a deliberate change turns a test red, ask whether the
assertion was pinning the behaviour or a photograph of it. Then write the
version that would have failed against the **original** bug — that is the test
you actually wanted.
