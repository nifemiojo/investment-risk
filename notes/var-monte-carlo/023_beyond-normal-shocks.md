# Beyond Normal Shocks: Distribution Choice in GARCH

**Date:** 2026-07-10
**Topic:** The shock distribution is a modeling choice — and changing it changes everything

---

## The General GARCH Form

$$r_t = \mu + \sigma_t \cdot \epsilon_t, \quad \epsilon_t \sim D(0,1)$$

**Terms:**
- $\epsilon_t$: the standardized shock — always mean 0, variance 1
- $D(0,1)$: any distribution you choose, standardized to mean 0, variance 1
- $\sigma_t$: the conditional volatility from GARCH

The GARCH equation itself doesn't change:

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \sigma_{t-1}^2$$

The only thing that changes is the distribution you draw $\epsilon_t$ from.

---

## Why Change It?

Even after accounting for time-varying volatility (via GARCH), the standardized residuals $\hat{\epsilon}_t = r_t / \hat{\sigma}_t$ often still have **fatter tails than normal.** The GARCH model captures volatility clustering, but the remaining shocks are still more extreme than normal would predict.

You can test this: fit a GARCH with normal shocks, extract the standardized residuals, and check their kurtosis. If kurtosis > 3 (normal = 3), the tails are fatter than normal. This is almost always the case for financial returns.

---

## Common Choices

### 1. Student's t-Distribution

$$\epsilon_t \sim t(\nu), \quad \text{scaled to variance 1}$$

**Terms:**
- $\nu$: degrees of freedom — lower = fatter tails
- $\nu \to \infty$: converges to normal
- $\nu \approx 4$–8: typical for daily financial returns

The t-distribution adds one parameter (ν) and captures the fat tails that remain after GARCH removes volatility clustering. The 1-day VaR becomes:

$$\text{VaR}_{0.05} = \mu + \sigma_t \cdot t_{0.05}(\nu)$$

where $t_{0.05}(\nu)$ is the 5th percentile of the standardized t-distribution. For ν = 4, this is about −2.13 (vs −1.64 for normal) — roughly 30% wider.

### 2. Generalized Error Distribution (GED)

$$\epsilon_t \sim \text{GED}(\kappa)$$

**Terms:**
- $\kappa$: shape parameter
- $\kappa = 2$: normal distribution
- $\kappa < 2$: fatter tails than normal
- $\kappa > 2$: thinner tails than normal

The GED is more flexible than the t — it can model both fatter and thinner tails.

### 3. Skewed Distributions

Standard t and GED are symmetric, but you already noted that returns can be asymmetric (leverage effect). Skewed versions add a skewness parameter:

- **Skewed Student's t:** ν (tail fatness) + λ (skewness)
- **Skewed GED:** κ (tail shape) + λ (skewness)

These capture both the fat tails AND the asymmetry (crashes more extreme than rallies).

---

## What This Changes

### For 1-Day VaR

| Shock Distribution | 1-Day VaR Formula | Extra Parameters |
|---|---|---|
| Normal | $\mu + \sigma_t \cdot z_\alpha$ | 0 |
| Student's t | $\mu + \sigma_t \cdot t_\alpha(\nu)$ | 1 (ν) |
| Skewed-t | $\mu + \sigma_t \cdot st_\alpha(\nu, \lambda)$ | 2 (ν, λ) |

The formula still works for 1-day if you can compute the quantile. `scipy` handles all of these.

### For 10-Day VaR

No formula exists for any of these. You must simulate. And the choice of shock distribution **changes the 10-day VaR substantially** — fat-tailed shocks produce more extreme multi-day paths.

---

## The Modeling Hierarchy

```
GARCH(1,1) with normal shocks     ← simplest, 3 params (ω, α, β)
    ↓
GARCH(1,1) with Student's t       ← adds ν, captures residual fat tails
    ↓
GARCH(1,1) with skewed-t          ← adds ν + λ, captures fat tails + asymmetry
    ↓
GJR-GARCH with skewed-t           ← adds γ (leverage) + ν + λ, full asymmetry
```

Each layer adds a parameter and captures a real empirical feature. Each layer also adds estimation risk. The question is always: **does the added complexity improve the VaR forecast enough to justify the extra parameter uncertainty?**

---

## The Monte Carlo Connection

This is another place where Monte Carlo earns its keep. You can simulate from a GJR-GARCH with skewed-t shocks for 10-day VaR. That's 6 parameters (ω, α, β, γ, ν, λ) governing a process with no closed-form 10-day distribution. The only way to get the VaR is simulation.

And this is also a Monte Carlo failure mode: **with 6 parameters, you have 6 ways to be wrong.** The model is flexible but fragile. Estimation error in any one parameter propagates through the simulation.

---

## Check-In

The shock distribution is a modeling choice, not a fixed assumption. The standard normal is just the simplest starting point. In practice, you'd almost always use at least Student's t — the fat tails in financial returns survive even after GARCH removes volatility clustering.

Does this connect back to your earlier question about variance being symmetric? The skewed distributions (skewed-t, skewed-GED) are the direct fix: they model the asymmetry you identified without needing a separate semi-variance framework.