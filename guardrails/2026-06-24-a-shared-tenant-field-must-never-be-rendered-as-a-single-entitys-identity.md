---
title: A shared-tenant field must never be rendered as a single entity's identity
date: 2026-06-24
category: guardrails
tags: [boundaries, contracts, multi-tenant]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A multi-tenant admin surface displayed a shared workspace-level name field as if it were each individual client's own company name. Because the underlying field is scoped to the tenant, not to the client record, a name chosen for one client's context leaked onto every other client sharing that tenant — each client saw a label that actually belonged to a different customer entirely.

The general defect class: any field whose scope is broader than the entity being displayed is a latent cross-entity leak the moment it is rendered as if it belonged to the narrower entity. This is easy to introduce because the field is genuinely present and non-null on the record being rendered — nothing about the data looks wrong at the point of use, only its scope is mismatched with the display context.

The fix is to drop the broader-scoped field from the narrower entity's display entirely and render only data that is genuinely owned at that entity's own scope (in this case, the client's own contact identity rather than the shared tenant's label). The generalizable review question for any admin or reporting surface in a multi-tenant system: for every field rendered on an entity's page, does the field's write-scope match the entity being shown, or could two sibling entities under the same parent scope end up displaying each other's data through it?
