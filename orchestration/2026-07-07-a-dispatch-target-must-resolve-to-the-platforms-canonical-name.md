---
title: A dispatch target must resolve to the platform's canonical name, never the local checkout's folder name
date: 2026-07-07
category: orchestration
tags: [orchestration, dispatch, repo-resolution]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A background coding-agent dispatch system defaulted its target-repository field to the LOCAL checkout's directory name whenever the caller didn't specify one explicitly. In a workspace where local folder names commonly differ from the actual remote repository name (an internal naming convention that adds a local-only prefix to every checkout), this default silently pointed every unconfigured dispatch at a repository that does not exist on the remote host, and the dispatch failed with an access error that read like a permissions problem rather than a wrong-target problem.

This exact failure mode recurred twice, in two different parts of the dispatch pipeline, because the wrong assumption (folder name equals remote name) was baked into more than one default/fallback path, and only the EXPLICIT-repo code paths had ever been exercised in testing — the DEFAULT path had shipped untested.

The general rule: anywhere a local checkout's directory name and its remote repository or package name can diverge — which is common when a workspace uses local-only naming prefixes or conventions — never derive a remote identifier from the local folder's basename. Resolve it from an explicit registry or mapping instead, and specifically unit-test the DEFAULT/fallback code path, not just the explicit-parameter path; a bug that only lives in a default value is invisible to any test that always supplies an explicit override.
