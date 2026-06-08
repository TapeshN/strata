---
title: Conditionally-rendered DOM fields require an explicit wait before interaction
date: 2026-06-02
category: infra
tags: [determinism, ci, interfaces]
confidence: learned
source: private-work
---

In a virtual-DOM framework, a DOM update triggered by a user action (selecting a value from a dropdown, toggling a checkbox) happens asynchronously relative to the triggering action. Immediately interacting with a conditionally-revealed field after the trigger will fail because the field has not been inserted into the DOM yet.

The fix: assert that the field is visible before interacting with it. The visibility assertion acts as an implicit wait for the conditional render to complete. This pattern applies to any conditionally-rendered field — not just top-level toggles, but nested conditional chains as well.

General lesson: in any test interacting with a conditionally-visible field, add an existence or visibility assertion before the interaction. Never assume a field is present immediately after a triggering action on a related element.
