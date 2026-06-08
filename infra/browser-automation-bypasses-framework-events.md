---
title: Browser automation that writes DOM values directly bypasses framework event systems
date: 2026-06-02
category: infra
tags: [ci, interfaces, determinism]
confidence: learned
source: private-work
---

Web automation tools that set form field values by writing to the DOM directly (bypassing the framework's event system) will appear to work — the field shows the value — but the framework's internal state stays blank because no event was fired. This causes form submissions to silently drop the entered data.

The fix: for framework-managed input components, use keyboard simulation events (focus, keydown, keypress, keyup) rather than direct value assignment. Direct-value assignment is only reliable for native HTML elements that listen to the lower-level change event rather than the framework's synthetic one.

General lesson: when automating a form built on a virtual-DOM framework, verify that the framework's bound state actually changed (the submit button enabling, a value echo in the UI) before assuming the input was accepted. The visible DOM and the framework's internal state are two separate things.
