---
title: A container runtime's own backend VM can die first under host memory pressure, silently, while its status process lingers
date: 2026-08-22
category: infra
tags: [docker, infra, agents]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

After a night of several parallel agent workers, each running its own throwaway database instance, a local dev server, and a browser automation harness, host free memory dropped to a small fraction of a gigabyte — and the container runtime's actual virtual-machine backend process had already exited, while a separate long-lived status/menu-bar process for the same runtime kept running and reporting as if nothing were wrong. A full machine restart was required. The post-mortem found several never-cleaned-up leftovers from past sessions: a multi-hour-old dev server, more than one throwaway database instance (one several days old, from an unrelated earlier session), and — after the restart — a dormant scheduled job that unconditionally relaunched a now-broken duplicate service on a port an active service already used.

General rule: when running a fleet of parallel agent workers alongside always-on services (a container runtime, demo environments) on one machine, treat host RAM as a shared, finite budget across the whole fleet, not an unlimited resource each worker can assume for itself. Every worker that starts a disposable process (a dev server, a scratch database, a browser instance) must tear it down when done and report what — if anything — it left running. Periodically sweep for and kill orphaned processes across the whole session. And any scheduled/boot-time job that (re)launches a service must first check whether an equivalent instance is already running before starting a duplicate.
