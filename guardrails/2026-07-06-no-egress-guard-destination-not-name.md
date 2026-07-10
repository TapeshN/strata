---
title: A no-egress guard must validate the destination, not the provider name
date: 2026-07-06
category: guardrails
tags: [no-egress, ssrf, toctou, security-guard, adversarial-review]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A "no external network calls" guard is only as strong as what it actually checks. Validating a provider's *name* or a boolean "is this local" flag is not the same as validating the network *destination* the code will actually hit — and if the guard re-reads mutable configuration at call time instead of pinning what it validated, an attacker (or just a misconfiguration) can swap the target between the check and the use.

What happened: a team built a guard meant to guarantee a local-LLM code path never sends data off-box. The guard passed as long as a config variable held something that looked like a local endpoint and responded to a probe. An adversarial review pointed out two holes. First, nothing stopped that config variable from being set to a public URL that happened to answer the probe — the guard would happily approve traffic that was then POSTed straight to an external host. Second, even after the guard ran once, the calling code re-read the same mutable environment variable each time it made a request, so the value could be changed after the check and before the actual call (a classic time-of-check-to-time-of-use gap).

How to apply: for any "must stay local / no egress" guarantee, validate the *resolved* destination — is it loopback, a private (RFC1918/ULA/link-local) address, or an explicitly allow-listed hostname like localhost — and explicitly reject anything else, including cloud-metadata addresses (e.g. 169.254.169.254). Then capture that validated value once and thread it directly into whatever performs the call, rather than letting the call site re-derive or re-read the setting from mutable global state. Treat any "stays local" or "stays internal" check as a destination check pinned at validation time, never a name check re-evaluated later.
