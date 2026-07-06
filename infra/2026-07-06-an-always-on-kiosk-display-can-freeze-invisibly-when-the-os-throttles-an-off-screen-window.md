---
title: An always-on kiosk display can freeze invisibly when the operating system throttles an off-screen window, and only a self-reported liveness signal on the page itself can distinguish that from a real outage
date: 2026-07-06
category: infra
tags: [kiosk, occlusion-throttling, display-rearrangement, freshness-witness, frozen-renderer-vs-failing-fetch]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A full-screen kiosk-style display pinned to fixed screen coordinates can be silently stranded when the underlying display arrangement changes and the actual visible panel moves to different coordinates, while the browser window rendering the kiosk content stays parked at its old position. The operating system's compositor throttles rendering for windows it judges to be occluded or off the visible area, so that stranded window freezes at its last painted frame. From the outside this looks identical to a genuine service outage — a frozen timestamp, no visible update — even though the backing service is healthy and being polled successfully the whole time; the fetch layer is working, but the renderer displaying its results has stopped repainting.

A watchdog that only checks whether network requests are failing cannot catch this failure mode, because the requests are succeeding; the problem lives entirely in a renderer that has stopped updating for a reason external to the application itself. The fix is to give the page its own visible, self-updating liveness witness — a simple live clock ticking once per second directly on the page, driven by client-side script — so a viewer can immediately tell "the whole page is frozen" apart from "a fetch failed but the page is alive," plus a listener that forces a refetch whenever the page's visibility or the window's show event fires, so waking from a throttled state recovers on its own. Operationally, any deliberate rearrangement of a kiosk display's physical position should be followed by restarting only the dedicated kiosk browser process, never a shared or general-purpose browser session.
