---
title: Agents doing feat/fix work must satisfy the repo's changelog_gate
date: 2026-06-16
category: agents
tags: [agent-dispatch, changelog-gate, spec-completeness, ci]
confidence: learned
source: private-work
---

any dispatch/subagent spec for a repo that gates on CHANGELOG must include the instruction: "feat/fix commits MUST add a CHANGELOG `[Unreleased]` bullet under an existing `### Added`/`### Changed`/`### Fixed` section — never a duplicate section header."

add a changelog-gate awareness line to the dispatch runbook template (alongside the outbox-clean and `--accept-autonomy` steps). Workers building in a repo they haven't touched before should grep for `changelog_gate` in CI config + act accordingly.
