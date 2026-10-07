# Triage and Prioritisation, Not a Verdict

**Artifact**: Attribution
**Date**: 2026-08-14
**Status**: Design rationale — resolves open question Q1

---

## The Decision

The PM's decision at the Attribution stage is not a binary one. It is a **triage and prioritisation** question: *which positions do I look at, and in what order?*

Attribution tells the PM **where risk lives**, not **whether that is wrong**. The output is a ranking that feeds the next phases of the workflow — it does not pretend to determine cut/add.

---

## Two-Stage Triage Funnel

The Snapshot and Attribution are two stages of the same routing logic, at different granularity:

| Stage | Granularity | Question | Output shape |
|---|---|---|---|
| Snapshot | Across portfolios | Which portfolios need a look? | Binary gate (investigate / no action) |
| Attribution | Within a portfolio | Which positions need a look, in what order? | Ranked prioritisation |

The funnel narrows from "this portfolio" to "these positions". The ranking is the input that decides which position the next phase (Change Report, Drift Analysis) opens on first.

---

## Descriptive, Not Normative

The reason Attribution cannot prescribe is structural, not stylistic:

- **"Where does risk live"** is a *descriptive* question. It needs only the current state — weights and covariance. Attribution holds both.
- **"Is that wrong"** is a *normative* question. It needs a *reference point* — the target allocation. Attribution does not hold the target.

Because Attribution lacks the reference, it literally cannot judge. The judgement is delegated to Drift Analysis, which *does* hold the target.

> "Stops short of cut/add" is therefore not a scope choice we are making. It is a consequence of the information the artifact carries.

---

## Implications

1. **No `decision` field.** A triage output is a ranked queue, not a verdict. A binary `decision` field would be the wrong shape for it — this settles the earlier "does Attribution need a binary decision field?" tension (E).
2. **The ranking is an input, not a terminal output.** It routes the PM to the next phase: the top-ranked position is where Change Report / Drift Analysis opens first.
3. **The boundary is information-grounded.** Attribution's descriptive scope and Drift Analysis's normative scope follow directly from which artifact holds the target allocation — not from an arbitrary line drawn between them.

---

## What This Resolves

- **Q1** — ranking vs gate: *resolved*. The output is a ranking that prioritises positions for investigation, explicitly stopped short of cut/add.
