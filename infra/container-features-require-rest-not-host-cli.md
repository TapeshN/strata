---
title: Container features must use REST with a mounted credential — not a host CLI
date: 2026-06-16
category: infra
tags: [isolation, boundaries, ci, interfaces, contracts]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A dashboard feature worked on the host development machine because the host had a CLI tool installed and authenticated. Running the same feature inside a container produced no results — the binary was absent from the image and the host authentication context was not available inside the container namespace.

The failure pattern: a feature is authored and verified on a machine where a CLI tool happens to be installed. It reads correctly in a local test. It silently fails or returns empty inside any containerized deployment because no container image includes host-machine CLIs or host-machine credentials by default. The feature needs to be re-authored.

The correct shape for any containerized feature that calls an external service: use the service's REST API directly, with a credential read from a volume-mounted path that is explicitly set at container launch. Verify the feature by running it from inside a running container instance, not from the host.

General rule: if a feature shells out to a CLI to reach an external service, it is implicitly host-coupled. For it to work in any environment other than the development machine, it needs to be rewritten as an API call with a portable credential.
