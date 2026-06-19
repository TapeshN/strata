---
title: A deployed container lacks the host's CLIs + auth — prefer REST + mounted-token over shelling to a CLI
date: 2026-06-16
category: infra
tags: [docker, container-vs-host, gh, rest-api, wired-not-working, mounted-token]
confidence: learned
source: private-work
---

any container feature that calls external services must use an API client + a mounted credential, not the host CLI. Witness container features IN-CONTAINER, not on the host.

when authoring a feature that calls GitHub (or any external service) inside a container: (a) use REST + mounted token; (b) verify the feature from inside a running container before claiming it works.
