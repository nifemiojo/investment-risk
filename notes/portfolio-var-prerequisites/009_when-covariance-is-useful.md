# 009 — When Covariance Is Actually Useful

**Date:** 2026-07-22
**Topic:** Covariance's raw units are essential for computation, even though they're bad for comparison

---

**Question:** "So when is covariance useful?"

**Answer:** Covariance's raw units are essential — just not for comparing co-movement patterns. It's useful when scale *matters*:

### 1. Portfolio variance formula

$$\sigma_p^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\,\text{Cov}(r_1, r_2)$$

This needs the raw covariance. If you only had correlation, you'd have to multiply back by σ₁σ₂ anyway. The scale contamination that makes covariance bad for comparison is exactly what makes it correct for portfolio math — the contribution of co-movement to portfolio risk depends on both the pattern *and* how volatile each asset is.

### 2. Beta

$$\beta = \frac{\text{Cov}(\text{stock}, \text{market})}{\text{Var}(\text{market})}$$

Raw covariance again. A stock with high correlation to the market but tiny volatility has a low beta — the scale matters for how much market risk you're actually exposed to.

### 3. Marginal risk contribution

When decomposing "how much does each position add to total portfolio risk," the cross-terms involve covariances. The units (%²) aren't pretty, but they're what the math needs.

---

**Mental model:** Correlation is for **comparison** ("does SPY co-move more with BND or with GLD?"). Covariance is for **computation** ("what's the actual portfolio variance?"). Different tools, different jobs.
