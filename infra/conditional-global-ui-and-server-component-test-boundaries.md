---
title: Conditionally-rendered global UI breaks hardcoded offsets; server components resist unit-test import
date: 2026-06-11
category: infra
tags: [testing, boundaries, contracts]
confidence: learned
source: private-work
---

Two frontend lessons from one lane, both about hidden contracts:

- **A global banner mounted at the app shell stacks above every downstream sticky element** — so every sticky `top` offset below it must be *conditional on the banner actually rendering*. Hardcoding the offset fixes one auth state (banner visible) and silently breaks the other (banner absent). An adversarial verifier caught the gap precisely because it checked the state the builder didn't develop in. The general rule: when a layout contribution is conditional, every measurement that depends on it must carry the same condition.
- **Server components that use server-only framework APIs (request headers, cookies) cannot be imported into a unit-test runner at all** — the import itself fails outside the server runtime. When you need to guard a derived data structure from such a component, mirror the expected key set inline in the test and document why the test can't import the real module. A subset-guard over a mirrored contract is weaker than importing the source, but it's honest about the boundary instead of silently skipping coverage.
