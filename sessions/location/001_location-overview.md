# Location: Where Does the Distribution Sit?

**Session:** location  
**Topic:** Overview of location measures, moment connection, population vs sample  
**Prerequisites:** moments/001–005 (moments overview, empirical vs theoretical, true process, raw vs central, location-scale-shape)

---

## 1. What Is Location?

**Location is the answer to "where?"** — where on the number line does this distribution live?

Take three portfolios:

| Portfolio | Daily mean return | Where it sits |
|-----------|-------------------|---------------|
| A: Short-dated Treasuries | +0.01% | Just above zero |
| B: S&P 500 | +0.04% | Modestly positive |
| C: Leveraged crypto fund | +0.15% | Well into positive territory |

Each has a return distribution. Each distribution has a location — a single number that summarises "the centre." Location is property #1 of any distribution. Before you ask about variance or skewness, you ask: **where is it?**

---

## 2. The Three Location Measures

There are three canonical ways to answer "where is the centre?" — and they give different answers:

### 2.1 The Mean (Arithmetic Average)

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

Add up all the returns. Divide by n. That's the mean.

**Intuition:** The balance point. If you placed the distribution on a seesaw, the mean is where you'd put the fulcrum for it to balance.

**The mean IS the first raw moment.** $\mu'_1 = E[X] = \frac{1}{n}\sum x_i$.

### 2.2 The Median

Sort all the returns. Pick the middle one.

$$m = \text{the value at the 50th percentile}$$

If n is odd: it's the exact middle observation. If n is even: the average of the two middle observations.

**Intuition:** The halfway point. Half the observations are above it, half below. It doesn't care how far above or below — just which side.

**The median is NOT a moment.** You can't get it from a power of $x$. It's a quantile-based measure.

### 2.3 The Mode

The most frequently occurring value. The peak of the histogram.

**Intuition:** The "most typical" value. If you had to bet on tomorrow's return being one specific number, the mode is your best single guess (under a 0-1 loss function).

**The mode is NOT a moment either.** And it's rarely useful for continuous financial returns — every return is unique to many decimal places.

### 2.4 Visual Comparison

```
Normal-ish return distribution:

        ┌───┐
        │   │        mode = peak (most common)
        │  █│        median = halfway mark (50th percentile)
        │ ██│        mean = balance point (pulled RIGHT by right tail)
        │ ██│
   ─────┼─██┼─────
        │███│
        │███│
        │███│
        └───┘
         ↑ ↑↑
```

For symmetric distributions: mean = median = mode. For skewed distributions: they diverge. Which one is the "real" centre? That's the wrong question — they answer different versions of "centre."

---

## 3. The Mean as a Moment

### 3.1 It's the First Raw Moment

$$\mu'_1 = E[X] = \frac{1}{n}\sum_{i=1}^{n} x_i$$

This is the simplest possible moment: $k=1$, just the average. No centring, no standardising. Raw. Direct.

### 3.2 The First Central Moment Is Always Zero

$$\mu_1 = E[X - \mu] = 0$$

This is an identity — it's zero by construction, for any data. Centring by definition moves the distribution so its centre is at 0. That's why you never see "first central moment" discussed — it contains no information.

### 3.3 The Mean Is the Foundation for Everything Above It

Every higher moment depends on the mean:

| Moment | Depends on... |
|--------|---------------|
| Variance ($\mu_2$) | $\sum (x_i - \bar{x})^2$ — deviations from the mean |
| Skewness ($\mu_3$) | $\sum (x_i - \bar{x})^3$ — cubed deviations from the mean |
| Kurtosis ($\mu_4$) | $\sum (x_i - \bar{x})^4$ — fourth-power deviations from the mean |

If your mean estimate is bad, **every higher moment is contaminated.** The error propagates upward. This is why estimation quality of the mean matters — it's load-bearing for the entire moment structure.

### 3.4 The Mean in the Raw-vs-Central Bridge Formulas

From 004, the bridge formulas all start from raw moments:

$$\mu_2 = \mu'_2 - (\mu'_1)^2$$
$$\mu_3 = \mu'_3 - 3\mu'_1\mu'_2 + 2(\mu'_1)^3$$
$$\mu_4 = \mu'_4 - 4\mu'_1\mu'_3 + 6(\mu'_1)^2\mu'_2 - 3(\mu'_1)^4$$

$\mu'_1$ — the mean — appears in **every single bridge formula.** It's the anchor that all central moments are computed relative to.

---

## 4. Population vs Sample: $\mu$ vs $\bar{x}$

This distinction is fundamental. It's the same one from 002 (empirical vs theoretical) but applied specifically to location.

### 4.1 The Two Worlds

| | Population | Sample |
|---|---|---|
| **Symbol** | $\mu$ (mu) | $\bar{x}$ (x-bar) |
| **What it is** | The true, fixed, unknown mean of the return-generating process | An estimate computed from observed data |
| **Does it change?** | Not unless the process changes | Yes — every time you add a new day of data |
| **Can you know it?** | No — it's unobservable (003) | Yes — you just computed it |
| **Is it a random variable?** | No — it's a fixed parameter | Yes — different samples give different $\bar{x}$ |

### 4.2 The Estimation Problem

You observe 252 daily SPY returns. You compute $\bar{x} = 0.04\%$.

**Question:** Is the true $\mu$ exactly 0.04%?

**Answer:** Almost certainly not. If you'd observed a different 252-day window, you'd get a different $\bar{x}$. The observed mean is $\mu$ + sampling error.

$$\bar{x} = \mu + \varepsilon$$

Where $\varepsilon$ is the estimation error. Its expected value is zero (the sample mean is an unbiased estimator), but any specific $\bar{x}$ is off by *some* amount.

### 4.3 How Precise Is $\bar{x}$?

The standard error of the mean tells you how much $\bar{x}$ bounces around:

$$\text{SE}(\bar{x}) = \frac{\sigma}{\sqrt{n}}$$

| n (sample size) | SE (if $\sigma = 1\%$ daily) |
|-----------------|------------------------------|
| 21 (1 month) | 0.218% |
| 63 (1 quarter) | 0.126% |
| 252 (1 year) | 0.063% |
| 1260 (5 years) | 0.028% |

The precision scales with $\sqrt{n}$, not $n$. To halve your estimation error, you need 4× the data. A quarterly mean is roughly twice as precise as a monthly mean. A 5-year mean is roughly twice as precise as a 1-year mean.

**But there's a catch:** the process might change over 5 years. The bias-variance trade-off: more data reduces estimation variance but increases the risk that you're averaging over different regimes (structural breaks). This is why 252 days is the standard in VaR — it's a compromise between precision and relevance.

### 4.4 Daily Mean vs Annualised Mean

$$\mu_{\text{annual}} = 252 \times \mu_{\text{daily}}$$

If $\bar{x}_{\text{daily}} = 0.04\%$, then $\bar{x}_{\text{annual}} = 252 \times 0.04\% = 10.08\%$.

Same estimation problem, scaled by 252. If you're off by 0.01% on the daily mean, you're off by 2.52% on the annualised mean. Small daily errors compound.

---

## 5. Properties of Location Measures

### 5.1 Sensitivity to Outliers

Take five returns: −2%, −1%, 0%, +1%, +50% (the +50% is a freak day).

| Measure | Value | Affected by the +50%? |
|---------|-------|----------------------|
| Mean | 9.6% | **Heavily.** The +50% drags it way up |
| Median | 0% | **Not at all.** It's still the middle value |
| Mode | ~0% (depends on binning) | **Minimally** |

**The mean is not robust.** One extreme observation can shift it dramatically. This is a feature, not a bug — it means the mean reflects ALL the data, including the extremes that matter for finance. A 50% daily return *should* affect your summary.

But it also means the mean is highly sensitive to the particular sample you observed. If that +50% had been a −50% instead, your mean would be −10.4%. Same process, wildly different estimate. This is the trade-off.

### 5.2 The Loss Function Perspective

Each location measure is optimal under a different loss function — it minimises a different kind of "wrongness":

| Measure | Minimises | Penalises |
|---------|-----------|-----------|
| Mean | $\sum (x_i - c)^2$ | Squared error — large deviations punished heavily |
| Median | $\sum |x_i - c|$ | Absolute error — all deviations punished equally |
| Mode | Count of $x_i \neq c$ | 0-1 error — only exact matches count |

The mean is the answer to: "what single number $c$ minimises the sum of squared deviations?" That's why it squares deviations — the same reason variance does. The mean and variance are a matched pair: mean minimises squared error, variance measures squared deviations from that minimiser.

### 5.3 Asymptotic Properties

As $n \to \infty$:

| Property | Mean | Median |
|----------|------|--------|
| **Consistent?** | Yes — converges to $\mu$ | Yes — converges to population median |
| **Unbiased?** | Yes — $E[\bar{x}] = \mu$ | Approx. yes for symmetric distributions |
| **Efficient?** | Yes — minimum variance among unbiased estimators (for normal data) | Less efficient than mean for normal data, more efficient for fat-tailed data |

"For normal data" is the critical qualifier. Financial returns are NOT normal. For fat-tailed distributions, the median can actually be a more efficient estimator of location than the mean — the mean's variance gets blown up by the occasional extreme observation.

---

## 6. When to Use Which in Finance

| Scenario | Use | Why |
|----------|-----|-----|
| Computing expected return | Mean | You want the mathematical expectation — what you'd earn on average over many repetitions |
| Computing VaR (parametric) | Mean (in $\mu - z\sigma$) | The formula requires it |
| Describing "typical" return to a non-technical stakeholder | Median | "Half the days are better than this, half are worse" — instantly understood |
| Comparing fund performance when one had one freak month | Median | The mean is dominated by the outlier; median shows sustained performance |
| Testing whether a strategy has genuine edge | Mean | You need expected value, not typical value |
| Setting a conservative capital buffer | Median or trimmed mean | You don't want one good outlier making your buffer look adequate |

### 6.1 The Trimmed Mean — A Compromise

Discard the top and bottom $\alpha\%$ of observations, then take the mean of what's left.

For $\alpha = 5\%$ with 252 days: discard the 13 best and 13 worst days. Compute the mean of the remaining 226.

This gives you: robustness to outliers (like the median) + use of most of the data (like the mean). It's not commonly used in VaR but it's a useful concept to know.

---

## 7. Link to VaR

### 7.1 Parametric VaR

$$\text{VaR}_{95\%} = -(\mu - 1.645\sigma)$$

The mean $\mu$ is right there in the formula. If you overestimate $\mu$ by 0.01% daily, you underestimate VaR by the same 0.01% daily — about 2.5% annualised. That's material for a risk limit.

But note: for a 1-day VaR, the mean term is usually tiny compared to the $\sigma$ term:

$$\text{VaR}_{95\%} = -(0.04\% - 1.645 \times 1.2\%) = -(0.04\% - 1.974\%) = 1.934\%$$

The mean contributes 0.04% out of 1.934% — about 2%. The volatility term dominates. This is why some practitioners set $\mu = 0$ for 1-day VaR — it barely matters. But for 10-day or longer VaR, the mean scales linearly with time while volatility scales with $\sqrt{10}$, so the mean becomes more important.

### 7.2 Historical VaR

Historical VaR doesn't use the mean explicitly — it just sorts and picks a quantile. But the mean is still implicitly there: the entire distribution's location matters. A distribution shifted 0.1% to the right will have a 0.1% better VaR (approximately).

### 7.3 Expected Shortfall (CVaR)

Expected Shortfall — the average of returns beyond VaR — does NOT use $\mu$ directly. But again, location matters. Shift the whole distribution right and ES improves.

### 7.4 Horizon Effects

For a h-day VaR, the mean scales linearly:

$$\mu_h = h \times \mu_1$$

If daily $\mu = 0.04\%$, 10-day $\mu = 0.4\%$.

But volatility scales with $\sqrt{h}$:

$$\sigma_h = \sqrt{h} \times \sigma_1$$

This means **the mean grows faster than the volatility as horizon increases.** For a 1-day VaR the mean is negligible. For a 1-year VaR it's the dominant term. The location property matters more at longer horizons.

---

## 8. Phase 1 Connections

| Phase 1 notebook / concept | How location connects |
|----------------------------|----------------------|
| **`np.mean(returns)`** | This IS the first raw moment estimate. Every notebook computes it |
| **Parametric VaR: $\mu - 1.645\sigma$** | $\mu$ is the location component. The $1.645\sigma$ is the scale-tail component |
| **Vol scaling** | When you scale $\mu$ by $h$ and $\sigma$ by $\sqrt{h}$, the relative importance of location grows with horizon |
| **Decay weighting** | An EWMA mean weights recent observations more — it's a local location estimate, tracking a process that might be drifting |
| **Combined method** | The weighted average of parametric and historical VaR implicitly blends location assumptions |
| **QQ plots** | If the points deviate from the 45° line by a constant offset, that's a location mismatch — the theoretical distribution is centred in the wrong place |
| **Rolling windows** | Each 252-day window gives a different $\bar{x}$ — you're watching the location estimate evolve through time |

---

## 9. Summary

| Concept | Key Point |
|---------|-----------|
| **What is location?** | Where the distribution sits on the number line |
| **Three measures** | Mean (balance point), median (halfway mark), mode (peak) |
| **Mean = first raw moment** | $\mu'_1 = \frac{1}{n}\sum x_i$ — the foundation for all higher moments |
| **$\mu$ vs $\bar{x}$** | $\mu$ is the true, unobservable population mean. $\bar{x}$ is an estimate that bounces around with sampling error |
| **Standard error** | $\sigma/\sqrt{n}$ — precision improves slowly, with the square root of sample size |
| **Sensitivity** | Mean is sensitive to outliers (a feature for finance). Median is robust (a feature for communication) |
| **In VaR** | The mean appears directly in parametric VaR but matters little for 1-day horizons. It grows in importance at longer horizons |

---

## 10. Check-in Questions

1. **What's the difference between "where is the centre?" (location) and "what is the typical value?" (could be mode, median, or mean depending on what "typical" means)?**

2. **If $\bar{x}_{\text{daily}} = 0.05\%$, $\sigma_{\text{daily}} = 1.5\%$, and $n = 252$, compute the standard error of the mean. What's the 95% confidence interval for $\mu$? (Use ±1.96 SE.) Is zero inside that interval?**

3. **Why does the mean appear in every central moment formula even though central moments are "mean-free"?**

4. **A portfolio has a great year: $\bar{x}_{\text{daily}} = 0.15\%$. But one day was +8% (earnings surprise on a concentrated position). Without that day, $\bar{x}_{\text{daily}} = 0.12\%$. How should you think about the "true" location of this strategy?**

5. **If you're computing a 1-day parametric VaR, how much does a 0.01% error in $\bar{x}$ actually matter? Work it out: $\sigma = 1.5\%$, compare VaR with $\mu = 0.04\%$ vs $\mu = 0.05\%$.**

6. **The standard error formula $\sigma/\sqrt{n}$ assumes independent observations. Real returns have volatility clustering — big days tend to follow big days. Does that make the true standard error bigger or smaller than the formula suggests? Why?**