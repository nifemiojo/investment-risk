# Empirical Distributions — the Distribution Your Data Actually Has

**Date:** 2026-07-26
**Topic:** What an empirical distribution is, how it's built from data, why it's the foundation of historical VaR, and what it can and can't tell you.

---

## Opening Question

> You have 252 SPY returns. Before you fit any model, before you assume normality, before you compute parametric VaR — what distribution do you actually have? The answer is the empirical distribution. It's not an assumption. It's not a model. It's the data itself, organised. Here's everything you need to know about it.

---

## 1. What Is an Empirical Distribution? — Start Concrete

Here are 10 fictional daily SPY returns:

```
−2.4%, −1.8%, −0.6%, −0.3%, −0.2%, +0.1%, +0.5%, +0.8%, +1.5%, +2.1%
```

The empirical distribution is the answer to: "If I pick one of these returns at random, what's the probability of each outcome?"

Since we have 10 returns and each appears once:

| Return | Count | Probability (empirical) |
|--------|-------|------------------------|
| −2.4% | 1 | 1/10 = 0.10 |
| −1.8% | 1 | 1/10 = 0.10 |
| −0.6% | 1 | 1/10 = 0.10 |
| −0.3% | 1 | 1/10 = 0.10 |
| −0.2% | 1 | 1/10 = 0.10 |
| +0.1% | 1 | 1/10 = 0.10 |
| +0.5% | 1 | 1/10 = 0.10 |
| +0.8% | 1 | 1/10 = 0.10 |
| +1.5% | 1 | 1/10 = 0.10 |
| +2.1% | 1 | 1/10 = 0.10 |

> That's it. The empirical distribution is: **each observed value gets probability mass 1/n.** Nothing more. Nothing less.

If I ask "what's the probability of observing a return ≤ −0.6%?", you count: −2.4%, −1.8%, −0.6%. Three out of ten. Answer: 0.30.

If I ask "what's the probability of observing a return between +0.5% and +1.5%?", you count: +0.5%, +0.8%, +1.5%. Three out of ten. Answer: 0.30.

No equation. No parameters. No assumptions. Just counting.

---

## 2. The Empirical CDF — the Distribution's Backbone

The **empirical cumulative distribution function** (ECDF) is the workhorse. For any value $x$, it tells you the proportion of observations ≤ $x$:

$$\hat{F}_n(x) = \frac{1}{n}\sum_{i=1}^n \mathbf{1}\{x_i \leq x\}$$

**Terms:**
- $\hat{F}_n(x)$ — the empirical CDF evaluated at $x$. The hat means "estimate" and the $n$ subscript reminds you it depends on sample size.
- $n$ — number of observations (here, 10)
- $x_i$ — the $i$-th observed return
- $\mathbf{1}\{x_i \leq x\}$ — an **indicator function**. Returns 1 if the condition is true, 0 if false. It's a counter.

Let's build it for our 10 returns, step by step. First, sort them:

```
−2.4%, −1.8%, −0.6%, −0.3%, −0.2%, +0.1%, +0.5%, +0.8%, +1.5%, +2.1%
```

Now: at each sorted value, the ECDF steps up by $1/10 = 0.10$:

| $x$ (threshold) | Count ≤ $x$ | $\hat{F}_{10}(x)$ |
|----------------|-------------|-------------------|
| −2.4% | 1 | 0.10 |
| −1.8% | 2 | 0.20 |
| −0.6% | 3 | 0.30 |
| −0.3% | 4 | 0.40 |
| −0.2% | 5 | 0.50 |
| +0.1% | 6 | 0.60 |
| +0.5% | 7 | 0.70 |
| +0.8% | 8 | 0.80 |
| +1.5% | 9 | 0.90 |
| +2.1% | 10 | 1.00 |

Between these values, the ECDF is flat — it's a step function. For example, at $x = -0.4\%$, there are still only 3 observations ≤ −0.4%, so $\hat{F}_{10}(-0.4\%) = 0.30$. The function only steps up when you cross an actual data point.

### Key properties of the ECDF

1. **It always starts at 0** (below the smallest observation, nothing is ≤ $x$)
2. **It always ends at 1** (above the largest observation, everything is ≤ $x$)
3. **It's a step function** — flat between data points, jumps at each observation
4. **Each jump is exactly 1/n** unless there are ties (duplicate values), in which case the jump is $k/n$ for $k$ tied observations
5. **It's non-decreasing** — as $x$ increases, the proportion ≤ $x$ can only stay the same or increase

---

## 3. The Empirical PMF vs Histogram — Understanding the Discreteness

The empirical distribution is fundamentally **discrete**. It has probability mass only at the observed values. There is zero probability assigned to values you haven't seen.

This creates a subtlety: when you plot a **histogram**, you're smoothing the empirical distribution. A histogram bins the data and shows density (or frequency) per bin. It's a visual choice, not the empirical distribution itself.

### The empirical PMF (probability mass function) — what it actually is

For our 10 returns:

$$P(X = x) = \begin{cases} 0.10 & \text{if } x \in \{-2.4\%, -1.8\%, \ldots, +2.1\%\} \\ 0 & \text{otherwise} \end{cases}$$

That's the raw empirical distribution — 10 atoms of probability, each with mass 0.10, at 10 specific values.

### The histogram — a smoothed visualisation

A histogram with 5 bins might give you:

| Bin | Count | Density |
|-----|-------|---------|
| [−2.5%, −1.5%] | 2 | 0.20 per % |
| [−1.5%, −0.5%] | 2 | 0.20 per % |
| [−0.5%, +0.5%] | 3 | 0.30 per % |
| [+0.5%, +1.5%] | 2 | 0.20 per % |
| [+1.5%, +2.5%] | 1 | 0.10 per % |

The histogram hides the exact values and shows approximate shape. This is useful for visualisation with large $n$ — you can't display 252 individual probability atoms — but it's already a layer of approximation on top of the empirical distribution.

> **When you see a histogram of returns, you're looking at a smoothed, binned approximation of the empirical distribution. The actual empirical distribution is the set of 252 return values, each with probability 1/252.**

---

## 4. Quantiles from the Empirical Distribution — This Is Historical VaR

A **quantile** is the inverse of the CDF. If $F(x) = p$, then $x$ is the $p$-th quantile. The ECDF gives you $F(x)$ for any $x$. To get a quantile, you invert: given $p$, find the smallest $x$ such that $\hat{F}_n(x) \geq p$.

### Computing the 5th percentile from 10 returns

We want the 5th percentile ($p = 0.05$). Look at the ECDF:

| Sorted return | $\hat{F}_{10}(x)$ |
|--------------|-------------------|
| −2.4% | 0.10 |
| −1.8% | 0.20 |
| ... | ... |

The smallest $x$ where $\hat{F}_{10}(x) \geq 0.05$ is $x = -2.4\%$ (where $\hat{F}_{10} = 0.10$). So the 5th percentile is −2.4%.

### Computing VaR at 95% confidence from 10 returns

VaR at 95% confidence is the 5th percentile of the return distribution. Same answer: −2.4%.

The interpretation: "Based on the last 10 days, I am 95% confident that tomorrow's loss will not exceed 2.4%." Or more precisely: "Only 10% of observed days had losses exceeding 2.4%, so I estimate a 10% probability of a worse day — which is higher than 5%, making this a conservative VaR estimate."

### The problem with small samples — quantile interpolation

With 10 observations, your quantile resolution is coarse — you can only read off quantiles at multiples of $1/10 = 0.10$. You have no data between them. With 252 observations, your resolution is $1/252 \approx 0.004$, which is much finer.

When $n \times p$ is not an integer — say you want the 5th percentile from 252 observations: $252 \times 0.05 = 12.6$. There's no 12.6th observation. Different software handles this differently:

- **`np.percentile(returns, 5, method='lower')`**: takes the 12th (floor), giving a more conservative VaR
- **`np.percentile(returns, 5, method='linear')`**: interpolates between the 12th and 13th, giving a smoother estimate
- **`np.percentile(returns, 5, method='higher')`**: takes the 13th (ceiling), giving a less conservative VaR

For your Phase 1 notebooks, `np.quantile(returns, 0.05)` uses linear interpolation by default. This means your historical VaR number is an interpolated value between two actual observations — it's not a return that actually occurred on any specific day.

---

## 5. The Empirical Distribution as an Estimator

The empirical CDF $\hat{F}_n$ is an **estimator** of the true CDF $F$. This is a critical idea: your data's ECDF is your best guess at the true distribution that generated the data.

### Why it's a good estimator

The **Glivenko-Cantelli theorem** says: as $n \to \infty$, the ECDF converges uniformly to the true CDF almost surely. In plain English: with enough data, the empirical distribution becomes arbitrarily close to the true distribution.

$$\sup_x |\hat{F}_n(x) - F(x)| \xrightarrow{\text{a.s.}} 0 \quad \text{as } n \to \infty$$

The supremum ($\sup$) means "the maximum vertical distance between the ECDF and the true CDF over all possible $x$." This maximum distance goes to zero as $n$ grows.

### Why it's imperfect — what you lose

| Property | True CDF ($F$) | Empirical CDF ($\hat{F}_n$) |
|----------|---------------|---------------------------|
| Domain | Usually continuous (all real $x$) | Discrete (only at observed values) |
| Tails | Extends to ±∞ | Bounded by min and max observation |
| Smoothness | Usually smooth | Step function |
| Probability between observations | Positive | Zero |

The biggest loss is in the **tails**. The empirical distribution has zero probability mass beyond the most extreme observation. If your worst day in 252 observations was −4.2%, the empirical distribution says the probability of a day worse than −4.2% is exactly zero. 

But the true distribution almost certainly assigns positive probability to worse days. You just haven't seen one yet.

> **This is the fundamental limitation of historical VaR: it can't see beyond the worst day in the sample.**

---

## 6. Sampling Variability — the ECDF Changes With Every New Sample

The ECDF is a function of your sample. A different sample gives a different ECDF. Here's a concrete demonstration:

### Sample A (calm month)
```
−1.0%, +0.3%, −0.5%, +0.8%, −0.2%, +0.1%, +0.6%, −0.3%, +0.4%, −0.1%
```
Mean = +0.01%, Std = 0.52%, Min = −1.0%

### Sample B (volatile month)
```
+2.1%, −3.5%, +0.8%, −2.0%, +1.5%, −1.2%, +3.0%, −2.8%, +0.5%, −1.8%
```
Mean = −0.34%, Std = 2.12%, Min = −3.5%

Same underlying process. Different 10-day window. Completely different empirical distributions. Different means, different standard deviations, different minimums, different shapes.

### What this means for VaR

Historical VaR from Sample A: the 5th percentile is −1.0% (the worst day).
Historical VaR from Sample B: the 5th percentile is −3.5% (the worst day).

Same method. Same confidence level. Same underlying process. The VaR estimate varies by a factor of 3.5× purely because of which 10 days happened to fall in the window.

This is **sampling variability** — the variance of the estimator itself. With $n = 252$, the variability is smaller but still present. This is why changing the window length is a trade-off: longer windows reduce sampling variability (more data → more stable estimate) but increase the risk of including stale data (if the process has changed).

---

## 7. Bootstrapping — the Empirical Distribution's Superpower

Because the empirical distribution assigns probability $1/n$ to each observation, you can **sample from it**. This is called bootstrapping:

1. Draw $n$ observations **with replacement** from the original $n$ observations
2. Compute the statistic of interest (mean, VaR, correlation, whatever)
3. Repeat thousands of times
4. The distribution of the statistic across bootstrap samples approximates the **sampling distribution** of that statistic

### Why this matters for VaR

You can't compute a confidence interval for historical VaR analytically — there's no formula. But you can bootstrap it:

```python
import numpy as np

returns = np.array([...])  # 252 daily returns
n_bootstrap = 10_000
var_estimates = np.empty(n_bootstrap)

for i in range(n_bootstrap):
    bootstrap_sample = np.random.choice(returns, size=len(returns), replace=True)
    var_estimates[i] = np.quantile(bootstrap_sample, 0.05)

# 90% confidence interval for the VaR estimate
ci_lower = np.quantile(var_estimates, 0.05)
ci_upper = np.quantile(var_estimates, 0.95)
```

This tells you: "Historical VaR is −2.1%, but given the sampling variability, the true VaR (for the unconditional distribution of this process) could plausibly be anywhere from −1.8% to −2.5%." That's honest. That's useful. That's what a risk manager should communicate.

---

## 8. The Empirical Distribution vs Assumed Distributions — the Practical Comparison

When you compute historical VaR, you're using the empirical distribution. When you compute parametric VaR, you're using an assumed distribution (normal). Here's what each gives you:

| | Empirical distribution | Assumed distribution (normal) |
|---|---|---|
| **What it is** | The data, tabulated | An equation fitted to the data |
| **Parameters** | None (nonparametric) | μ and σ (parametric) |
| **Shape** | Whatever the data looks like | Bell curve (forced) |
| **Tails** | Bounded by observed extremes | Extends to ±∞ |
| **Extrapolates?** | No — can't see beyond data | Yes — can compute any quantile |
| **Respects higher moments?** | Yes — skewness and kurtosis are baked in | No — forces γ₁=0, γ₂=3 |
| **Sensitive to outliers?** | Only to the rank of the worst observations | Yes — one extreme day inflates σ |
| **Confidence interval?** | Bootstrap | Formula-based (standard error of quantile) |

### When to use which

- **Use the empirical distribution** when: you have enough data (252 days is reasonable for 95% VaR), you're at a moderate confidence level (95%, not 99.9%), and you want to avoid distributional assumptions. This is historical VaR.

- **Use an assumed distribution** when: you have little data, you need a very extreme quantile (99.9% for regulatory capital), or you have a strong reason to believe a specific distribution is correct. This is parametric VaR. But for financial returns and 95% confidence, the empirical distribution is often the more honest choice.

---

## 9. Where the Empirical Distribution Shows Up in Your Phase 1 Work

| Code/Concept | What's happening with the empirical distribution |
|-------------|------------------------------------------------|
| `np.quantile(returns, 0.05)` | Reading the 5th percentile from the ECDF. The entire historical VaR method is: build ECDF, read quantile. |
| `returns.hist(bins=50)` | Plotting a smoothed visualisation of the empirical distribution |
| `ecdf(returns)` (if you've plotted one) | The step function itself — every quantile lives here |
| Comparing historical vs parametric VaR | Comparing a quantile from the ECDF to a quantile from an assumed distribution. The gap *is* the higher moments. |
| Window comparison (60d vs 252d) | Comparing two different empirical distributions built from different windows. The difference is sampling variability + potential non-stationarity. |
| Decay-weighted VaR | Uses a weighted ECDF — observations have different weights, so the step sizes are unequal. The more recent observations get larger steps. |
| The correlation ratio (ρ_fast / ρ_slow) | Two empirical correlation estimates from two different empirical distributions (short window vs long window) |
| Bootstrap confidence intervals (if used) | Sampling from the empirical distribution to estimate the sampling distribution of VaR |

---

## 10. Three Things the Empirical Distribution Cannot Do

### 1. It cannot extrapolate beyond the data

If the worst day in 252 was −4.2%, the empirical distribution says $P(\text{return} < -4.2\%) = 0$. This is obviously wrong — worse days are possible, you just haven't seen one. The empirical distribution has a hard boundary at the observed extremes.

This is why historical VaR at 99% (≈ 1st percentile) from 252 days is unreliable. You're estimating the 3rd-worst day from only 2–3 observations in the tail. The estimate is extremely noisy.

### 2. It cannot distinguish between signal and noise

Every bump and wiggle in the empirical distribution is taken as truth. If there's an outlier — a single −8% day during a flash crash — that observation gets the same probability mass (1/252) as any other day. It pulls the empirical quantiles leftward, perhaps permanently (until it rolls out of the window). But was that −8% day a structural feature of the process, or a one-off anomaly?

The empirical distribution doesn't care. It treats every observation as equally representative of the true process. If you have reason to believe some observations are anomalous, you need to handle that yourself (winsorisation, trimming, or judgment).

### 3. It cannot tell you about time dependence

The empirical distribution pools all 252 returns and treats them as independent draws. It ignores the order. A dataset where the worst day was in March 2020 and a dataset where the worst day was yesterday produce identical empirical distributions — but completely different risk assessments. The recent worst day is more informative because of volatility clustering and regime persistence. The empirical distribution, by construction, can't see this.

This is why decay weighting and volatility scaling exist — they're attempts to inject time-awareness into what is fundamentally a time-ignorant object.

---

## 11. Questions to Test Your Understanding

### Beginner

1. **You have 5 returns: +1%, −2%, +3%, −1%, +0.5%. What is the empirical probability of a return ≤ 0%?** Count them. Answer: −2%, −1% — that's 2 out of 5 = 0.40.

2. **If you add a new −5% return to a 252-day dataset, what happens to the ECDF? Where does it change?** At −5%, a new step appears. The jump at −5% is 1/253. Every existing step shrinks from 1/252 to 1/253. The shape shifts.

### Intermediate

3. **Why is historical VaR at 99% from 252 days less reliable than historical VaR at 95% from 252 days?** At 95% you're reading roughly the 13th-worst day — you have 12 observations in the tail to anchor the estimate. At 99% you're reading roughly the 3rd-worst day — only 2 observations below it. The estimate is based on far fewer data points, so sampling variability is much higher.

4. **You bootstrap VaR and get a 90% confidence interval of [−1.7%, −2.8%]. What does this tell a risk manager that a single point estimate (−2.1%) doesn't?** It communicates uncertainty. "The model says −2.1%, but given the data we have, the true VaR of the unconditional distribution could reasonably be as low as −1.7% or as high as −2.8%." A risk manager who only sees −2.1% might over-trust it. A risk manager who sees the interval knows the model isn't precise.

### Advanced

5. **The Glivenko-Cantelli theorem says the ECDF converges to the true CDF as n → ∞. But financial returns are non-stationary — the true CDF changes over time. What does this mean for the theorem's applicability?** The theorem assumes i.i.d. data from a fixed distribution. If the true distribution is shifting (non-stationarity), then as you collect more data, you're mixing observations from different distributions. The ECDF converges to a *mixture* of past distributions, not to the current true CDF. Adding more data doesn't help — it may actually make things worse by including stale observations from a different regime. This is the mathematical justification for windowing (using only recent data) and decay weighting (down-weighting older data).

---

## What's Next

The natural next deep dives, depending on which thread you want to pull:

- **Quantiles and percentiles** — a focused dive on the inverse CDF, interpolation methods, and why `np.quantile` gives the number it does
- **The PDF, CDF, PPF triad** — how these three functions relate, and why you mostly use the CDF and its inverse (PPF) for risk
- **The normal distribution** — the theoretical distribution that parametric VaR assumes, and why its properties make it both compelling and dangerous
- **Estimators and their properties** — bias, variance, consistency, Bessel's correction. Why some estimators are better than others, and what "better" means
- **A practical exercise** — build the ECDF for your SPY data, compute VaR at multiple confidence levels, bootstrap the confidence intervals, and compare to parametric VaR
