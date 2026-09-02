---
title: Retiring a shared credential is not done until every consumer of it is migrated, and a heartbeat nobody reads is not monitoring
date: 2026-09-02
category: guardrails
tags: [credentials, security-review, monitoring, heartbeat, existence-oracle]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

**1. A credential-retirement change that fixes the server side isn't finished until every caller of the old credential is enumerated and migrated.** A change that made a service correctly refuse a legacy shared credential shipped with its own tests green, but nobody had checked for every internal tool or scheduled job still authenticating with that same legacy credential. Two of them kept using it, started failing silently the moment the server-side change landed, and a full week passed with a dead automation loop before an unrelated security review of a different change happened to check "would the existing callers still work" and found they already hadn't. Rule: a credential-retirement change must list every consumer of the old credential and show each one migrated and exercised live — fixing the server side alone is half the job.

**2. A heartbeat file that nothing reads is not monitoring, it's a diary.** The failing automations were in fact writing a heartbeat or status file recording their own failure the entire time, but nothing consumed those files or alerted on a stale or failing heartbeat, so the failure sat silent for a week. Rule: every heartbeat or status artifact needs a reader wired to it that actively alarms on staleness or a failing status; a heartbeat with no listener provides the feeling of observability without the function.

**3. A read performed before an authorization check can leak an existence oracle even when the eventual response carries no data.** A code path that looked up a record before verifying the caller was allowed to access it leaked information through timing or behavior differences alone, independent of what the response body contained. Rule: order every sensitive path as authorize-then-read, never read-then-authorize — even a read whose result you plan to discard can still answer "does this exist" to someone who shouldn't be allowed to ask.
