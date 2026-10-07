# 004 — Covariance and Correlation: How Assets Move Together

**Date:** 2026-07-22
**Topic:** What covariance and correlation actually measure, and how they shape the portfolio return distribution

---

## The question correlation answers

You have two return series. You want to know: when SPY has a bad day, does BND also tend to have a bad day? Or does BND tend to have a good day?

Correlation quantifies that tendency. It's a single number between −1 and +1 that summarises the historical pattern of co-movement.

---

## Part A: Covariance — the raw co-movement

### The intuition

Take one day. Multiply SPY's deviation from its average by BND's deviation from its average:

$$\text{Day's contribution} = (r_{\text{SPY}} - \bar{r}_{\text{SPY}}) \times (r_{\text{BND}} - \bar{r}_{\text{BND}})$$

| Scenario | SPY deviation | BND deviation | Product |
|----------|--------------|--------------|---------|
| Both above average | + | + | **+** |
| Both below average | − | − | **+** (negative × negative = positive) |
| SPY up, BND down | + | − | **−** |
| SPY down, BND up | − | + | **−** |

When they move together, the product is positive. When they move in opposite directions, the product is negative.

Covariance is the **average of these day-by-day products:**

$$\text{Cov}(X, Y) = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})$$

**Terms:**
- $x_i, y_i$ — return of asset X and asset Y on day $i$
- $\bar{x}, \bar{y}$ — sample mean return of each asset
- $n$ — number of observations
- $n-1$ — Bessel's correction (makes this an unbiased estimator of the population covariance — we'll revisit this when we cover estimation)

### Concrete example with 5 days

Recall our 5-day example from file 002:

| Day | SPY ($x_i$) | BND ($y_i$) | $x_i - \bar{x}$ | $y_i - \bar{y}$ | Product |
|-----|------------|------------|-----------------|-----------------|---------|
| 1 | +1.00% | +0.30% | +1.00 | +0.18 | +0.180 |
| 2 | −2.00% | +0.50% | −2.00 | +0.38 | **−0.760** |
| 3 | +0.50% | −0.10% | +0.50 | −0.22 | **−0.110** |
| 4 | −1.50% | −0.20% | −1.50 | −0.32 | +0.480 |
| 5 | +2.00% | +0.10% | +2.00 | −0.02 | −0.040 |

Means: $\bar{x} = 0.00\%$, $\bar{y} = 0.12\%$

Sum of products: $0.180 + (-0.760) + (-0.110) + 0.480 + (-0.040) = -0.250$

$$\text{Cov}(\text{SPY}, \text{BND}) = \frac{-0.250}{5-1} = -0.0625 \text{ (in \%²)}$$

The covariance is negative — meaning on average, when SPY is above its mean, BND tends to be below its mean, and vice versa. That's diversification-friendly.

### The problem with covariance

Covariance has ugly units (%²). And you can't compare a covariance of −0.0625 between SPY/BND with, say, a covariance of +0.0003 between SPY/GLD — the scales are completely different because the assets have different volatilities.

---

## Part B: Correlation — standardised covariance

Correlation fixes the units problem by dividing covariance by both assets' standard deviations:

$$\rho_{X,Y} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$$

**Terms:**
- $\rho_{X,Y}$ — correlation coefficient (dimensionless, always between −1 and +1)
- $\sigma_X = \sqrt{\text{Var}(X)}$ — standard deviation of asset X's returns
- $\text{Cov}(X, Y)$ — as defined above

Think of it as: **"How much of the way toward perfect co-movement do these assets go?"**

- $\rho = +1$: "Whatever X does, Y does exactly the same (scaled by volatility)." Zero diversification.
- $\rho = 0$: "X's move tells you nothing about Y's move." Full diversification benefit.
- $\rho = -1$: "Whatever X does, Y does the exact opposite." Maximum diversification.
- $\rho = -0.3$: "When X is above average, Y tends to be below average — but not perfectly. About 30% of the way toward perfect opposition."

### Why it's bounded between −1 and +1

This isn't obvious unless you've seen it. The intuition: correlation is a kind of inner product between mean-centered vectors. By the Cauchy-Schwarz inequality, the absolute value of the covariance can never exceed the product of the standard deviations. So dividing by $\sigma_X \sigma_Y$ forces the result into $[-1, 1]$.

---

## Part C: Connecting back to the portfolio return distribution

Now we can complete the picture from file 002. Remember: the portfolio return distribution is narrower than the individual distributions — that's diversification made visible.

**Correlation determines how much narrower.**

Consider SPY (σ ≈ 1% daily, say) and BND (σ ≈ 0.4% daily, say) in a 60/40 portfolio:

| Correlation (ρ) | What happens to portfolio VaR | Intuition |
|----------------|------------------------------|-----------|
| +1.0 | No benefit — portfolio return distribution is just a scaled blend of two perfectly synchronised series | Every bad day for SPY is also a bad day for BND. No cushion. |
| 0.0 | Meaningful benefit — losses in one asset are unrelated to losses in the other | About half the bad SPY days are offset by neutral or positive BND days |
| −0.3 | Strong benefit — BND tends to gain when SPY loses | Most bad SPY days are partially cushioned by BND |
| +0.5 | Weak benefit — assets still tend to move together, but imperfectly | Some cushion, but much less than you planned for |

And here's the crucial point for risk management: **correlation is not constant.** The ρ you estimate today from 252 days of history may not be the ρ you experience tomorrow. We'll get to that in Module 1D.

---

## Check-in

1. Does the day-by-day product intuition for covariance make sense — specifically, why "both below average" gives a positive product (negative × negative)?
2. Does correlation as "standardised covariance" click — why dividing by both σ's solves the units problem?
3. Can you see how the correlation number directly shapes the portfolio return distribution we talked about in file 002?
