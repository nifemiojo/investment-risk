# 006 — What Covariance Captures: Direction and Magnitude of Co-Deviations

**Date:** 2026-07-22
**Topic:** Clarifying covariance's two-dimensional signal

---

**Question:** "Covariance tells us about the direction and magnitude of co-deviations from respective means?"

**Answer:** That's exactly it. Two dimensions in one number:

- **Direction** (sign): positive → they tend to deviate to the same side of their respective means. Negative → they tend to deviate to opposite sides.
- **Magnitude** (size): how large those co-deviations are on average. Bigger absolute value = stronger co-movement tendency.

The only thing covariance doesn't give you is a sense of *how strong is strong* — because magnitude is in raw units (%²), which aren't comparable across pairs. That's why we standardise into correlation. But the raw signal — direction × magnitude of co-deviations — is exactly what covariance captures.
