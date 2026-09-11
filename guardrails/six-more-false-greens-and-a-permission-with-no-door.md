---
title: Artifact-state and witness gaps let false-greens pass undetected
date: 2026-08-12
category: guardrails
tags: [determinism, gating, ci, lifecycle, idempotency]
confidence: learned
source: private-work
---

Several distinct failure modes all share the same surface signature: a check completes, reports a passing result, and the underlying state is wrong. The unifying cause is that the check measured something adjacent to the property that mattered, not the property itself.

In deployment contexts, pulling a new commit and restarting a process are necessary but not sufficient. Any build artifact that is derived from source — generated clients, compiled schemas, cached manifests — exists in its own state that does not automatically advance when source advances. A deploy step is only complete when source, artifact, and process are all aligned to the same version. Treating 'merged' as equivalent to 'ready to serve' routinely produces runtime errors that appear immediately after a successful deploy.

In test suites, pinning the exact wording of an error message rather than the behavioral property the message describes creates a test that fails loudly on safe copy changes and passes silently when the behavior regresses in a way that happens to preserve the old phrasing. Security-relevant assertions should verify the property — the thing that was rejected, the tier that was not promoted — not a particular English sentence.

In shell automation, command chains that use short-circuit evaluation (such as and-chains) will silently skip later steps when an early step fails for an environmental reason unrelated to the logic under test. If the edit or transformation step is skipped, the validation step still runs — on the unmodified input — and reports a result that describes nothing. The mitigation is to emit a witness: a deliberate, observable signal that the mutation actually occurred, checked before the verdict is trusted.

In authorization design, a permission tier that cannot be assigned through any reachable interface is not a feature — it is an orphaned constraint. For every role or capability, there must be an explicit, auditable path by which a principal is granted it. The absence of such a path should be treated as a defect, not a security margin.

The common thread: a check that passes without having touched the thing it was meant to verify is indistinguishable from a check that passed correctly. The only defense is to make the verification step leave evidence that it reached the actual subject.
