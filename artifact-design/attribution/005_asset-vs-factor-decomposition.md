# Asset vs Factor Decomposition

**Artifact**: Attribution
**Date**: 2026-08-14
**Status**: Design rationale — resolves open question Q2

---

## The Decision

Attribution is **asset-level** decomposition for v1. It asks "which *positions* is the risk coming from", not "which *risk factors*".

Factor decomposition is a direction to **iterate towards**, but it is **out of scope for now**.

---

## Asset vs Factor — Two Different Questions

| | Asset decomposition | Factor decomposition |
|---|---|---|
| Answers | Which positions carry the risk | Which systematic risk premia (equity beta, rates, gold, FX) drive it |
| Needs | weights + asset returns → covariance | a factor model: factor definitions, exposures, factor covariance |
| Status | v1 (definitive) | future direction, out of scope |

---

## Why Asset First — Dependency Order, Again

Factor decomposition is not a sibling of asset decomposition; it is a *layer on top of it*.

Factor attribution works by regressing asset returns on factors to get exposures, then attributing portfolio risk through those exposures. That machinery needs the asset-level returns and covariance as its substrate.

So "iterate towards factor" is the natural next depth once the asset-level pipeline exists — the same dependency-order logic as the cross-sectional / time-series boundary.

---

## What This Resolves

- **Q2** — asset vs factor: *resolved*. Asset-level decomposition for v1; factor decomposition is the intended next depth, explicitly out of scope now.
