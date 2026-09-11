---
title: Four false verdicts in one session, all one bug: the check could not tell "it is absent" from "I failed to look"
date: 2026-08-31
category: infra
tags: [verification, false-negative, positive-control, silent-failure, measure-the-real-thing.]
confidence: learned
source: private-work
---

a verification must fail LOUDLY when it could not observe. Check the fetch's exit status, assert the artifact you searched is non-empty and is the artifact you meant, wait for animations to settle before measuring geometry, and confirm your pattern matches a known-present control before trusting its absence elsewhere. A grep that finds nothing has told you nothing until you have proven it can find something.

pair every "expected absent" assertion with a positive control in the same run. And note the asymmetry: a false failure costs a detour, a false pass ships the bug — the fourth error was a network hiccup being reported to the operator as a missing fix, which is the cheap direction, but the same blindness produced two false passes on the expensive one.
