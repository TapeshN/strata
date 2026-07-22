---
title: Represent a live, multi-route application by hosting and embedding it, not by flattening it into a static snapshot
date: 2026-07-19
category: orchestration
tags: [architecture, embedding, product-design, boundaries]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A deliverable that is a real running application — login, role-based routing, multiple pages, client-side hydration — cannot be honestly represented as a single static file dropped into a catalog of concept artifacts; doing so forces a lossy snapshot that materially changes what's actually being delivered. The better move, once a deliverable is a genuinely running app rather than a static concept, is to deploy it to its own hosting target and grow the surrounding system's "embed a design" capability into an "embed a hosted, live app by URL" capability — a same-origin-isolated frame around an allowlisted external URL, rather than a self-contained file.

**The rule:** a single self-contained file is the right format only for genuinely static concepts. The moment a deliverable is a running application, host it at its own real address and reference it by URL from wherever it needs to be reviewed or presented — don't force it backward into a static-artifact shape it no longer fits.
