# Attribution Design Decision: Minimal Header

**Artifact**: Attribution  
**Date**: 2026-08-18  
**Status**: Decision recorded  

---

## Decision

The Attribution screen header should be minimal. The observation label **“Close”** is not necessary for v1 and is removed.

No other part of the artifact design is changed by this decision.

## Header

```text
╔══════════════════════════════════════════════════╗
║  ATTRIBUTION                                     ║
║  60/40 Multi-Asset                               ║
║  As of 14 March 2022                             ║
╚══════════════════════════════════════════════════╝
```

## Rationale

The header only needs to identify:

- the artifact: **Attribution**;
- the portfolio: **60/40 Multi-Asset**;
- the observation date: **14 March 2022**.

“Close” can be safely assumed for now because the artifact has one understood observation point and does not yet need to distinguish between intraday, open, or close observations.

The risk measure and methodological boundary remain in the body of the artifact rather than being added to the header.

---

## Scope of this update

This decision changes only the Attribution screen header:

- remove **“Close”**;
- retain the artifact name;
- retain the portfolio name;
- retain the observation date.

It does not change the risk calculations, displayed evidence, visual structure, or interpretation boundary.
