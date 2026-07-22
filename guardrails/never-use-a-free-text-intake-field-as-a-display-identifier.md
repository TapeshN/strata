---
title: Never use a free-text intake field as a display identifier
date: 2026-07-19
category: guardrails
tags: [ux, data-modeling, product-design]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A feature that let users describe something in a free-text field ended up using the raw text of that field, truncated only by a hard character cap, as the item's display title elsewhere in the product — so a whole run-on sentence could render as a page heading. The fix had to happen at two layers: derive a genuinely concise title at the point of creation (first clause, capped sensibly), AND independently cap/truncate at the display layer on a word boundary, so that existing already-bad records self-heal on render with no data migration required.

**The rule:** a free-text intake/description field is never an acceptable source for a display identifier. Derive a real title at the point where the record is created, and defensively re-cap at every place it's rendered — the display-layer cap is what protects you against every record created before the source-side fix existed.
