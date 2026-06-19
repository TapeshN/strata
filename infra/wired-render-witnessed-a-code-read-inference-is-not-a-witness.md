---
title: Wired ≠ render-witnessed: a code-read inference is not a witness
date: 2026-06-16
category: infra
tags: [verification, wired-not-working, dont-claim-rendered-without-rendering, ui]
confidence: learned
source: private-work
---

a rendered UI claim requires actually rendering the UI and observing the element's value. Code-read + data-confirmation is evidence; rendering is the witness.

for any UI claim about a dynamic value (badge count, rendered text, panel state), the acceptable witness is: open the app → observe the element → match the expected value. "The code should set it to X" is not sufficient.
