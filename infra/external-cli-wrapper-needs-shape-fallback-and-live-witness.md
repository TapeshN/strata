---
title: Any tool wrapping an external CLI needs a shape-fallback and a live smoke witness — mocked boundaries cannot catch version drift
date: 2026-06-11
category: infra
tags: [ci, gating, interfaces, versioning]
confidence: learned
source: private-work
---

A tool that wraps an external CLI can have a fully green test suite and still break the day after a routine system update renames or removes an output field. The failure mode is classic: the test suite mocks the CLI boundary, so it proves the tool's internal logic but not the interface contract with the external binary. A field the tool has always read is gone in a new version, and every call silently falls to a different code path — typically one that defaults to a conservative or wrong verdict.

**Three requirements for any tool that wraps an external CLI:**

1. **Shape-fallback.** Implement a dual-shape fetch: try the new/current field first; if the response doesn't include it (unknown field error or missing key), fall back to the previous field shape. The tool degrades gracefully instead of hard-failing or silently misclassifying.

2. **Conservative classification for unknown values.** When the tool receives a signal it cannot interpret, it must choose the safest verdict. For a CI check tool, "unknown signal → PENDING, never early-merge" is the correct conservative default. Defaulting to a pass on unknown input is a fail-open defect in a gate.

3. **A live smoke witness in the definition of done.** At least one test must drive the REAL binary, not a mock, and assert the observed output shape matches the tool's current expectations. This witness does not need to be in the full test suite; it can be a separate integration test that runs in CI with the actual binary installed. Without it, interface-premise drift is undetectable until production.

**Mocked-boundary suites prove logic, never the boundary.** This is not a defect in mocking — mocks are correct for testing internal behavior. It is a gap: the boundary itself needs a separate, live witness.
