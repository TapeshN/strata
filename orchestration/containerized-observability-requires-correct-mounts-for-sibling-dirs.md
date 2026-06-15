---
title: A containerized observability tool requires mounts that match its actual data sources — sibling directories outside the mounted root are invisible
date: 2026-06-14
category: orchestration
tags: [isolation, boundaries, worktree, gating]
confidence: learned
source: private-work
---

When a dashboard or observability tool runs inside a container, its visibility is bounded by what is mounted. A root-directory mount does not automatically include sibling directories at the same level. If the tool's data source lives in a sibling directory (e.g., a worktrees directory adjacent to the project root), that source is invisible to the container, and any tile reading from it will show an empty or zero value — without surfacing an error.

**Diagnostic checklist when a container tile shows 0 or empty:**
1. Confirm which filesystem path the tile's data source reads.
2. Confirm that path is mounted inside the container (inspect the compose config, not just the image).
3. If the path is a sibling of the mounted root, add it as a separate bind-mount with an explicit env-var or config key.

**Stale container from a different compose project:** rebuilding an image with `docker compose up --build` does not replace a container that was started from a different compose project (different project name) and is holding the same port. The old container keeps serving. Check `docker ps` for the image name and compose project label, not just port binding, before concluding that a rebuild took effect.

**Images that shell out to external tools must ship those tools.** A container image built on a minimal base that calls an external binary (e.g., `git`) at runtime will crash silently when that binary is absent. The crash may produce a zero-count or an empty response that looks like valid data. Explicitly add required runtime tools to the image and test the invocation path — don't assume the base image includes them.

**Endpoint-naming clarity:** two endpoints that share a name prefix but serve different data sources (e.g., one for running processes, one for filesystem objects) cause diagnostic confusion when troubleshooting. Distinguish them clearly in naming and in error output so an operator checking the wrong endpoint doesn't conclude the data source is empty.
