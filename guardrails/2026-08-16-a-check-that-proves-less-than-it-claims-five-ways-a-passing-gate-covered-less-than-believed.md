---
title: A check that proves less than it claims: five ways a passing gate covered less than believed
date: 2026-08-16
category: guardrails
tags: [gating, security-floor, layering, verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Five separate, unrelated incidents in one review stretch shared the same shape: a check or a fix
existed, appeared to cover the relevant surface, and in fact covered only a fraction of it.

A redirect for signed-out users was corrected in the shared guard function used by most routes,
while several individual pages carried their OWN inline duplicate of the same redirect logic that
fired FIRST and never went through the shared fix — an unauthenticated user could still reach a
page the fix was supposed to protect. This was the third time the same shape of duplicated logic
recurred; the reliable defense is to grep the underlying CONCEPT repository-wide before declaring
a cross-cutting fix complete, not just the one file a plan happened to name.

Separately, a build pipeline copied a set of image assets from a shared source directory into a
gitignored output directory on every build — so painting a fix into the gitignored copy directly
shipped nothing at all; only comparing the built artifact's checksum against the source checksum
revealed that nothing had actually changed. Any file a build script is free to regenerate deserves
an explicit "is this the producer or just a copy?" check before a fix targeting it is trusted.

A capability-gating test scanned an application's PAGES and reported success, while every one of
that module's dozens of underlying API routes and server actions had zero enforcement at all — the
scan proved only what it looked at, not the module's full reachable surface. The fix is to
enumerate a module's COMPLETE sink list (every route, action, and mutation path) and make sure the
scanning test's coverage matches that full list, not just the pages a human happened to think of.

A regression test asserted, correctly, that a pure predicate function returned false for a
disallowed case — proving the author understood the rule — while the code path that actually
served requests never called that predicate at all, so the disallowed case succeeded in practice.
A test of the RULE is not a test of its ENFORCEMENT; the assertion belongs on the actual serving
sink (does the route return the expected refusal?), not only on the isolated function.

Finally, a hand-maintained mapping table translated one naming convention into another for a set
of application routes, and several of its entries pointed at paths the running application never
actually served — every visit through the stale mapping silently minted a brand-new duplicate page
next to the real one, defeating the very de-duplication the mapping existed to guarantee. Any
hand-maintained map between two systems is a rot vector unless it is derived from, or tested
against, the live system it claims to describe.
