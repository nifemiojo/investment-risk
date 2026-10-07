# Sample Moments — Estimating Distribution Shape from Data

**Date:** 2026-07-26
**Topic:** How moments are computed from the empirical distribution, why the formulas look the way they do, and how much you should trust each estimate.

---

## Opening Question

> You have 252 SPY returns. You want to describe their distribution: centre, spread, asymmetry, tail weight. You reach for the sample mean, sample variance, sample skewness, sample kurtosis. But which formula? Why does variance divide by $n-1$ while skewness divides by $n$? Why does SciPy's `kurtosis` subtract 3? Why should you trust the mean more than the kurtosis? Every formula is a choice — and every choice has a reason.

---

## 1. Sample Moments vs Population Moments — the Estimation Framework

Recall the chain from earlier sessions:

```
True process → True distribution → Parameters (μ, σ², γ₁, γ₂)
                                              ↑
                                        we estimate these
                                              │
Observed data → Empirical distribution → Sample moments (x̄, s², g₁, g₂)
```

A **population moment** is a property of the theoretical distribution. $\mu = E[X]$ is the true mean — a fixed number you'll never know.

A **sample moment** is a function of your data — a number you compute. $\bar{x} = \frac{1}{n}\sum x_i$ is an estimate of $\mu$.

The **estimator** is the formula (the rule for computing it from data). The **estimate** is the number you get when you apply the formula to a specific sample.

| | Estimator (the formula) | Estimate (the number) |
|---|---|---|
| Mean | $\hat{\mu} = \frac{1}{n}\sum X_i$ | $\bar{x} = 0.04\%$ |
| Variance | $\hat{\sigma}^2 = \frac{1}{n-1}\sum (X_i - \bar{X})^2$ | $s^2 = 1.44$ |

The estimator is a random variable (it changes with each sample). The estimate is a realisation of that random variable given your specific data. When we talk about properties like "bias" or "variance" of a moment, we're talking about the estimator — its behaviour across repeated sampling.

---

## 2. The Four Sample Moments — Formulas and Intuition

### 2.1 Sample Mean (First Raw Moment)

$$\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i$$

**Why this formula:** It's the arithmetic average. For the empirical distribution — where each observation has probability $1/n$ — this is exactly the expected value: $E_{\text{empirical}}[X] = \sum x_i \cdot \frac{1}{n} = \bar{x}$.

**Why divide by $n$ (not $n-1$):** The sample mean is an unbiased estimator of the population mean with denominator $n$. No correction needed. $E[\bar{X}] = \mu$ exactly.

### 2.2 Sample Variance (Second Central Moment)

$$s^2 = \frac{1}{n-1}\sum_{i=1}^n (x_i - \bar{x})^2$$

**Why this formula:** Variance is the average squared deviation from the mean. We square so that positive and negative deviations both contribute positively, and larger deviations are weighted more heavily.

**Why divide by $n-1$ (not $n$):** This is Bessel's correction. If you divided by $n$, the estimator would be biased downward — it would systematically underestimate the true variance. The reason: $\bar{x}$ is itself estimated from the same data, and it's always pulled toward the data points, making deviations $(x_i - \bar{x})$ slightly smaller than the true deviations $(x_i - \mu)$ would be. Dividing by $n-1$ compensates for this.

Full derivation in Section 3.

### 2.3 Sample Skewness (Third Standardised Central Moment)

$$g_1 = \frac{\frac{1}{n}\sum_{i=1}^n (x_i - \bar{x})^3}{\left(\frac{1}{n}\sum_{i=1}^n (x_i - \bar{x})^2\right)^{3/2}}$$

Or equivalently, the **adjusted** (unbiased) version:

$$G_1 = \frac{\sqrt{n(n-1)}}{n-2} \cdot g_1$$

**Why divide by $n$ in the numerator but $n-1$ is complicated here:** The standardised moment is a ratio — the third central moment divided by the cube of the standard deviation. Both numerator and denominator are estimated with bias. The bias correction for the ratio is messy and depends on $n$. The simple $g_1$ with denominator $n$ is what most software returns by default (NumPy, SciPy's `skew` with `bias=True`). The adjusted $G_1$ (SciPy's default with `bias=False`) corrects for small-sample bias.

**Why cubed:** Cubing preserves the sign — negative deviations stay negative, positive stay positive. If the left tail is fatter (more extreme negative than positive), the sum of cubes is negative → negative skewness.

### 2.4 Sample Kurtosis (Fourth Standardised Central Moment)

$$g_2 = \frac{\frac{1}{n}\sum_{i=1}^n (x_i - \bar{x})^4}{\left(\frac{1}{n}\sum_{i=1}^n (x_i - \bar{x})^2\right)^2} - 3$$

**Why divide by $n$:** Same as skewness — the simple version uses $n$ in numerator and denominator. The adjusted (unbiased) version exists but is complex and sample-size-dependent.

**Why the fourth power:** The fourth power makes extreme deviations enormous — a 3σ event contributes $3^4 = 81$ times as much as a 1σ event to the sum. This makes kurtosis exquisitely sensitive to tail observations.

**Why subtract 3:** A normal distribution has kurtosis = 3. Subtracting 3 gives "excess kurtosis" — zero means normal tails, positive means fatter than normal, negative means thinner than normal. SciPy's `kurtosis` returns excess kurtosis by default. NumPy doesn't — it returns raw kurtosis. This discrepancy has caused countless bugs.

> **Practical rule: always check what your library returns.** SciPy `kurtosis` = excess (subtracted 3). NumPy doesn't have a direct kurtosis function. Pandas `kurtosis` = excess by default. When in doubt, test with `np.random.normal(size=10000)` — it should give approximately 0 for excess, 3 for raw.

---

## 3. Why $n-1$ for Variance — Full Derivation

This is the most important formula in sample moments. Let's derive it properly.

### Step 1: Define the naive estimator (denominator $n$)

$$\hat{\sigma}^2_{\text{naive}} = \frac{1}{n}\sum_{i=1}^n (X_i - \bar{X})^2$$

We want to know: is this unbiased? That is, does $E[\hat{\sigma}^2_{\text{naive}}] = \sigma^2$?

### Step 2: Expand $(X_i - \bar{X})^2$

We can't directly take the expectation of $(X_i - \bar{X})^2$ because $\bar{X}$ is also random. The trick: add and subtract $\mu$:

$$X_i - \bar{X} = (X_i - \mu) - (\bar{X} - \mu)$$

So:

$$(X_i - \bar{X})^2 = (X_i - \mu)^2 - 2(X_i - \mu)(\bar{X} - \mu) + (\bar{X} - \mu)^2$$

### Step 3: Sum over $i$

$$\sum_{i=1}^n (X_i - \bar{X})^2 = \sum_{i=1}^n (X_i - \mu)^2 - 2(\bar{X} - \mu)\sum_{i=1}^n (X_i - \mu) + n(\bar{X} - \mu)^2$$

Now, $\sum_{i=1}^n (X_i - \mu) = n(\bar{X} - \mu)$, so the middle term simplifies:

$$-2(\bar{X} - \mu) \cdot n(\bar{X} - \mu) = -2n(\bar{X} - \mu)^2$$

And the full sum:

$$\sum_{i=1}^n (X_i - \bar{X})^2 = \sum_{i=1}^n (X_i - \mu)^2 - 2n(\bar{X} - \mu)^2 + n(\bar{X} - \mu)^2$$

$$= \sum_{i=1}^n (X_i - \mu)^2 - n(\bar{X} - \mu)^2$$

### Step 4: Take expectations

$$E\left[\sum (X_i - \bar{X})^2\right] = \sum E[(X_i - \mu)^2] - n \cdot E[(\bar{X} - \mu)^2]$$

- $E[(X_i - \mu)^2] = \sigma^2$ for each $i$ (definition of variance)
- $E[(\bar{X} - \mu)^2] = \text{Var}(\bar{X}) = \frac{\sigma^2}{n}$ (variance of the sample mean)

So:

$$E\left[\sum (X_i - \bar{X})^2\right] = n\sigma^2 - n \cdot \frac{\sigma^2}{n} = n\sigma^2 - \sigma^2 = (n-1)\sigma^2$$

### Step 5: The punchline

$$E\left[\frac{1}{n}\sum (X_i - \bar{X})^2\right] = \frac{n-1}{n}\sigma^2 \neq \sigma^2$$

**The naive estimator with denominator $n$ is biased downward** — it gives $\frac{n-1}{n}\sigma^2$ on average, which is less than $\sigma^2$.

But:

$$E\left[\frac{1}{n-1}\sum (X_i - \bar{X})^2\right] = \sigma^2$$

**Dividing by $n-1$ fixes the bias.** This is Bessel's correction. It's not arbitrary — it falls directly out of the algebra.

### Why $n-1$ and not $n-2$ or something else?

Because we "lost" one degree of freedom by estimating $\bar{x}$ from the data. The deviations $(x_i - \bar{x})$ are not independent — they must sum to zero. If you know $n-1$ of them, the last one is determined. So there are only $n-1$ independent pieces of information about spread in the sample. Dividing by $n-1$ reflects this.

### The $n-1$ shrinks as $n$ grows

For $n = 10$: $\frac{n-1}{n} = 0.90$ — the bias is 10%. Meaningful.
For $n = 252$: $\frac{n-1}{n} = 0.996$ — the bias is 0.4%. Negligible for most purposes.
As $n \to \infty$: $\frac{n-1}{n} \to 1$ — the bias disappears.

> **For the sample sizes you work with (252 days), the difference between dividing by $n$ and $n-1$ for variance is tiny. The correction matters much more for small samples or when computing skewness/kurtosis, where the bias is larger.**

---

## 4. Why Skewness and Kurtosis Have Different Corrections

The bias correction for higher moments is more involved because you're dealing with powers of deviations estimated from the same data.

### The general problem

To estimate $E[(X - \mu)^k]$, you need $\mu$. You estimate $\mu$ with $\bar{x}$. The error in $\bar{x}$ gets raised to the $k$-th power inside the deviations, creating a bias that grows with $k$ and shrinks with $n$.

For variance ($k=2$): the bias is correctable by switching $n$ to $n-1$.

For skewness ($k=3$): the bias involves both the denominator and the ratio (numerator uses $\hat{\sigma}^3$, which itself has bias). The adjusted skewness is:

$$G_1 = \frac{\sqrt{n(n-1)}}{n-2} \cdot g_1$$

This correction is larger than just changing the denominator. For $n = 252$:

$$\frac{\sqrt{252 \times 251}}{252-2} = \frac{\sqrt{63,252}}{250} = \frac{251.5}{250} \approx 1.006$$

A 0.6% adjustment — small but real.

For kurtosis ($k=4$): the bias is even more complex, involving both the fourth moment estimation bias and the bias in $\hat{\sigma}^4$ in the denominator. The adjusted formula is:

$$G_2 = \frac{n-1}{(n-2)(n-3)}\left[(n+1)g_2 + 6\right]$$

For $n=252$:

$$G_2 = \frac{251}{250 \times 249}\left[253 \cdot g_2 + 6\right] \approx 0.00403 \times (253 \cdot g_2 + 6)$$

This is a non-trivial adjustment. When $g_2 = 5$ (excess kurtosis = 5, typical for equity returns), $G_2 \approx 0.00403 \times (253 \times 5 + 6) = 5.13$. That's a 2.6% adjustment.

### The practical take

| Moment | Bias at $n=252$ | Worth correcting? |
|--------|----------------|-------------------|
| Mean ($\bar{x}$) | None (unbiased with denominator $n$) | N/A |
| Variance ($s^2$) | 0.4% downward if using $n$ | Yes — trivial to fix, standard practice |
| Skewness ($g_1$) | ~0.6% downward if uncorrected | Maybe — small but SciPy does it by default |
| Kurtosis ($g_2$) | ~2.6% downward if uncorrected | Maybe — meaningful, depends on application |

For risk work with $n \geq 252$, the uncorrected versions are generally fine. The sampling variability of higher moments swamps the bias correction. But you should know which version your software gives you.

---

## 5. Standard Errors — How Precise Are Your Sample Moments?

A point estimate without a standard error is just a number. Here's how precise each moment estimate is (assuming normal data — if the data is non-normal, these are approximate):

### Standard error of the mean

$$\text{SE}(\bar{x}) = \frac{s}{\sqrt{n}}$$

For SPY: $s \approx 1.2\%$, $n = 252$:

$$\text{SE}(\bar{x}) = \frac{1.2\%}{\sqrt{252}} = \frac{1.2\%}{15.87} \approx 0.076\%$$

So $\bar{x} = 0.04\% \pm 0.076\%$ (roughly one SE). The mean estimate is imprecise — a 95% confidence interval spans about $\pm 0.15\%$, which is large relative to the daily mean itself (~0.04%). **The daily mean is estimated with terrible signal-to-noise.** This is why VaR is dominated by volatility, not drift.

### Standard error of the variance

$$\text{SE}(s^2) \approx \sigma^2 \sqrt{\frac{2}{n}}$$

For SPY: $\sigma^2 \approx 1.44$, $n = 252$:

$$\text{SE}(s^2) \approx 1.44 \times \sqrt{\frac{2}{252}} = 1.44 \times 0.089 \approx 0.128$$

95% CI for $\sigma^2$: $1.44 \pm 0.25$. Reasonably precise.

### Standard error of the standard deviation

$$\text{SE}(s) \approx \frac{\sigma}{\sqrt{2n}}$$

$$\text{SE}(s) \approx \frac{1.2\%}{\sqrt{504}} = \frac{1.2\%}{22.4} \approx 0.054\%$$

95% CI for $\sigma$: $1.2\% \pm 0.11\%$. Also reasonably precise.

### Standard error of skewness (normal data)

$$\text{SE}(g_1) \approx \sqrt{\frac{6}{n}}$$

For $n = 252$: $\sqrt{6/252} = \sqrt{0.0238} \approx 0.154$.

So $g_1 = -0.6 \pm 0.15$ (one SE). The standard error is about 25% of the estimate. **Skewness estimates are noisy.**

### Standard error of excess kurtosis (normal data)

$$\text{SE}(g_2) \approx \sqrt{\frac{24}{n}}$$

For $n = 252$: $\sqrt{24/252} = \sqrt{0.0952} \approx 0.309$.

So $g_2 = 5 \pm 0.31$ (one SE). But wait — the true kurtosis is far from normal, so the normal-based SE formula is unreliable. The actual SE for a fat-tailed distribution is larger. **Kurtosis estimates are very noisy, and the standard error formulas assume normality — which is exactly the assumption you're testing.**

### Summary table

| Moment | Typical SPY value | Approx SE | SE as % of estimate | Trust level |
|--------|-------------------|-----------|---------------------|-------------|
| Mean | 0.04% | 0.076% | 190% | Low — daily mean is mostly noise |
| Std Dev | 1.20% | 0.054% | 4.5% | High — reasonably precise |
| Skewness | −0.6 | 0.15 | 25% | Moderate — directional signal |
| Excess Kurtosis | 5 | 0.31+ | 6%+ | Moderate but formula unreliable |

> **The fundamental pattern: each higher moment is less precisely estimated. The mean is noisy because financial returns have tiny signal-to-noise. The variance is reasonable. Skewness is noisy. Kurtosis is very noisy. Use higher moments as directional indicators, not point estimates.**

---

## 6. Robustness — How Fragile Are Higher Moments?

Beyond precision (standard error), there's **robustness**: how much does a single observation affect the estimate?

### Sensitivity to a single outlier

Add one extreme observation to 252 typical SPY returns. How much does each moment shift?

| Moment | Formula power | Effect of one −8% day in 252 | Robust? |
|--------|--------------|------------------------------|---------|
| Mean | $x^1$ | Pulls mean down by ~0.03% | Generally robust |
| Variance | $(x - \bar{x})^2$ | Noticeable but bounded | Moderately robust |
| Skewness | $(x - \bar{x})^3$ | Substantial — cubic amplifies the extreme | Not robust |
| Kurtosis | $(x - \bar{x})^4$ | Dominating — one day can double kurtosis | Extremely fragile |

### Worked example — one bad day

Suppose SPY's 252-day returns have excess kurtosis of 4 (typical). On day 253, SPY drops −7% (a ~6σ event, given daily σ ≈ 1.2%).

Contribution to the fourth power sum: $(-0.07 - \bar{x})^4 \approx (0.07)^4 = 0.00002401$

The existing sum of fourth powers (from 252 observations): based on excess kurtosis = 4, so raw kurtosis ≈ 7, meaning $\frac{1}{n}\sum(x_i - \bar{x})^4 \approx 7\sigma^4 = 7 \times (0.012)^4 = 7 \times 2.07 \times 10^{-8} \approx 1.45 \times 10^{-7}$.

So $\sum_{i=1}^{252} (x_i - \bar{x})^4 \approx 252 \times 1.45 \times 10^{-7} \approx 3.65 \times 10^{-5}$.

The one −7% day adds $2.4 \times 10^{-5}$ to this sum — increasing it by 66%.

**One day out of 253 increases the sample kurtosis by about two-thirds.** That's how fragile the fourth moment is.

> **This is why you should never treat a single kurtosis number as gospel. One flash crash can dominate the estimate for the entire 252-day window. Kurtosis is best used as a monitoring signal — "has kurtosis been rising?" — not as a precise measurement.**

---

## 7. Which Software Gives You Which Version

This is a practical minefield. Different libraries default to different corrections.

| Library | Function | Default denominator | Excess or raw? | Notes |
|---------|----------|---------------------|-----------------|-------|
| NumPy | `np.mean(x)` | $n$ | N/A | Unbiased for the mean |
| NumPy | `np.var(x)` | $n$ | N/A | **Biased!** Use `ddof=1` for sample variance |
| NumPy | `np.std(x)` | $n$ | N/A | **Biased!** Use `ddof=1` for sample std |
| Pandas | `df.var()` | $n-1$ | N/A | Unbiased by default |
| Pandas | `df.std()` | $n-1$ | N/A | Unbiased by default |
| Pandas | `df.skew()` | $n-1$ adjusted | N/A | Uses adjusted Fisher-Pearson $G_1$ |
| Pandas | `df.kurtosis()` | $n-1$ adjusted | Excess | Returns excess (subtracted 3) |
| SciPy | `stats.skew(x)` | $n-1$ adjusted | N/A | `bias=False` by default (adjusted) |
| SciPy | `stats.kurtosis(x)` | $n-1$ adjusted | Excess | `bias=False`, `fisher=True` by default |

### The safe approach

```python
import numpy as np
import pandas as pd
from scipy import stats

returns = np.array([...])

# Mean — all agree
mean = returns.mean()

# Variance — use ddof=1
var = returns.var(ddof=1)  # NumPy, sample variance

# Std — use ddof=1
std = returns.std(ddof=1)

# Skewness — use scipy, decide on bias
skew = stats.skew(returns, bias=False)  # adjusted (default)
# or
skew_uncorrected = stats.skew(returns, bias=True)  # uncorrected (n in denominator)

# Kurtosis — use scipy, check fisher
excess_kurt = stats.kurtosis(returns, bias=False, fisher=True)  # excess, adjusted (default)
raw_kurt = stats.kurtosis(returns, bias=False, fisher=False)    # raw, adjusted
```

### When the differences matter

With $n = 252$, the differences are small. But with $n = 20$ (a short lookback window):

- `np.var(returns)` (biased): divides by 20
- `np.var(returns, ddof=1)` (unbiased): divides by 19
- Difference: 5%

If you're doing a 20-day rolling VaR and computing volatility, using the wrong denominator gives you a 2.5% error in $\sigma$ (square root of 5%). Not catastrophic, but it's a systematic bias you can eliminate with one keyword argument.

---

## 8. Sample Moments and VaR — the Connection

### Parametric VaR uses the first two sample moments

$$\widehat{\text{VaR}}_{95\%} = \bar{x} - 1.645 \cdot s$$

This is: sample mean (1st moment) minus a constant times sample standard deviation (√ of 2nd moment). The higher sample moments (skewness, kurtosis) are *not used* — they're implicitly assumed to be 0 and 3 (normal).

### The gap between historical and parametric VaR IS the higher moments

$$\text{Gap} = \text{VaR}_{\text{historical}} - \text{VaR}_{\text{parametric}}$$

When sample skewness is negative and sample kurtosis is high, the gap is large (historical VaR is more negative). When skewness ≈ 0 and kurtosis ≈ 3, the gap is small.

**This means you can monitor sample skewness and kurtosis as leading indicators for when parametric VaR will become unreliable.**

### Cornish-Fisher expansion — using sample moments to adjust parametric VaR

The Cornish-Fisher expansion adjusts the normal quantile $z_\alpha$ using sample skewness and kurtosis:

$$z_{\alpha}^{\text{CF}} = z_\alpha + \frac{g_1}{6}(z_\alpha^2 - 1) + \frac{g_2}{24}(z_\alpha^3 - 3z_\alpha) - \frac{g_1^2}{36}(2z_\alpha^3 - 5z_\alpha)$$

Then:

$$\text{VaR}_{\alpha}^{\text{CF}} = \bar{x} - z_{\alpha}^{\text{CF}} \cdot s$$

This adjusts parametric VaR using all four sample moments. For $z_{0.05} = -1.645$, $g_1 = -0.6$, $g_2 = 5$:

$$z_{0.05}^{\text{CF}} = -1.645 + \frac{-0.6}{6}(1.645^2 - 1) + \frac{5}{24}(-1.645^3 + 3 \times 1.645) - \frac{0.36}{36}(-2 \times 1.645^3 + 5 \times 1.645)$$

The negative skewness makes $z_\alpha$ more negative (pushes VaR further left), and the positive kurtosis also pushes it further left. The Cornish-Fisher VaR will be more conservative than parametric — and should be closer to historical VaR.

> **This is the bridge: sample moments aren't just descriptive statistics. They're the inputs that let you adjust parametric models to respect the actual shape of your data.**

---

## 9. How Many Observations Do You Need?

A practical question: given the standard errors, how much data do you need for reliable moment estimates?

| Moment | Rule of thumb | With 252 days | With 1,260 days (5 years) |
|--------|--------------|---------------|---------------------------|
| Mean | $n > 30$ for CLT, but signal/noise is the real problem | SE ≈ 0.076% (daily mean ~0.04%) | SE ≈ 0.034% (still noisy) |
| Variance | $n > 30$ gives reasonable precision | SE ≈ 12.8% of estimate | SE ≈ 5.7% of estimate |
| Skewness | $n > 100$ for rough estimate, $n > 500$ for precision | SE ≈ 0.15 — directional only | SE ≈ 0.07 — moderately precise |
| Kurtosis | $n > 500$ for rough estimate, $n > 2,000$ for precision | SE ≈ 0.31+ — very noisy | SE ≈ 0.14 — still noisy |

> **The bottom line: with 252 days, you can estimate the mean and variance reasonably well (though the mean's signal-to-noise is inherently terrible). Skewness and kurtosis are directional signals — "is it becoming more negative?" or "are tails fattening?" — not precise measurements. If you need precise higher moments, you need much more data, but more data brings non-stationarity problems (old data may not represent the current regime).**

---

## 10. Check-in Questions

1. **You compute `np.var(returns)` and get $s^2 = 1.40$. You compute `np.var(returns, ddof=1)` and get $s^2 = 1.406$. With $n=252$, the difference is 0.4%. Is this worth worrying about? In what situation would it matter more?**

2. **Your SPY returns have sample skewness = −0.6 with SE ≈ 0.15. Can you reject the hypothesis that the true skewness is zero (symmetric)?** (Rough rule: if estimate / SE > 2, it's statistically significant at ~5% level. Here: 0.6 / 0.15 = 4. Significant. The negative skewness is real, not sampling noise.)

3. **One day SPY drops −8%. The next day, your 252-day rolling kurtosis doubles. A colleague says: "This proves the distribution has extremely fat tails." Is this a fair inference from one day?**

4. **Why does the sample mean use $n$ in the denominator, but the sample variance uses $n-1$?** (The mean doesn't need a correction because we're not estimating anything else to compute it. The variance needs a correction because we use $\bar{x}$ — an estimate — when computing deviations. That estimation step consumes one degree of freedom.)

5. **You have 60 days of returns and want to estimate skewness. $n=60$, SE ≈ $\sqrt{6/60} = 0.316$. Your estimate is −0.4. How much trust would you place in this number?** (The SE is almost as large as the estimate. The 95% CI is roughly −0.4 ± 0.63, which comfortably includes zero. With 60 days, you can't distinguish negative skew from symmetric noise. Don't report a number — report a range or a directional indication.)

---

## What's Next

- **The normal distribution deep dive** — why it's the null hypothesis, how its moments (μ, σ², 0, 3) define it uniquely, and why finance rejects it
- **Estimators and their properties** — a systematic treatment of bias, variance, consistency, and efficiency. Bessel's correction as a special case of bias correction
- **The bias-variance trade-off in window length** — why 60-day and 252-day windows give different moment estimates, and which one is "better" (it depends on what you're optimising for)
- **A practical exercise** — compute all four sample moments from SPY data, bootstrap their standard errors, and assess which are reliable and which are just directional
