---
title: An invocation can succeed while the artifact under test is a stub — verify the artifact before debugging the invocation
date: 2026-06-10
category: guardrails
tags: [verify-dont-trust, evals, release, determinism]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A command that runs successfully does not prove that the artifact it invoked is complete. When a command produces fewer results than expected, or results that look thin, the first diagnostic question should be: is the artifact itself fully populated?

In a concrete case, a database seed command exited with success but produced a live system where every catalog entry appeared empty. The command executed correctly; the seed script it ran populated only a small fraction of the expected rows (those for which data had been explicitly added to the script). The remaining rows existed only as a client-side array with no corresponding database rows — the command surface was fine, the artifact behind it was incomplete.

The failure mode is easy to miss because the command's exit code is green, no error is raised, and downstream behavior looks like an environment or connection problem rather than a data problem. The diagnostic that cracks it is direct inspection of the output artifact: count the rows the system actually has, compare to the catalog of rows it should have.

This applies broadly to any relationship between a command and the data or artifact it produces:

- A generation command that exits cleanly may have generated only a partial result if the input catalog was incomplete.
- A build command that succeeds may have built only the modules for which source files were present.
- A migration command that runs without error may have migrated only the tables whose schema changes were included in the migration file.

The verification pattern: for any "the command ran but the system doesn't behave as expected" report, read the artifact directly before reading the invocation path. The question "is the artifact complete?" is faster to answer than debugging the invocation, and it is often the answer.
