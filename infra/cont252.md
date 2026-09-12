---
title: "Lost the CSS cascade three times in one day to a later rule at equal specificity"
date: 2026-09-10
category: infra
tags: ["cascade-specificity", "duplicate-rule", "measure-computed-not-source"]
confidence: learned
source: private-work
---

target by class (two-class specificity) and fold intent into the existing rule; comments at each site say which later rule they beat and why.

after a CSS change, measure the COMPUTED value in the browser. "The rule is in the file" is not evidence; the same file having a later rule for the same element is the default case in a 19k-line stylesheet.
