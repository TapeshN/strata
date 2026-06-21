---
title: Environment-variable shadowing is a recurring failure class — diagnose the layering, not the value
date: 2026-06-10
category: infra
tags: [secrets, boundaries, determinism, lifecycle]
confidence: learned
source: private-work
---

Three distinct shadowing failures appeared in a single session, each with a different mechanism but the same presenting symptom: a tool behaved as though it was using a different value than the one you had set.

**Session-scoped export over credential store.** A temporary `export VAR=value` in an interactive shell takes precedence over the credential store for tools that check the environment before the store. The session export is invisible to a reader of the store file. Applications launched from that shell inherit the export.

**Last-definition-wins vs. first-definition-wins file parsing.** A configuration file with two definitions of the same key will resolve to either the first or the last, depending on the parser. Assuming the wrong resolution rule leads to the wrong value being read. For dotenv-style files: the standard is last-definition-wins; for some parsers it is first. A diagnostic `head -1` on a file with duplicate keys will show the first definition, which may not be the one the application reads.

**Quote stripping in manual extractions.** A value in a configuration file surrounded by single quotes will be stored with the literal quote characters unless the extraction pipeline strips them. Shell `source` commands and purpose-built loaders strip quotes correctly; manual `grep | cut` pipelines typically do not. The mismatch produces a value with trailing or leading quote characters that fail validation.

The diagnostic pattern for any "tool is using the wrong value": print the length and the first and last characters of the value the tool actually received, without printing the value itself. A length mismatch or unexpected leading/trailing character points immediately to the shadowing layer. Do not attempt to debug the value; debug the extraction path.

Prevention: any environment that supports multiple definition sources (env export, dotenv file, credential store, config file) needs a documented precedence order, and the rotation checklist must verify that the winning layer holds the intended value.
