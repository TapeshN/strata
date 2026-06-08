---
title: CI first-try pass rate is the eval for classification tasks; build a separate eval loop only for judgment tasks
date: 2026-06-02
category: evals
tags: [evals, ci, golden-sets, judge]
confidence: learned
source: private-work
---

For classification tasks with mechanical outputs (does this entry have a valid schema? is the category field correct? does the required label exist?), CI is already the evaluation pipeline. Each submission is a test run; the first-try pass rate over time is the quality metric for the classifier that produced the entries.

A separate judge evaluation loop is only needed for non-deterministic, judgment-dependent outputs that CI cannot mechanically validate — for example, "is this entry generalizable enough to be useful?" or "is this explanation clear?"

Before designing a separate eval loop, check whether a CI gate already catches the failure mode. A mechanical gate whose pass rate is measured over time gives you the classification quality signal without additional tooling. Phase the separate eval in only when the corpus is large enough that the signal is meaningful.

General lesson: do less evaluation infrastructure before it is needed. CI first, measure its pass rate, then layer in a judge eval only for the genuinely non-deterministic quality dimension.
