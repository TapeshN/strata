---
title: "A legend is a promise the view has to keep — and reconciling two surfaces by adding a field just mirrors the bug"
date: 2026-08-12
category: infra
tags: [ui-truth, verification, twin-implementation, instrumentation, cross-surface-parity]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

# A legend is a promise the view has to keep

A key beside a data visualisation states a fact: *this colour means this
status*. If the drawing renders that status in a different colour, the key is
not decoration that happens to be stale — it is a false statement, and the
reader believes it over the pixels, because the key is the thing that claims to
explain them.

The same user reported this twice, two days apart, from opposite directions:
first that the drawing never showed the colour the key promised; then, after a
fix, that the key no longer matched the drawing.

## Reconciling a disagreement by adding a field just moves it

The first report was "fixed" by adding a dedicated *swatch colour* to the status
definition, so the key could show a status at full strength while the drawing
washed it faint. That is a **reconciliation field** — a second place the same
fact is stated — and it produced the exact mirror image of the original defect.

Worse, the statuses that never got the new field had been wrong the whole time
in a quieter way: their swatch painted a translucent colour onto a **white
card**, while the drawing composited the same translucent colour over a
**coloured background**. Alpha over white is not alpha over anything else.
Never the same colour, for any status, in either direction.

The fix was to delete the second field. One value per status, and the swatch
renders it the way the drawing does — same value, same backdrop, same
compositing. They cannot disagree because there is nothing left to disagree
about. The one genuine adjustment then falls out honestly: the shared value had
to move so that **one** number works in both places.

**Prevention.** When two surfaces disagree about a fact, delete one of the
statements; never add a field that lets them differ deliberately. If a
legend / summary / preview appears to need its own version of a value, ask what
actually differs between the two contexts — it is usually a *rendering
condition* (a backdrop, an alpha, a blend) that should be reproduced, not a
second constant that must be kept in sync by hand.

**Prevention.** Any surface whose job is to explain another surface must be
*derived* from it, or changed in the same breath. Where they genuinely must
differ, the difference is a decision to write down, not a default to inherit.

## A colour change has as many outcomes as it has backdrops

A wordmark rendered light on one step of a flow and dark on the next, which read
to the user as "it changes colour when I submit". Forcing the light treatment
made both steps agree — on a phone, where the card sits on a photograph. On a
desktop the same card sits on pale paper, and a light wordmark on pale paper is
invisible. This was caught only by screenshotting the change rather than
trusting that the stylesheet said what was meant, and the change was reverted
rather than guessed at a third time in one batch.

**Prevention.** Before shipping a colour or contrast change, list the surfaces
the element appears on — viewport widths, themes, photo versus flat plate — and
look at each one. And when the mechanism turns out not to live where you expect
it (neither in the component nor in its stylesheet), that is the signal to go
find it, not to overpower it from somewhere else.

## The user's parenthetical question is the finding

Asked for an input cap, the user added: *"or is this a manual guard against the
error state?"* It was neither — there was no cap at all, so the only thing
catching a mistyped value was the rejection *after* submitting. They were asking
whether an absence was deliberate, which means they had already run into the
absence.

**Prevention.** When someone asks "is this on purpose?", answer by **checking**,
not by explaining the design. The question is evidence they hit something; a
confident yes without a look is how a real gap gets talked past. And prefer a
field that cannot hold a wrong value over a message explaining one — server-side
validation stays as the thing that *decides*, not as the interface.

## A probe with a guessed field name returns the default, not an error

Investigating "this region renders with no colour", real rows were fed to the
real status-derivation function, which reported every record as the default
status — which looked exactly like a live bug worth reporting. The function's
parameter was named `effective`; the probe passed `status`. Structural typing
with optional members means a wrong key is not a crash, it is a *plausible
answer*: nothing matched, so every branch fell through to the default.

**Prevention.** Read the signature of any function you are calling as an
**instrument**, especially one you did not write. A measurement harness deserves
the same scrutiny as production code, because a wrong reading is worse than no
reading — it points the next hour at a fiction. Sanity-check a probe against a
case whose answer you already know before trusting it on the case you don't.

## Name the layer you could not reach

For that same report, three layers were measured and agreed — the database rows,
the shared derivation, and the live API response. The rendered pixels were not
seen, because the browser session had lapsed, and that was said plainly rather
than folded into "everything checks out".

**Prevention.** A layered claim is only honest if the unmeasured layer is called
out by name. "Everything checks out" over a chain you sampled three-quarters of
is the same false green as a passing test that never ran.
