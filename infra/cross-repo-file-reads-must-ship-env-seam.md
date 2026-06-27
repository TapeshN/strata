---
title: Any code that reads a file from a sibling repository must ship an env-seam override and a fixture default in the same PR
date: 2026-06-11
category: infra
tags: [multi-repo, ci, isolation, contracts]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A CI runner clones only the repository under test. Code that constructs a path like "../sibling-repo/config/file.json" fails the moment it runs in CI because the sibling directory does not exist. The failure is obvious in isolation but consistently overlooked when a single codebase grows to span multiple repositories.

The pattern that makes cross-repo reads CI-safe:

1. Replace the hardcoded relative path with a path read from an environment variable.
2. Provide a sensible default for when the environment variable is unset (a fallback fixture path within the current repo, or a known safe value).
3. In tests, supply a test fixture at the fixture path so the test suite runs without the sibling present.
4. Ship the env-seam, the fixture, and the code change in the same pull request. A cross-repo read without its seam is a CI failure waiting for the next merge.

When this class recurs — three or more instances of the same pattern across a 24-hour window — treat it as structural rather than incidental. A grep-based preflight check that flags new code touching sibling-repo paths without a corresponding env-seam in the same diff will mechanically enforce the rule going forward.
