---
title: Four recurrent artifact-hygiene failure modes and their mitigations
date: 2026-06-10
category: guardrails
tags: [ip-boundary, contracts, preflight, gating, docs]
confidence: learned
source: private-work
---

A single session surfaced four distinct but related ways that an artifact can silently misrepresent its own state. Each is worth cataloguing as a class, not just a one-off fix.

**1. Internal naming leaking into public artifacts.** Codenames, initiative labels, and internal calendar identifiers rode into public-facing pull-request titles and bodies before anyone noticed. The operator caught the mismatch — the language read as insider shorthand rather than a plain deliverable description. The fix operates at two layers: worker-level instructions that prohibit internal naming conventions in any externally visible text, and a coordinator-level scrub that catches slippage before merge. This is the same family as the no-internal-IDs rule, extended to cover initiative codenames and lane identifiers.

**2. A stub that runs successfully is not the same as a complete artifact.** A data-seeding command completed without error, which led the team to blame the environment for missing data. The root cause was the seed script itself: it populated only a small fraction of the expected records, with the remainder living as hardcoded values in application code that never touched the database. The command worked; the artifact was incomplete. The diagnostic discipline is to read the artifact before debugging the invocation. Catalog completeness — whether a script, migration, or fixture fully represents the intended state — is a deploy-witness concern, not just an environment concern.

**3. Environment-variable shadowing is a recurring class, not a one-time accident.** Two separate shadowing failures appeared in the same session. In one case, a shell-local export silently took precedence over a credential stored in a secrets manager, causing several freshly-issued credentials to appear to fail when they were never being used. In a second case, a stale localhost connection string on the first line of a multi-definition config file shadowed the correct remote URL on a later line. The generalizable principle: when a tool behaves as though it is using a different value than the one you believe is active, suspect precedence — shell environment beats keyring, and in a file with duplicate definitions the winner depends on parse order. The diagnostic is to inspect the variable as it exists in the live shell environment, and to grep config files for duplicate definitions before assuming the value you set is the value being read. Periodic hygiene sweeps should include a duplicate-definition check alongside rotation and liveness checks.

**4. Wired but never fired is a distinct state from working.** Code that fully implements an integration — correct interfaces, plausible logic, no obvious defects — can reach production with zero real invocations. All observed executions may be fixtures or synthetic test rows, making the integration appear load-bearing when it has never been exercised against a live system. This state is not detectable by reading the code; it requires cross-referencing execution ledgers, dispatch logs, or equivalent runtime evidence. A periodic wired-versus-load-bearing audit — separate from code review — is the appropriate control. The audit also surfaces manifest drift, where documentation or configuration references a surface that the code has retired, or vice versa.
