# 1-Day VaR and Path-Dependency: When It Matters and When It Doesn't

**Date:** 2026-07-10
**Topic:** For 1-day VaR, GARCH still matters — but through a different mechanism than you might think

---

## Your Observation

For 1-day VaR, each path is one simulation. There's no multi-day sequence. So how can path-dependency (volatility clustering, autocorrelation) affect the 1-day VaR?

The short answer: **it doesn't affect the 1-day VaR directly through the path structure. It affects it through the current state of volatility.**

---

## Case 1: Simulating From a Distribution (No Process)

If you're just simulating from a distribution:

```python
simulated_returns = np.random.normal(mu, sigma, 10000)
var_95 = np.percentile(simulated_returns, 5)
```

Each draw is independent. The 1-day VaR is just the quantile of that distribution. There's no path structure, no dependence, no GARCH. This converges to the parametric VaR.

---

## Case 2: Simulating From GARCH — 1-Day VaR

With GARCH, the 1-day simulation still only needs one step per path. But that one step depends on **today's current volatility** — which was set by yesterday's return.

```
Path 1:  r₁ = μ + σ_current · z₁    ← σ_current is today's vol, computed from yesterday
Path 2:  r₂ = μ + σ_current · z₂
...
Path 10000: r₁₀₀₀₀ = μ + σ_current · z₁₀₀₀₀
```

**Each path is one step. But all paths use the same $\sigma_{\text{current}}$.** The $\sigma_{\text{current}}$ is computed from the GARCH equation using yesterday's actual return and yesterday's modeled variance.

So the GARCH 1-day VaR for today is:

$$\text{VaR}_{0.05} = \mu + \sigma_{\text{current}} \cdot z_{0.05}$$

**Terms:**
- $\sigma_{\text{current}}$: today's volatility, computed from GARCH using yesterday's data
- $z_{0.05}$: the 5th percentile of the standard normal = −1.6449

But wait — if $\sigma_{\text{current}}$ is just a number, and $z_{0.05}$ is just −1.6449, then this is... the parametric VaR formula with $\sigma_{\text{current}}$ instead of $\hat{\sigma}$.

**The GARCH 1-day VaR is parametric VaR with a time-varying volatility estimate.**

---

## So What Does Monte Carlo Actually Add for 1-Day VaR?

For 1-day VaR from a GARCH model, Monte Carlo adds nothing over the parametric formula. You already know $\sigma_{\text{current}}$ and you already know the quantile of the normal distribution.

**Monte Carlo earns its keep at two specific points:**

### 1. Multi-Period VaR (Horizon > 1 Day)

For 10-day VaR, you need the distribution of cumulative 10-day returns from a GARCH process. There's no formula for this. You must simulate 10,000 paths of 10 days each, where each day's $\sigma_t$ updates based on the previous day's return.

### 2. Non-Normal Shock Distributions

If you use GARCH with Student's t shocks instead of normal shocks:

$$r_t = \mu + \sigma_t \cdot \epsilon_t, \quad \epsilon_t \sim t(\nu)$$

The 1-day VaR is $\mu + \sigma_{\text{current}} \cdot t_{0.05}(\nu)$. You can compute this with `scipy.stats.t.ppf(0.05, df=ν)`. Monte Carlo still isn't needed for 1-day.

But if you want the 1-day VaR from a GARCH process with a **regime-switching** model or a **copula** for multi-asset dependence, the parametric formula breaks — and Monte Carlo is needed even for 1-day.

---

## The Real Picture

| Scenario | 1-Day VaR | 10-Day VaR |
|---|---|---|
| **Normal i.i.d.** | Formula: μ − z_α · σ̂ | √10 × 1-day (or formula) |
| **GARCH + normal shocks** | Formula: μ − z_α · σ_current | **Monte Carlo needed** |
| **GARCH + t-distribution shocks** | Formula: μ − t_α(ν) · σ_current | **Monte Carlo needed** |
| **GARCH + regime-switching** | **Monte Carlo needed** | **Monte Carlo needed** |
| **Multi-asset + copula** | **Monte Carlo needed** | **Monte Carlo needed** |

---

## Your Insight Is Correct

For 1-day VaR, the dependence structure (GARCH) matters through the **current state** — today's volatility is conditional on yesterday's return. But that's a single number, not a path. You can compute the 1-day VaR directly from that number.

It's only when you need a multi-period horizon (and the path matters) or when the model is complex enough that no closed-form quantile exists that Monte Carlo simulation is genuinely necessary.

---

## Check-In

Does this clarify the 1-day vs multi-day distinction? For 1-day GARCH, you don't need Monte Carlo — you just need $\sigma_{\text{current}}$, which GARCH gives you. For 10-day GARCH, you need to simulate paths because there's no formula for the 10-day distribution of a GARCH process.

And here's the practical implication: **at Spreadex, what's the VaR horizon?** If it's 1-day, Monte Carlo with GARCH adds nothing over a parametric formula with time-varying vol. If it's multi-day or if the portfolio has nonlinear instruments (options), Monte Carlo earns its keep.