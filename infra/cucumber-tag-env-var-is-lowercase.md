---
title: Tag-filtering env var and spec-filter config flags must be set correctly for Cucumber tag filtering to work
date: 2026-06-03
category: infra
tags: [ci, determinism]
confidence: learned
source: private-work
---

In a widely-used Cypress/Cucumber preprocessor library, the environment variable that controls tag filtering is case-sensitive and lowercase. Using an uppercase variant causes the filter to be silently ignored — all specs run instead of only those matching the tag. Additionally, tag-based spec filtering requires two configuration flags in the library's package.json section; without them, tags are evaluated per-scenario but all spec files still open.

Configuration: set both spec-filter flags at project creation and use the lowercase variable name in all scripts. A misconfiguration here produces no error — it simply runs everything, making it easy to assume tag filtering is working when it is not.

General lesson: when tag filtering appears not to work, check the variable name casing and the two spec-filter config flags before debugging the tags themselves.
