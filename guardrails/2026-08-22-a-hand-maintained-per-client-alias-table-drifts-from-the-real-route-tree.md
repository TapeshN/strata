---
title: A hand-maintained per-client alias/lookup table drifts from the app's real structure — derive it, and test it against a conformance check
date: 2026-08-22
category: guardrails
tags: [portal, data, conformance, twin-implementation]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A portal maintained a hand-written table mapping each client application's logical page names to its real route paths, used to resolve incoming feedback notes to the right page. The table was stale for the one app it actually covered (missing a mount-point prefix the app had since adopted) and simply absent for two others that shared the same mount-point pattern. The result: every note against the affected pages silently minted a duplicate "unknown route" entry beside the correctly-seeded one — dozens of duplicate records across all affected pages.

The fix had two parts: strip the shared mount-point prefix before doing the alias lookup, and regenerate each app's alias map from that app's own real route tree rather than a hand-maintained list, with a dry-run/apply reconciliation pass to merge the resulting duplicates back down. The lasting fix pairs this with a conformance test that resolves every route of every client app to exactly one canonical key and fails if a route would otherwise auto-create a new one.

General rule: any per-client (or per-tenant, per-integration) map maintained by hand inside a shared system will drift the moment the thing it maps drifts underneath it. Generate the map from the upstream source of truth, or continuously test it against that source — never trust a hand-authored list to stay accurate as new clients or new routes are added.
