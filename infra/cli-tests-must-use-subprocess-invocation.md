---
title: CLI tests must include at least one subprocess invocation of the real entry point
date: 2026-06-07
category: infra
tags: [ci, verify-dont-trust, interfaces, reproducibility]
confidence: learned
source: private-work
---

A test suite that imports a CLI module's functions and calls them directly may pass while the actual CLI invocation crashes on startup. The module import path resolves packages relative to the test runner, which may not match the environment when the script is invoked as a standalone program. Absolute-import statements that work under a test framework fail with module-not-found errors when the script is run directly.

In a concrete case, a suite with many unit tests all passed, yet the documented operator command crashed immediately with an import error when run as a CLI.

Prevention: any lane shipping a CLI must include at least one test that invokes the CLI via subprocess, verifying the real entry point works in the same way the operator would run it. The subprocess test catches entry-point-specific issues that in-process tests cannot surface.
