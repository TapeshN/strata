---
title: A sensitivity-flagged config pulls empty over any programmatic path — use the execution context already trusted with it, and never express a policy threshold as a ratio of a config that can move
date: 2026-08-30
category: infra
tags: [secrets, migrations, thresholds, ci]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A migration needed a production database credential, but the platform had that credential flagged as sensitive: every programmatic pull returned an empty string rather than an error, and the platform's own "encrypted" listing view gave no way to distinguish a sensitive variable from an ordinary one, so a blocked pull looked identical to a misconfigured one. The unblock was architectural rather than a workaround: the deploy platform's own production build already runs with that credential available, and executes exactly once per release, so the migration step was added inside the production build itself — hard-gated on the platform's own real production-environment marker, specifically because the same environment variables are also reachable from preview builds, where an ungated migration step would let any pull request silently mutate the production schema.

A second, unrelated policy bug surfaced in the same piece of work: a session-rotation window was expressed as a fraction of a token's total lifetime rather than as a fixed duration. That ratio only produced the intended "roughly an hour" behavior for the one configuration it was tuned against; a much shorter-lived token in a test environment inherited the same fraction and rotated every few seconds, which an automated test caught immediately. The fix was to express the policy as an absolute value with an explicit cap and floor — the shorter of a fixed ceiling and half the token's life — so the intended behavior can never regress silently just because some other config's shape changes.

The generalizable rule in both cases: when a credential is deliberately unreadable from outside its platform, look for the execution context the platform already trusts with it rather than trying to extract it. And any time a policy threshold is derived as a ratio of another value, ask what happens when that other value gets small; if the answer is "it breaks," express the policy as an absolute number with a floor and ceiling instead.
