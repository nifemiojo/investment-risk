# 011 — Where the Naive Sum Comes From: Portfolio VaR Under ρ = +1

**Date:** 2026-07-22
**Topic:** Deriving why the weighted sum of individual VaRs is the "no diversification" baseline

---

## Starting point: portfolio variance

For two assets with weights $w_1, w_2$, the portfolio variance is:

$$\sigma_p^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\,\text{Cov}(r_1, r_2)$$

**Terms:**
- $\sigma_p^2$ — portfolio return variance
- $w_1, w_2$ — portfolio weights (sum to 1)
- $\sigma_1^2, \sigma_2^2$ — individual asset return variances
- $\text{Cov}(r_1, r_2)$ — covariance between the two return series

## Substitute ρ = +1

When ρ = +1, the covariance is $\text{Cov}(r_1, r_2) = \rho\,\sigma_1\sigma_2 = \sigma_1\sigma_2$.

Plug in:

$$\sigma_p^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\sigma_1\sigma_2$$

This is a perfect square:

$$\sigma_p^2 = (w_1\sigma_1 + w_2\sigma_2)^2$$

So:

$$\sigma_p = w_1\sigma_1 + w_2\sigma_2$$

**The portfolio's volatility is exactly the weighted sum of individual volatilities.** No diversification benefit at the variance level — the cross-term adds fully, with no discount from imperfect correlation.

## From volatility to VaR

For parametric VaR under a normal distribution with zero mean:

$$\text{VaR}_i = z \times \sigma_i$$

where $z$ is the z-score for the confidence level (e.g. $z = 1.645$ for 95%).

Then the portfolio VaR under ρ = +1:

$$\text{VaR}_p = z \times \sigma_p = z \times (w_1\sigma_1 + w_2\sigma_2)$$

$$= w_1(z\sigma_1) + w_2(z\sigma_2) = w_1\text{VaR}_1 + w_2\text{VaR}_2$$

**Under perfect correlation, portfolio VaR = weighted sum of individual VaRs.**

---

## What this means

The weighted sum $w_1\text{VaR}_1 + w_2\text{VaR}_2$ is the **worst-case portfolio VaR** — the risk you'd have if the assets moved in perfect lockstep. It's the "no diversification" baseline.

Any actual portfolio VaR below that baseline is the diversification benefit:

$$\text{Diversification benefit} = \frac{w_1\text{VaR}_1 + w_2\text{VaR}_2 - \text{VaR}_p}{w_1\text{VaR}_1 + w_2\text{VaR}_2}$$

Concrete example (60/40 SPY/BND):

$$\text{Naive sum} = 0.60 \times 2.0\% + 0.40 \times 1.0\% = 1.60\%$$

If actual portfolio VaR is 1.15%:

$$\text{Benefit} = \frac{1.60\% - 1.15\%}{1.60\%} = 28.1\%$$

---

## A note on the unweighted form

The plan uses an unweighted sum in its formula: $\sum \text{VaR}_i = \text{VaR}_1 + \text{VaR}_2 = 2\% + 1\% = 3\%$. This form makes sense when the VaR numbers are already in **currency terms** (dollars per position) — then adding them gives total dollar risk in the worst case, and the weights are implicit in the position sizes.

But in percentage terms, the weighted form is correct: $w_1\text{VaR}_1 + w_2\text{VaR}_2$. The two are equivalent if the VaRs are expressed as a percentage of the *same base* (total portfolio value). I'll use the weighted form going forward.

---

## Check-in

1. Does the algebra from $\sigma_p^2$ to $(w_1\sigma_1 + w_2\sigma_2)^2$ at ρ = +1 make sense — specifically why $2w_1w_2\sigma_1\sigma_2$ completes the square?
2. Can you see why $w_1\text{VaR}_1 + w_2\text{VaR}_2$ is the ρ = +1 worst case regardless of the VaR method (historical, parametric, etc.)? Or is the normality assumption needed?
