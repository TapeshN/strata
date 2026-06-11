---
title: Roughly a quarter of "green" builds carried a defect only an adversarial pass found
date: 2026-06-11
category: evals
tags: [evals, proofs, judge]
confidence: learned
source: private-work
---

In one evening of parallel build lanes, independent verifiers tasked with *refuting* each builder's claim caught four real defects that had all shipped green: a path resolver that silently returned the wrong root (empty output reading as success), a non-hermetic test that broke the moment real data existed, an alias accepted where the canonical name was required (the builder's fix stopped one hop short), and content deep-linking users into an environment missing one of its advertised targets — masked because the spec asserted a link prefix but never that the targets were a subset of the environment. Roughly a quarter of that day's green builds carried a defect only the refuting pass found.

Every catch came from an executed witness — run it, mutate it, fetch it — never from reading the code. Three sub-patterns generalize:

- A mapping between a catalog and an environment needs a **subset guard** (each row's targets ⊆ the environment's slice), proven to fire on a known-bad pairing; a prefix or existence check is theater.
- **Phantom coverage**: tests that re-implement the production rule inline prove the test, not the code. Detection is the mutation protocol — break production and demand a failing test; the fix is exporting or injecting the real unit and driving the real path.
- **Absence claims are checkable claims.** "This repo has no CI" was repeated by a builder and its first verifier while every recent PR showed named checks running. Claims that a gate does not exist get the same verify-don't-trust treatment as claims that one passed.
