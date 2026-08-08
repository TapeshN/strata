---
title: A dead compositor can swallow clicks silently while the DOM keeps responding
date: 2026-07-25
category: mcp
tags: [headless-browser, browser-automation, dom-truth, determinism, reproducibility]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

In a long browser-automation session with repeated pane resizes and restarts, the visual rendering layer can silently desync from the live page — the on-screen capture goes stale or blank even though the underlying page keeps executing correctly: scripted reads of the page's own content still succeed, and its event wiring is still intact. In that state, a coordinate-based click (aimed at pixel coordinates rather than an element) can appear to land on the right control and produce nothing at all — no navigation, no follow-up dialog, no outbound request — which looks identical to the feature itself being broken.

The diagnostic order that resolves this quickly, cheapest signal first: check the network log before anything else — zero outbound requests after a click means the click never reached any handler, which rules out an application-logic bug immediately. Next, compare the visual capture against a fresh, scripted read of the page's own content; a stale or blank capture sitting over a page that is still demonstrably live and responsive confirms the rendering layer itself has desynced, not the application. A forced reload of the pane typically resyncs it. While diagnosing (or as a durable workaround), drive the interaction at the element/DOM level instead of by screen coordinates — invoking a target element's own interaction behavior directly still fires the same handlers a real pointer action would, and for a form field under framework control, setting its value through the framework's own input-handling path is far more reliable than coordinate-based typing.

One related trap worth flagging: if the page under test opens a native browser confirmation dialog, an automated pane may silently auto-dismiss it without any visible sign that happened — a workaround installed to intercept that dialog needs to be reinstalled after every page reload, since it does not survive a navigation.

General lesson: when a browser-driven interaction "does nothing," suspect the rendering/compositor layer before the application or its handler — a page that is still live by every scripted measure but visually frozen is the tell, and driving interactions at the DOM/element level is a resilient way to keep working while the visual layer catches up. This extends the broader "prefer DOM-truth over screenshots when a browser tool looks flaky" principle with a sharper, faster-to-run diagnostic order and a concrete workaround for the specific "click reaches nothing" symptom.
