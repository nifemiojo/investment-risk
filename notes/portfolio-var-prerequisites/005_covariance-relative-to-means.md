# 005 — Covariance is Relative to Individual Means (Clarification)

**Date:** 2026-07-22
**Topic:** Why covariance measures co-movement around each asset's own mean, not around zero

---

**Question:** "Covariance measures how two asset returns vary together around their individual means, so everything — the interpretation — is relative to their individual means?"

**Answer:** Exactly right — and that's a distinction worth cementing because it's easy to miss.

The covariance product is $(x_i - \bar{x})(y_i - \bar{y})$, not $x_i \times y_i$. The baseline is each asset's own mean, not zero.

Here's why it matters concretely:

| Day | SPY ($x_i$) | BND ($y_i$) | Raw $x_i \times y_i$ | $(x_i - \bar{x})(y_i - \bar{y})$ |
|-----|------------|------------|---------------------|----------------------------------|
| Tue | +0.10% | +0.05% | +0.005 | ? |
| Wed | −0.10% | −0.05% | +0.005 | ? |

Raw product says both days contribute the same positive signal. But suppose $\bar{x} = +0.04\%$ (SPY's long-run average is positive) and $\bar{y} = +0.01\%$:

| Day | SPY vs its mean | BND vs its mean | Covariance contribution |
|-----|----------------|----------------|------------------------|
| Tue | +0.10% − 0.04% = +0.06 | +0.05% − 0.01% = +0.04 | **+0.0024** (both above their means) |
| Wed | −0.10% − 0.04% = −0.14 | −0.05% − 0.01% = −0.06 | **+0.0084** (both below their means) |

Both are positive — assets moved in the same direction relative to their own centres. But the magnitudes differ. And crucially, a day where SPY does +0.02% (below its +0.04% mean) while BND does +0.03% (above its +0.01% mean) would contribute a **negative** product — SPY is below *its* average while BND is above *its* average — even though both returns are positive in absolute terms.

So: **everything is relative to each asset's own mean.** That's what makes it a measure of co-movement *patterns* rather than just raw direction.
