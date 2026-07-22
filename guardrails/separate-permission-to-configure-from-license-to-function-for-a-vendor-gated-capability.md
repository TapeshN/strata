---
title: When assessing whether a vendor-gated capability is possible, drive the real admin surface and separate permission-to-configure from license-to-function
date: 2026-07-20
category: guardrails
tags: [ground-truth, vendor-gotcha, determinism]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Asked whether a specific third-party integration was possible under an account provisioned through a reseller, the tempting shortcut was to answer from the vendor's public plan-tier documentation. The well-known failure mode ("a reseller-provisioned account locks you out of the underlying platform's admin console") turned out to be only half right, and the half that mattered was invisible without actually looking: reasoning from a public tier matrix conflates two genuinely independent gates — (a) whether the account holder has admin rights to grant an application permission, and (b) whether the specific seat/mailbox carries the license the target capability requires.

Driving the real admin surfaces directly revealed the true state: the reseller-branded portal was indeed the front door, but the underlying platform's own admin console opened fully and permission-granting was available — gate (a) was open, contrary to the initial assumption. The actual blocker was on the account's license page: the seat carried a lower email-only tier with no license for the capability in question — gate (b) was closed. The capability could never work regardless of any permission granted, and no tier-matrix document surfaced that fact as clearly as the account's own license screen did.

General rule: for any question of the form "can we configure vendor capability X given this specific account," drive the actual admin surfaces (the permission/consent state, and separately the license/seat state) rather than reasoning from the vendor's marketing or tier documentation — and treat permission-to-configure and license-to-function as two independent gates that must each be checked, since a pitch for a "native integration" dies on the license side far more often than on the permission side. A read-only credential probe against the platform's own API is often the fastest way to get this ground truth when the admin UI itself is ambiguous.
