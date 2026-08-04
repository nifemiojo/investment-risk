# Moments: What They Are, Why They're Called That, and Why They Matter for Risk

**Date:** 2026-07-26
**Topic:** Foundational overview of statistical moments — expectation, variance, skewness, kurtosis — and their role in financial risk.

---

## Opening Question

> You compute VaR every day. You sort 252 returns, take the 5th percentile, and call it risk. But what does that number *actually capture*? What story does it tell about your return distribution — and what does it leave out?
>
> Moments are the answer. They are the **summary statistics that describe the shape of a distribution**. Everything you do in risk — parametric VaR, correlation monitoring, volatility scaling, decay weighting — assumes something about moments. Understanding them is understanding what your models assume and when those assumptions break.

---

## 1. What Is a Moment? — Start With a Concrete Example

Forget formulas for a minute. Let's look at data.

Here are the daily returns for SPY over a recent week:

| Day | SPY Return |
|-----|-----------|
| Mon | +0.8% |
| Tue | −0.3% |
| Wed | +1.2% |
| Thu | −0.1% |
| Fri | +0.5% |

If I asked you to describe these returns to someone, what would you say?

You'd probably start with: **"On average, SPY went up about 0.42% per day."** That's the first moment — the **mean**. It tells you where the centre of the distribution is.

Then you might add: **"But it wasn't steady. Some days were up, some were down, ranging from −0.3% to +1.2%."** That's the second moment — the **variance** (or its square root, **standard deviation**). It tells you how spread out the returns are.

Now imagine two different return series, both with the same mean and same standard deviation:

**Series A:**
```
−1.5%, −1.0%, −0.5%, 0.0%, +0.5%, +1.0%, +1.5%
```

**Series B:**
```
+0.1%, +0.2%, +0.2%, +0.3%, +0.4%, +0.4%, −3.5%
```

Same mean? Yes (both ≈ 0.0%). Same standard deviation? Yes (both ≈ 1.08%). But they feel *completely different*. Series A is symmetric — the extreme moves are balanced on both sides. Series B has one massive negative outlier — a crash day — and otherwise mostly small positive days.

That difference is captured by the **third moment** — **skewness**. Series A has skewness ≈ 0 (symmetric). Series B has negative skewness — the tail on the left is fatter than the tail on the right.

Now imagine a fourth dimension: how extreme are the extreme moves, on *both* sides? Do you get more ±3σ days than a normal distribution would predict? That's the **fourth moment** — **kurtosis**. Financial returns famously have "fat tails": many more extreme moves than a normal distribution would allow.

> **The big idea:** Moments are a compact description of a distribution's shape. Each moment captures a different aspect: location, spread, asymmetry, tail weight. Together they give you a surprisingly complete picture.

---

## 2. Why Are They Called "Moments"?

This is one of those names that makes no sense until someone explains it — and then it's actually beautiful.

The term comes from **physics**, specifically from the concept of a **moment of force** (torque). In physics, a moment is a quantity multiplied by its distance from a reference point:

$$\text{Moment} = \text{force} \times \text{distance from pivot}$$

If you have a plank balanced on a fulcrum, the first moment tells you whether it tips left or right — it's the **centre of mass**. This is exactly the mean of a distribution: the point where the probability mass balances.

The second moment in physics is the **moment of inertia** — how hard it is to spin an object. It depends on how far the mass is from the centre, squared. This is exactly the variance: how far the probability mass is from the mean, squared.

Here's the mapping:

| Physics | Statistics | What it captures |
|---------|-----------|-----------------|
| Centre of mass | Mean (1st moment) | Where is the balance point? |
| Moment of inertia | Variance (2nd moment) | How spread out is the mass? |
| Skewness of weight distribution | Skewness (3rd moment) | Is more mass on one side? |
| How extreme the outlying mass is | Kurtosis (4th moment) | How much mass is far from centre? |

The word "moment" stuck because early statisticians (Karl Pearson and others in the late 19th century) explicitly borrowed the analogy from mechanics. A distribution is like a physical object with probability mass instead of physical mass, and moments describe its mechanical properties.

> **The intuition that matters:** Just as you can describe a physical object's shape by its moments (centre of mass, spread, skew), you can describe a return distribution's shape by its statistical moments. The more moments you know, the more precisely you know the distribution.

---

## 3. The Four Moments — Derivation, Intuition, and What They Mean for Returns

### 3.1 The Raw Moment Definition

For a random variable $X$, the $k$-th **raw moment** (moment about zero) is:

$$\mu'_k = E[X^k]$$

For a sample of $n$ observations:

$$\hat{\mu}'_k = \frac{1}{n}\sum_{i=1}^{n} x_i^k$$

**Terms:**
- $X$ — the random variable (in our case, daily returns)
- $k$ — which moment (1st, 2nd, 3rd, 4th)
- $E[\cdot]$ — expectation operator (the theoretical average over all possible outcomes)
- $\hat{\mu}'_k$ — sample estimate of the $k$-th raw moment ($\hat{}$ means "estimate")
- $x_i$ — the $i$-th observed return
- $n$ — number of observations (e.g., 252 trading days)

The raw moments are simple: raise each observation to the $k$-th power, take the average. But they're not directly interpretable because they're measured from zero, not from the centre of the distribution. That's why we usually work with **central moments**.

### 3.2 Central Moments — Measured From the Mean

The $k$-th **central moment** is:

$$\mu_k = E[(X - \mu)^k]$$

Where $\mu = E[X]$ is the mean.

For a sample:

$$\hat{\mu}_k = \frac{1}{n}\sum_{i=1}^{n} (x_i - \bar{x})^k$$

**Terms:**
- $\mu_k$ — the $k$-th central moment (theoretical)
- $\mu$ — population mean (the first raw moment, $\mu'_1$)
- $\bar{x}$ — sample mean
- $(x_i - \bar{x})$ — deviation of observation $i$ from the mean

By centring (subtracting the mean), we measure the shape around the distribution's centre, not around zero. This is what makes central moments interpretable.

---

### 3.3 First Moment: Expectation (Mean) — $\mu = E[X]$

**What it is:** The average value. The centre of mass of the distribution.

**Sample formula (central moment version):**
$$\hat{\mu}_1 = \frac{1}{n}\sum_{i=1}^{n} (x_i - \bar{x}) = 0 \quad \text{(always — by definition of the mean)}$$

The first central moment is always zero, because deviations from the mean sum to zero. So we use the raw version: $\hat{\mu} = \frac{1}{n}\sum x_i$.

**For SPY daily returns (2018–2025):** ≈ +0.04% per day (about +10% annualised).

**What it tells a risk manager:**
- The mean is the *expected daily return*. If you hold SPY for one day, your best guess for tomorrow's return is the historical average.
- But here's the catch: in VaR, the mean barely matters for a 1-day horizon. The daily mean is so small relative to daily volatility (±1–2%) that VaR is dominated by volatility, not drift. $\text{VaR}_{95\%} \approx \mu - 1.645\sigma$ — and $|\mu| \ll \sigma$ on a daily scale.
- Where the mean *does* matter: multi-period VaR (10-day), performance attribution (was the VaR a good deal?), and expected shortfall.

---

### 3.4 Second Moment: Variance — $\sigma^2 = E[(X - \mu)^2]$

**What it is:** The average squared deviation from the mean. It measures spread — how far typical returns are from the average.

**Why square?** Three reasons:
1. **Deviations above and below the mean are treated the same.** If you just averaged $(x_i - \bar{x})$, the positives and negatives would cancel to exactly zero. Squaring makes everything positive.
2. **Larger deviations are penalised more.** A 3% deviation contributes 9 units; a 1% deviation contributes 1 unit. This makes variance sensitive to extreme moves.
3. **Mathematical tractability.** Variance is linear for independent variables: $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)$. Standard deviation doesn't have this property. This is why portfolio variance uses $w'\Sigma w$.

**Standard deviation:** $\sigma = \sqrt{\sigma^2}$. This puts the units back into the original scale (percentage returns, not squared-percentage). It's more interpretable — you can say "daily volatility is about 1.2%" rather than "daily variance is about 1.44 squared-percent."

**For SPY daily returns (2018–2025):** $\sigma \approx 1.2\%$ per day.

**What it tells a risk manager:**
- This is the **foundation of parametric VaR**: $\text{VaR}_{95\%} = \mu - 1.645\sigma$. If $\sigma$ is wrong, VaR is wrong.
- Variance (and therefore volatility) is **not constant** over time. This is the single most important fact in financial risk. It clusters — calm periods follow calm periods, turbulent periods follow turbulent periods. GARCH models this. Decay weighting (λ=0.94 in RiskMetrics) is a practical response: give recent observations more weight when estimating variance.
- The **bias-variance trade-off** in estimation: a 60-day window gives you a fast estimate (low bias to current regime) but noisy (high variance of the estimate itself). A 252-day window is smoother but slow to react. There is no free lunch.

---

### 3.5 Third Moment: Skewness — $\gamma_1 = E\left[\left(\frac{X - \mu}{\sigma}\right)^3\right]$

**What it is:** Standardised third central moment. It measures asymmetry — which tail is fatter?

**Why standardised?** Dividing by $\sigma^3$ makes skewness dimensionless (unit-free). This lets you compare skewness across assets with different volatilities.

**Why cubed?** Because cubing preserves the sign:
- Negative deviation cubed → negative (keeps the sign)
- Positive deviation cubed → positive (keeps the sign)
- If negative deviations are larger (in magnitude), the sum is negative → negative skew

**Interpretation:**
- $\gamma_1 = 0$: symmetric distribution (normal distribution)
- $\gamma_1 < 0$: **negative skew** — left tail is fatter. Large negative returns are more common than large positive returns. This is the typical pattern for equity returns.
- $\gamma_1 > 0$: **positive skew** — right tail is fatter. Large positive returns are more common. Some strategies (trend-following, options selling) have this property.

**For SPY daily returns (2018–2025):** typically around −0.5 to −0.7.

**What it tells a risk manager:**
- **Negative skewness means VaR at 95% is more negative than normality predicts.** If returns were normal, the 5th percentile would be at $\mu - 1.645\sigma$. With negative skew, it's further out. This is why historical VaR often exceeds parametric VaR — the data has fatter left tails than a normal distribution.
- If you're monitoring a portfolio and skewness becomes more negative, **your downside risk is increasing faster than your volatility suggests**. Volatility alone won't catch this.
- Trading strategies can change skewness. Selling puts adds negative skew (collect small premia, occasionally take a large loss). Buying puts adds positive skew. A risk manager needs to know which side the skew is on.

**The skewness asymmetry check for your portfolio:**

When skewness turns more negative, parametric VaR (which assumes symmetry) increasingly *understates* risk. The gap between historical and parametric VaR widens. This is one of the signals in your multi-window dashboard (Notebook 14).

---

### 3.6 Fourth Moment: Kurtosis — $\gamma_2 = E\left[\left(\frac{X - \mu}{\sigma}\right)^4\right] - 3$

**What it is:** Standardised fourth central moment, with 3 subtracted (the "excess kurtosis"). Measures tail weight — how much probability mass is in the extreme tails relative to a normal distribution.

**Why the fourth power?** The fourth power makes extreme deviations enormous:
- A 1σ move contributes $1^4 = 1$ to the sum
- A 3σ move contributes $3^4 = 81$ to the sum
- A 5σ move contributes $5^4 = 625$ to the sum

This makes kurtosis exquisitely sensitive to the most extreme observations. A single 5σ day dominates the calculation.

**Why subtract 3?** A normal distribution has kurtosis = 3. Subtracting 3 makes the normal distribution the baseline (excess kurtosis = 0). Anything positive means "fatter tails than normal."

**Interpretation:**
- Excess kurtosis = 0: tails match a normal distribution
- Excess kurtosis > 0: **leptokurtic** — fatter tails. More extreme events than normal. This is the hallmark of financial returns.
- Excess kurtosis < 0: **platykurtic** — thinner tails. Less extreme events than normal. Rare in finance.

**For SPY daily returns (2018–2025):** excess kurtosis typically 3–8 (so raw kurtosis 6–11).

**What it tells a risk manager:**
- **High kurtosis means VaR at 95% misses a lot.** VaR tells you about the *threshold* of the worst 5% of days. It says nothing about how bad those 5% of days actually are. A portfolio with the same 95% VaR but higher kurtosis has much worse *worst-case* outcomes.
- This is why expected shortfall (ES / CVaR) exists: it averages the outcomes in the tail, so it's sensitive to kurtosis in a way VaR is not.
- During crises, kurtosis spikes as extreme moves arrive. A risk system that only monitors volatility and VaR will miss the surge in tail risk until after the damage is done.

**The kurtosis trap:**

Two distributions can have the same mean, same variance, same skewness, and even the same 95% VaR — but different kurtosis. The one with higher kurtosis has a worse worst day. This is the limit of VaR as a risk metric: it's a quantile, not an integral over the tail.

---

## 4. The Big Picture: What Moments Tell You That a Single VaR Number Doesn't

A VaR number is a single point on the return distribution — the 5th percentile. Here's what happens when you only look at VaR:

| What you see | What you miss |
|-------------|--------------|
| VaR = −2.1% | Is this symmetric? (skewness) |
| | How bad are the worst days? (kurtosis) |
| | Has volatility been rising or falling? (variance trend) |
| | Is the mean positive or negative? (expectation) |

Moments give you the **full shape** of the distribution. VaR is one point on that shape. Here's why this matters in practice:

**Scenario 1 — Rising skewness but stable VaR:**
Your portfolio VaR is steady at −2.1%. But skewness has gone from −0.3 to −0.9 over the past month. What's happening? The left tail is fattening. The *threshold* hasn't moved yet, but the *shape* is changing. When the next shock hits, the VaR number will jump — but you could have seen it coming.

**Scenario 2 — Same VaR, different kurtosis:**
Two portfolios, both with VaR₉₅ = −2.0%. Portfolio A has excess kurtosis = 2. Portfolio B has excess kurtosis = 8. Portfolio A's worst day in 252 days is −3.5%. Portfolio B's worst day is −6.2%. Same VaR, completely different risk profile. A risk manager who only looks at VaR would call these equal.

**Scenario 3 — The moment cascade during a crisis:**

In a market crisis, moments don't change one at a time — they cascade:
1. **Variance spikes first** (volatility jumps)
2. **Skewness turns sharply negative** (crash risk concentrates on the downside)
3. **Kurtosis explodes** (extreme moves arrive)
4. **The mean may turn negative** (drift shifts)

A risk system that monitors all four moments catches the cascade early. A system that only monitors VaR sees the result after the cascade has played out.

---

## 5. Where Moments Appear in Your Phase 1 Work

Moments aren't abstract — they're embedded in every notebook you've written:

| Concept | Where it appears | What moment is doing |
|---------|-----------------|---------------------|
| `returns.std()` | Notebooks 03, 04, 08 | Second moment — scaling VaR, comparing volatility regimes |
| `np.quantile(returns, 0.05)` | Every VaR computation | Reads a point on the CDF — the CDF is the *integral* of the PDF, which is shaped by all four moments |
| Vol scaling (share price → returns) | Notebook 08 | Assumes the *distribution shape* (moments 3+) is stable when you divide by volatility. If it's not, vol scaling distorts the distribution. |
| Combined method (Notebook 09) | Notebook 09 | Blends equal-weight and decay-weight to fix lag — implicitly assumes recent returns are a better estimate of current variance (second moment) |
| Parametric VaR = μ − z·σ | Sessions 004–009 | Explicitly uses first and second moments. Assumes third and fourth are zero (normality). This is exactly why parametric ≠ historical. |
| Correlation ratio monitoring | Notebooks 13, 14, 15 | Correlation is standardised covariance — a second-moment relationship between two variables |
| Decay weighting (λ=0.94) | Notebooks 05, 06 | Gives more weight to recent observations when estimating variance — a response to the fact that second moments are non-stationary |

---

## 6. Questions You Should Be Asking

These are the questions that separate "I can calculate moments" from "I understand what moments mean for risk." Work through them in order:

### Beginner

1. **If I told you a portfolio's returns have μ = +0.05%, σ = 1.2%, γ₁ = −0.6, and γ₂ = 5, what story does this tell?** Can you describe this portfolio's return pattern to a trader in plain English?

2. **Why does subtracting 3 from kurtosis make sense?** What's special about the number 3, and why does it appear?

3. **If skewness = 0, does that mean the distribution is symmetric?** (Hint: no. Zero skewness is necessary for symmetry, not sufficient. Think about multimodal distributions.)

### Intermediate

4. **You estimate σ from 60 days vs 252 days. Which estimate is more volatile?** Not the estimate of volatility — the volatility *of the estimate*. This is the bias-variance trade-off.

5. **The sample variance formula divides by (n−1), not n. Why?** (This is Bessel's correction — it makes the sample variance an *unbiased estimator* of the population variance. If this concept isn't familiar, it's worth a deep dive.)

6. **During the COVID crash (March 2020), did SPY's skewness become more positive or more negative?** Think about what happened: a rapid crash followed by a rapid recovery. What does that do to the shape of the distribution sampled over a 252-day window?

### Advanced

7. **If returns are not independent (volatility clusters), are your moment estimates reliable?** Standard errors for moment estimates assume i.i.d. data. Financial returns violate this. What does that mean for how much you should trust a skewness or kurtosis estimate from 252 days of data?

8. **Kurtosis is extremely sensitive to outliers. If you have one −8% day in 252, how much does it shift the sample kurtosis?** This is the robustness problem. A single observation can dominate the fourth moment. Is kurtosis a useful statistic if one day can change it dramatically?

9. **Higher moments (skewness, kurtosis) require more data to estimate reliably than lower moments (mean, variance).** Why? (Think about the power: to estimate $E[X^k]$ well, you need observations of $X^k$ to converge. For $k=4$, extreme values are raised to the fourth power — and extreme values are, by definition, rare. You're trying to estimate the shape of the tail using the few observations actually in the tail.)

---

## 7. The Fundamental Trade-Off in Moment Estimation

There is a brutal truth about estimating moments from financial data, and it's worth stating explicitly:

| Moment | What it requires | The problem |
|--------|-----------------|-------------|
| Mean (1st) | Relatively easy to estimate. Converges quickly. | Financial means are very small relative to noise. The signal-to-noise ratio is terrible. |
| Variance (2nd) | Reasonably estimable with 60–252 days. | Non-stationary — the true variance changes over time. Your estimate is always chasing a moving target. |
| Skewness (3rd) | Needs more data. Cubic deviations amplify noise. | Non-stationary AND noisy. During calm periods, negative skew may appear small. During crises, it shifts violently. |
| Kurtosis (4th) | Very data-hungry. Dominated by the most extreme observations. | A single crash day can double your kurtosis estimate. The estimate bounces around wildly. |

> **The practical implication:** You can compute moments every day, but you should trust them differently. The mean and variance from a 252-day window are reasonably stable. Skewness and kurtosis are noisier — use them as directional signals (is skewness becoming more negative?) rather than precise point estimates (skewness is exactly −0.63).

---

## 8. Standardised Moments vs Raw Moments — Why Standardise?

You'll often see skewness and kurtosis written with $\sigma$ in the denominator:

$$\text{Skewness} = E\left[\left(\frac{X - \mu}{\sigma}\right)^3\right]$$

$$\text{Kurtosis} = E\left[\left(\frac{X - \mu}{\sigma}\right)^4\right]$$

Dividing by $\sigma^k$ standardises the moment — it makes it dimensionless and scale-free.

**Why this matters:** Imagine SPY returns with σ = 1.2% and a 3× leveraged SPY ETF with σ = 3.6%. The raw third central moment $E[(X-\mu)^3]$ is 27× larger for the leveraged ETF (because $\sigma^3$ is 27× larger). But the *shape* — the asymmetry — is identical. Standardised by $\sigma^3$, both have the same skewness. This is why standardisation matters for comparison.

**The same logic as correlation:** Just as correlation = covariance / (σ₁σ₂) strips out scale to leave pure co-movement, standardised moments strip out volatility to leave pure shape. The raw moment tells you about magnitude; the standardised moment tells you about shape.

---

## 9. Moments and VaR — The Parametric Connection

Parametric VaR uses only the first two moments:

$$\text{VaR}_{95\%} = \mu - 1.645\sigma$$

This formula assumes the third and fourth standardised moments are zero (i.e., the distribution is normal). When returns have negative skew and positive excess kurtosis, this formula *understates* VaR.

The gap between historical VaR and parametric VaR is, fundamentally, **a statement about higher moments**:

$$\text{Gap} = \text{VaR}_{\text{historical}} - \text{VaR}_{\text{parametric}}$$

A large gap means: "The actual return distribution has fatter left tails and more extreme outliers than normality assumes." The gap is a measure of how badly the parametric assumption is violated.

In your Phase 1 notebooks, when you see historical VaR consistently more negative than parametric VaR for SPY, that's negative skewness and excess kurtosis at work.

---

## 10. Check-In Questions

Before moving on to the next deep dive (likely the normal distribution or estimators), test yourself:

1. **Explain to yourself in plain English what each moment captures.** Don't use formulas. "The mean is where the centre of the returns sits. The variance is..."

2. **If a trader asks you "how risky is this portfolio?", what would you need beyond VaR to answer?** Which moments provide that information?

3. **Why can't you simply add the VaRs of two assets to get the portfolio VaR?** (This is the fundamental inequality question — it's about the second moment relationship between assets, which VaR as a quantile doesn't capture.)

4. **You have a new dataset of 100 daily returns. You compute the mean, variance, skewness, and kurtosis. Rank them by how much you trust each estimate.** Which would you be most confident in? Least?

---

## What's Next

This overview introduces the four moments. Each one deserves its own deep dive:

- **Variance deep dive:** population vs sample, unbiased estimators (Bessel's correction), why $n-1$, the bias-variance trade-off in window length
- **Skewness deep dive:** what creates negative skew in practice, how to detect it, how it interacts with VaR
- **Kurtosis deep dive:** the robustness problem, expected shortfall as a kurtosis-aware metric, why VaR ignores kurtosis
- **The normal distribution:** why it's the null hypothesis, how its moments (0, σ², 0, 3) define it, and why finance rejects it

The next file you should pick up is whichever of these connects most directly to a question you're currently asking yourself.
