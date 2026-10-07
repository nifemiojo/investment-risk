# Cross-Sectional Only, For Now

**Artifact**: Attribution
**Date**: 2026-08-14
**Status**: Design rationale — resolves the cross-sectional boundary

---

## The Decision

Attribution stays **cross-sectional only** for now. It decomposes one snapshot into its sources at a single point in time — it ignores trend and time-series.

Trend / time-series analysis can come later, either in this artifact (extended) or in another — **TBD**.

---

## Why Cross-Sectional First Is the Correct Build Order

This is not just scope discipline. The time-series artifacts are *downstream* of the point-in-time primitives in the dependency graph:

| Time-series analysis | Needs, first |
|---|---|
| Change Report | two snapshots (A vs B) |
| Drift Analysis | attribution + a target |
| Diversification trend | a history of attributions |

You cannot do change / trend / drift until the point-in-time primitives exist. Building cross-sectional first is therefore dependency order, not deferral.

---

## Same Discipline as the Snapshot

The Snapshot is already stateless — a point-in-time function that hands comparison off to the Change Report. Attribution follows the same discipline: it is a stateless decomposition of `(weights, covariance)` at one date. Keeping it stateless means it can be re-run for any date with no notion of "since when".

---

## What Cross-Sectional Includes and Excludes

**In scope (point-in-time):**

- Component contribution per asset
- Weight contrast (contribution vs weight)
- Standalone risk per asset
- Diversification benefit (a single number)
- Concentration (top-N %)

**Out of scope (time-series), deferred:**

- Diversification *trend* (rising / falling / stable)
- Correlation *shifts* (which pairs moved)
- Drift vs target
- Change since last period

---

## Where Trend Lands Later — TBD

The destination of the deferred time-series analysis is deliberately left open: it may extend Attribution later, or live in another artifact (Diversification Monitor / Change Report). Not pre-committed.

---

## What This Resolves

- **Cross-sectional boundary** — *resolved*. Attribution is point-in-time only; all trend / time-series analysis is deferred, with its eventual home TBD.
