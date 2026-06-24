---
title: HTTP 200 on the HTML is not a witness that the rendered page loads — verify assets at the serving URL
date: 2026-06-23
category: guardrails
tags: [verify-dont-trust, evals, interfaces, ci]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A page was verified pre-merge by confirming that the HTML URL returned HTTP 200 and that the asset files were reachable at their canonical paths. The page still shipped broken: fonts and scripts did not load. The root cause was relative asset references (`src="app.js"`, `url("fonts/…")`). At the page's actual serving URL — which differed from the assets' canonical paths due to a path-rewriting layer — the browser resolved the relative paths against the wrong base, producing 404s for every asset.

The pre-merge check answered the wrong question. "Can the HTML be fetched?" and "Can each asset be fetched at its direct path?" are both true. "Does the page render correctly when served at its real URL?" was not asked.

**The rule:** for any page served through a path-rewriting layer, the verification witness is a screenshot or computed-style check of the rendered page at its actual serving URL — not a curl of the HTML plus separate curls of the assets' canonical paths. A 200 on an asset's direct path does not guarantee the page's embedded references resolve correctly from the URL the browser actually visits.

This is a specific instance of the general principle: the witness must exercise the same path the end user exercises, not a convenient proxy that shares only some of the properties.
