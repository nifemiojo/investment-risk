# Practical Limitations of Parametric VaR and How Practitioners Mitigate Them

**Date:** 2026-07-07
**Topic:** What goes wrong with parametric VaR in practice and the toolkit practitioners use to fix it

---

## The Framework

Every limitation flows from one of two sources:

1. **The model is wrong** (normality doesn't hold)
2. **The parameters are wrong** (μ̂, σ̂ are noisy estimates)

And every mitigation is either: fix the model, fix the estimates, or accept the error and build safeguards around it.

---

## Limitation 1: The Normality Assumption Is Wrong

### The Problem

Real returns have:
- **Fat tails** (kurtosis > 3): extreme events happen more often than normal predicts
- **Negative skew**: crashes are more severe than rallies
- **Asymmetric tails**: the left tail is fatter than the right

Consequence: parametric VaR **underestimates tail risk**. For a 99% VaR, the error is worse than for 95% because you're deeper in the tail where normality fails most dramatically.

```
Normal says:   P(loss > 3σ) ≈ 0.135%  →  once every 3.7 years
Reality:       P(loss > 3σ) ≈ 0.5%    →  once every year
```

### Mitigations

**A. Switch to a fatter-tailed distribution.**

| Distribution | Solves | Cost |
|---|---|---|
| Student's t | Fat tails | Extra parameter ν to estimate |
| Generalized Error (GED) | Flexible tail thickness | Extra parameter β |
| Skewed t | Fat tails + asymmetry | Two extra parameters (ν, α) |

Most common in practice: **Student's t with ν ≈ 3–6** for daily equity returns.

**B. Cornish-Fisher expansion.**

Instead of switching distributions, you adjust the normal quantile using sample skewness ($S$) and kurtosis ($K$):

$$z_{\text{CF}} = z_{\alpha} + \frac{S}{6}(z_{\alpha}^2 - 1) + \frac{K-3}{24}(z_{\alpha}^3 - 3z_{\alpha}) - \frac{S^2}{36}(2z_{\alpha}^3 - 5z_{\alpha})$$

**Terms:**
- $z_{\text{CF}}$: the Cornish-Fisher adjusted Z-score
- $z_{\alpha}$: the standard normal quantile (e.g., 1.6449 for 95%)
- $S$: sample skewness
- $K$: sample excess kurtosis ($K = 0$ for normal)

If $S$ is negative (crash skew) and $K$ is positive (fat tails), $z_{\text{CF}} > z_{\alpha}$ — the adjusted VaR is larger in magnitude.

**Why this is clever:** You keep the normal framework but correct for the most important non-normalities. No new distribution to fit. Just four sample moments.

**C. Extreme Value Theory (EVT).**

Instead of modeling the whole distribution, model only the tail using a generalized Pareto distribution. This is for when you care specifically about the 1% and 0.1% quantiles and don't want the body of the distribution to influence your tail model.

---

## Limitation 2: The Mean Is Hard to Estimate

### The Problem

The standard error of the sample mean is:

$$\text{SE}(\hat{\mu}) = \frac{\sigma}{\sqrt{n}}$$

For $\sigma = 1.2\%$ and $n = 252$:

$$\text{SE}(\hat{\mu}) = \frac{1.2\%}{\sqrt{252}} = 0.076\%$$

Your estimate $\hat{\mu} = 0.04\%$ has a standard error of 0.076%. The 95% confidence interval for the true μ is roughly $[-0.11\%, +0.19\%]$ — it could be negative!

**The mean is the noisiest parameter.** For short horizons (1-day, 1-week), the mean contributes very little to VaR anyway — the volatility term dominates. Including a noisy mean just adds error.

### Mitigation

**Set μ = 0 for short-horizon VaR.**

$$\text{VaR}_{95\%} \approx -z_{\alpha} \cdot \sigma$$

For 1-day VaR, the mean term (μ̂) is typically 0.01–0.05% while the volatility term (z·σ̂) is 1–3%. The mean is lost in the noise. Setting it to zero simplifies and removes a source of estimation error.

**When NOT to do this:** Longer horizons (monthly, quarterly) where the mean accumulates and matters. For 10-day VaR, μ̂ contributes roughly 10× more and shouldn't be zeroed.

---

## Limitation 3: Volatility Changes Over Time

### The Problem

The parametric method treats $\hat{\sigma}$ as a constant estimated from equally-weighted historical data. But volatility is **time-varying**:

```
2020: σ ≈ 35% (COVID)
2021: σ ≈ 12% (recovery)
2022: σ ≈ 25% (bear market)
2023: σ ≈ 15% (stabilization)
```

A single $\hat{\sigma}$ from the past 252 days mixes these regimes. If you're in a calm period, it overestimates. If you're entering a crisis, it underestimates — badly.

This is the **regime change problem** you identified in the historical VaR limitations session. It applies here too.

### Mitigations

**A. Exponentially Weighted Moving Average (EWMA).**

Weight recent observations more heavily:

$$\hat{\sigma}_t^2 = \lambda \cdot \hat{\sigma}_{t-1}^2 + (1-\lambda) \cdot r_{t-1}^2$$

**Terms:**
- $\hat{\sigma}_t^2$: variance estimate for day $t$
- $\lambda$: decay factor (typically 0.94 for daily data, from RiskMetrics)
- $r_{t-1}$: yesterday's return

With $\lambda = 0.94$, the effective sample half-life is about 11 days. Recent data dominates. When vol spikes, EWMA catches it quickly.

**B. GARCH(1,1).**

Generalizes EWMA by adding a long-run variance term:

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \sigma_{t-1}^2$$

**Terms:**
- $\omega$: long-run variance component
- $\alpha$: reaction to recent shocks (news impact)
- $\beta$: persistence of volatility
- $\alpha + \beta$: must be < 1 for stationarity (typically 0.95–0.99 for financial data)

GARCH captures mean-reversion in volatility — vol spikes, then decays back to long-run average. More realistic than constant σ̂.

**C. Implied volatility (from options).**

Skip historical data entirely. Use VIX or at-the-money option implied vol as your σ estimate. This is forward-looking — it embeds the market's expectation of future volatility.

**Tradeoff:** Implied vol is forward-looking but includes a risk premium (tends to overestimate). Historical vol is backward-looking but unbiased.

---

## Limitation 4: The √t Scaling Rule for Multi-Day VaR

### The Problem

To go from 1-day VaR to 10-day VaR, the standard approach is:

$$\text{VaR}_{10\text{-day}} = \sqrt{10} \times \text{VaR}_{1\text{-day}}$$

This assumes:
- Returns are **independent** across days (no autocorrelation)
- Returns are **identically distributed** (volatility is constant)
- Returns are **normal** (the distribution shape is preserved under scaling)

All three assumptions are wrong. Returns have autocorrelation (momentum, mean-reversion), volatility clusters, and the distribution changes shape as you aggregate.

### Mitigation

**A. Use overlapping multi-day returns directly.**

Instead of scaling 1-day returns, compute 10-day overlapping returns from your data and estimate VaR directly on those. This preserves the actual distribution shape and any autocorrelation structure.

**B. Adjust for autocorrelation.**

If returns have first-order autocorrelation ρ, the scaling factor is:

$$\text{Scaling factor} = \sqrt{h + 2\sum_{k=1}^{h-1}(h-k)\rho_k}$$

**Terms:**
- $h$: the horizon in days (e.g., 10)
- $\rho_k$: the autocorrelation at lag $k$

For positive autocorrelation (momentum), this is > √h. For negative (mean-reversion), it's < √h.

**C. Monte Carlo simulation** (the third VaR method, which we'll cover separately).

---

## Limitation 5: The Data Window Is Arbitrary

### The Problem

252 days? 500 days? 1000 days? Your choice changes the VaR meaningfully.

| Window | Implication |
|---|---|
| Short (60 days) | Very responsive to recent regime, very noisy |
| Medium (252 days) | Standard choice, balances responsiveness and stability |
| Long (1000 days) | Stable estimates, includes old regimes that may be irrelevant |

There's no "correct" answer. The window is a judgment call.

### Mitigation

**A. Use a decay factor** (EWMA) rather than a hard cutoff. This avoids the cliff edge where day 253 suddenly drops out of your window.

**B. Run multiple windows and watch the divergence.** If 60-day VaR and 252-day VaR are very different, that's a signal — the recent regime is different from the longer history. Don't pick one; monitor the spread.

**C. Backtest to calibrate.** Choose the window that would have produced the best-calibrated VaR (breaches ≈ α% of the time) over a validation period.

---

## Limitation 6: Portfolios Need Correlations

### The Problem

For a portfolio of $N$ assets, parametric VaR requires the covariance matrix:

$$\sigma_{\text{portfolio}} = \sqrt{\mathbf{w}^T \Sigma \mathbf{w}}$$

**Terms:**
- $\mathbf{w}$: vector of portfolio weights ($N \times 1$)
- $\Sigma$: covariance matrix ($N \times N$)
- $\mathbf{w}^T \Sigma \mathbf{w}$: portfolio variance

For $N = 50$ assets, you need to estimate $50$ variances + $1225$ covariances = $1275$ parameters. With 252 days of data, that's 0.2 observations per parameter. The covariance matrix is **noisy and unstable.**

And correlations break in crises — exactly when you need them most.

### Mitigations

**A. Shrinkage estimators.** Blend the sample covariance matrix with a structured target (e.g., constant correlation, single-factor model). This pulls extreme estimates toward the center and reduces estimation error.

**B. Factor models.** Instead of modeling all pairwise correlations, model each asset's exposure to a few common factors:

$$r_i = \alpha_i + \beta_{i,1}F_1 + \beta_{i,2}F_2 + \cdots + \epsilon_i$$

For 50 assets and 3 factors, you estimate 50×3 = 150 betas instead of 1225 correlations. Dramatically fewer parameters.

**C. Stress correlations.** Don't rely on the historical correlation matrix. Test what happens to portfolio VaR when correlations jump to crisis levels (e.g., all correlations → 0.7).

---

## Limitation 7: It Gives a Single Number

### The Problem

Parametric VaR outputs: "-1.297%". That's it. One number.

It doesn't tell you:
- What happens beyond -1.297% (how bad are the 5% of days?)
- How sensitive the number is to your assumptions
- Whether the model is well-calibrated to recent data

### Mitigation

**A. Always report alongside Expected Shortfall (CVaR).** ES tells you the average loss on the days you breach VaR. VaR is the fence; ES is what's on the other side of it.

**B. Sensitivity analysis.** Report VaR under different windows, different distributions, different decay factors. Show the range, not just the point estimate.

**C. Backtesting.** Track whether actual breaches occur at the expected frequency. If 95% VaR is breached 8% of the time, your model is understating risk. Adjust.

---

## The Practitioner's Toolkit — Summary

| Limitation | Primary Mitigation | Secondary |
|---|---|---|
| Normality is wrong | Student's t or Cornish-Fisher | EVT for deep tails |
| Mean is noisy | Set μ = 0 for short horizons | Bayesian shrinkage |
| Vol changes over time | EWMA (λ ≈ 0.94) | GARCH, implied vol |
| √t scaling is wrong | Use overlapping returns | Adjust for autocorrelation |
| Window is arbitrary | EWMA decay | Multi-window monitoring |
| Correlations needed | Factor models | Shrinkage, stress testing |
| Single number output | Report with ES | Sensitivity analysis, backtesting |

---

## The Meta-Lesson

Every parametric VaR number you see in production is the output of a chain of decisions:

```
Choose distribution → choose estimation method → choose window → choose horizon → get number
```

The number is only as good as the weakest link in that chain. Practitioners who understand this don't trust the number — they trust the **process** that produces it, and they monitor it continuously.

---

## Check-In

At Spreadex, you're likely running parametric VaR for autohedging. If volatility suddenly spikes from 15% to 35% (like COVID), which mitigation would catch this fastest: EWMA, GARCH, or implied volatility? And why?