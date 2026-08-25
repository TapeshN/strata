---
title: "Three infrastructure-hardening gotchas: digest pins, test config isolation, and backoff diagnostics"
date: 2026-08-25
category: infra
tags: [docker, digest-pin, test-isolation, backoff, ci]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

**1. Loading a container image from a local archive does not satisfy a digest-pinned reference, even when the tag matches.** A deployment configuration pinned base images by content digest rather than by tag, for reproducibility. Loading those same images from a pre-built local archive onto a new host — rather than pulling them from a registry — left the local image store able to satisfy a plain tag reference but not the pinned-digest reference, because the metadata mapping a digest to a locally-loaded image is only populated by an actual registry pull, never by loading an archive. Any deployment pattern that mixes offline image loading with digest-pinned references needs an explicit registry pull for every digest-pinned image on any new host, not just a tag-based load.

**2. A test suite that reads a real user's live configuration file will pass or fail depending on that user's personal settings, not on the code under test.** A notification tool's test suite unexpectedly started failing the moment a real integration was configured on the machine running the tests, because the test harness's default configuration-loading path pointed at the same real config location a live user would use, rather than an isolated one. The general rule: any tool with a user-level configuration file must have its test setup pin that tool's config-loading environment variable or path to an isolated, non-existent location before each test run — never rely on the tool happening to have no real configuration present at test time.

**3. A retry backoff can make a manual or interactive test run look like it silently did nothing, when it in fact correctly deferred.** Running a notification or retry-based tool interactively, twice in quick succession, produced an empty-looking result both times with no explanation — the underlying cause was a cooldown window correctly suppressing a repeat action, but nothing in the visible output distinguished "correctly deferred, still due later" from "found nothing to do." The fix is procedural: any tool with backoff or cooldown logic should be diagnosed from its own decision ledger — the record of what it considered and why it acted or didn't — never from the absence of console output, which looks identical for both "nothing to do" and "something to do, but not yet."
