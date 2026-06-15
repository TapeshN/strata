---
title: A containerized observability tool must not use host-coupled signals; unknowable state should surface as UNKNOWN, not a false default
date: 2026-06-11
category: orchestration
tags: [isolation, boundaries, hitl, autonomy]
confidence: learned
source: private-work
---

An observability dashboard running inside a container will silently lie if any of its state signals rely on host-only resources. Two common patterns that fail inside a container:

1. **Host PID checks** — testing whether a process is alive by signaling its PID (`os.kill(pid, 0)`) always reports the process dead inside the container because the container PID namespace does not include host PIDs. A factory-state tile that checks the coordinator's lock PID this way will always show IDLE even when the coordinator is actively running on the host.

2. **Host home-path checks** — reading a file under the host user's home directory (e.g., `$HOME/.claude/projects/…`) fails in the container where `$HOME` resolves to the container's own home, which is empty. Any freshness or existence check against such a path silently falls through to its "not found" default.

**The design rule for containerized status tools:** every signal must be derivable from the read-only workspace mount, or it must render an honest `UNKNOWN` state rather than falling through to a misleading default (e.g., IDLE, 0, empty). Host-PID and host-home checks are enrichment only — acceptable additions when they can resolve, but must be guarded with `UNKNOWN` fallbacks rather than producing negative certainty.

**Diagnostic corollary:** when a container-hosted tile shows 0 or a negative status, verify that the data source it reads is actually mounted in the container before assuming the host state matches. A sibling directory to the mounted root is not automatically visible inside the container.

**Two same-day instances of the same class** is the threshold for structural treatment: add it as a named design rule and audit all similar state-derivation paths for the same assumption.
