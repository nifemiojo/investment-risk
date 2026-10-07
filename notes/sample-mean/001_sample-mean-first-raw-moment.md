# The Sample Mean: First Raw Moment as an Empirical Estimate

**Session:** sample-mean  
**Topic:** The sample mean $\bar{x}$ — definition, estimation, properties  
**Prerequisites:** location/001 (location overview), moments/004 (raw vs central moments), moments/005 (location-scale-shape)

---

## 1. What Is the Sample Mean?

### 1.1 The Formula

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i = \frac{x_1 + x_2 + \cdots + x_n}{n}$$

You have $n$ observations. Add them up. Divide by $n$. That is the sample mean.

### 1.2 A Concrete Example

Five daily SPY returns: $−2.1\%, −0.8\%, +0.3\%, +1.2\%, −0.5\%$

$$\bar{x} = \frac{-2.1 + (-0.8) + 0.3 + 1.2 + (-0.5)}{5} = \frac{-1.9}{5} = -0.38\%$$

Five numbers collapse to one. That compression — from many to one — is what makes it a *summary statistic.* The cost is information loss. The gain is interpretability.

### 1.3 Notation

| Symbol | Meaning | Notes |
|--------|---------|-------|
| $\bar{x}$ | Sample mean | Computed from observed data. Pronounced "x-bar" |
| $\hat{\mu}$ | Estimated population mean | Same number as $\bar{x}$, different framing — it's a guess about $\mu$ |
| $\mu$ | True population mean | Unknown, unobservable parameter of the return-generating process |
| $\mu'_1$ | First raw moment (population) | $E[X]$. When computed from a sample: $\frac{1}{n}\sum x_i$ |

In most of the VaR notebooks, we write $\mu$ as shorthand for $\bar{x}$ — technically imprecise but common. When we're being careful about estimation, we distinguish them.

---

## 2. The Sample Mean as the First Raw Moment

### 2.1 Raw Means "No Centring"

A raw moment of order $k$:

$$\mu'_k = \frac{1}{n}\sum_{i=1}^{n} x_i^k$$

For $k=1$:

$$\mu'_1 = \frac{1}{n}\sum_{i=1}^{n} x_i^1 = \frac{1}{n}\sum_{i=1}^{n} x_i = \bar{x}$$

The sample mean **is** the first raw moment. It's the simplest possible moment — just raise to the first power (do nothing) and average.

### 2.2 Why "First"?

Because $k=1$ — the exponent is 1. Higher moments use $k=2,3,4,\ldots$:

| $k$ | Raw moment $\mu'_k$ | Name |
|-----|---------------------|------|
| 1 | $\frac{1}{n}\sum x_i$ | Mean |
| 2 | $\frac{1}{n}\sum x_i^2$ | Second raw moment (not variance) |
| 3 | $\frac{1}{n}\sum x_i^3$ | Third raw moment |
| 4 | $\frac{1}{n}\sum x_i^4$ | Fourth raw moment |

### 2.3 The Mean Anchors Every Higher Moment

Every central moment is computed relative to $\bar{x}$:

$$\mu_2 = \frac{1}{n}\sum (x_i - \bar{x})^2 \quad \text{— the deviations are from } \bar{x}$$
$$\mu_3 = \frac{1}{n}\sum (x_i - \bar{x})^3 \quad \text{— cubed deviations from } \bar{x}$$
$$\mu_4 = \frac{1}{n}\sum (x_i - \bar{x})^4 \quad \text{— fourth-power deviations from } \bar{x}$$

If $\bar{x}$ is estimated poorly, every central moment is off. The error propagates. This is the *load-bearing* property of the mean — it's the foundation the entire moment structure rests on.

---

## 3. Why Estimate? The Population vs Sample Problem

### 3.1 The Setup

The true return-generating process has some fixed, unknown mean $\mu$. We never see it. Instead, we observe $n$ returns — a *sample* — and compute $\bar{x}$.

$$\bar{x} = \mu + \underbrace{\varepsilon}_{\text{sampling error}}$$

Every sample gives a different $\bar{x}$, even if $\mu$ hasn't changed. The variation in $\bar{x}$ is *sampling variability* — it's noise from which specific days happened to land in our window.

### 3.2 Three Questions Estimation Must Answer

| Question | What it's asking |
|----------|-----------------|
| **Bias:** On average, does $\bar{x}$ equal $\mu$? | If we could draw infinitely many samples, would the average of all the $\bar{x}$'s be $\mu$? |
| **Variance:** How much does $\bar{x}$ bounce around? | How wide is the sampling distribution? If we drew a new 252-day window, how different could the answer be? |
| **Consistency:** Does it get better with more data? | As $n \to \infty$, does $\bar{x} \to \mu$? |

The sample mean answers all three cleanly — which is *why* it's the workhorse of statistics.

---

## 4. Properties of the Sample Mean

### 4.1 Unbiasedness: $E[\bar{x}] = \mu$

The expected value of $\bar{x}$, over all possible samples, is the true population mean.

**Proof:**

$$E[\bar{x}] = E\left[\frac{1}{n}\sum_{i=1}^{n} x_i\right] = \frac{1}{n}\sum_{i=1}^{n} E[x_i] = \frac{1}{n}\sum_{i=1}^{n} \mu = \frac{1}{n} \cdot n\mu = \mu$$

Linearity of expectation does the work. We assume $E[x_i] = \mu$ for every observation (each day's return is drawn from the same distribution). Under that assumption, the sample mean is unbiased.

**What this means in practice:** If you could re-run history 10,000 times, each time observing a different 252-day window from the same process, and computed $\bar{x}$ each time — the average of those 10,000 $\bar{x}$'s would be $\mu$. Any single $\bar{x}$ is still off, but it's not systematically off in one direction.

**The equal-mean assumption is fragile.** In finance, the mean may drift over time (secular bull/bear markets, regime changes). If it does, $E[x_i] \neq \mu$ for all $i$ — the observations at the start and end of your window come from different processes. Unbiasedness holds only if the process is stationary.

### 4.2 Variance: $\text{Var}(\bar{x}) = \frac{\sigma^2}{n}$

The variance of $\bar{x}$ — how much it bounces from sample to sample — shrinks as $n$ grows.

**Proof (assuming independence):**

$$\text{Var}(\bar{x}) = \text{Var}\left(\frac{1}{n}\sum x_i\right) = \frac{1}{n^2}\text{Var}\left(\sum x_i\right) = \frac{1}{n^2}\sum\text{Var}(x_i) = \frac{1}{n^2} \cdot n\sigma^2 = \frac{\sigma^2}{n}$$

Variance scales with $1/n$, so standard error scales with $1/\sqrt{n}$.

| $n$ | SE (if $\sigma = 1.2\%$ daily) | Interpretation |
|-----|-------------------------------|----------------|
| 21 (1 month) | 0.262% | Very noisy — monthly mean is barely informative |
| 63 (1 quarter) | 0.151% | Still wide — a 95% CI spans ±0.30% |
| 252 (1 year) | 0.076% | Tighter — ±0.15% daily, or ±3.8% annualised |
| 1260 (5 years) | 0.034% | Tight — but is the process really the same over 5 years? |

**The diminishing returns are brutal.** To halve your standard error, you need 4× the data. Going from 1 year to 4 years to cut error in half.

**The independence assumption is wrong for financial returns.** Volatility clustering means $\text{Cov}(x_i, x_j) \neq 0$ for nearby days. When observations are positively correlated, the true $\text{Var}(\bar{x})$ is larger than $\sigma^2/n$ — the effective sample size is smaller than $n$. The formula above is a lower bound; reality is worse.

### 4.3 Consistency: $\bar{x} \xrightarrow{p} \mu$ as $n \to \infty$

As the sample grows, $\bar{x}$ converges to $\mu$ in probability. The Weak Law of Large Numbers guarantees this — as long as the observations have finite mean and come from the same distribution.

For any $\varepsilon > 0$:

$$P(|\bar{x} - \mu| > \varepsilon) \to 0 \quad \text{as} \quad n \to \infty$$

**The practical limit:** "As $n \to \infty$" is a mathematical statement, not a practical one. In finance, you never get infinite data. Worse: the process itself changes over long horizons. The asymptotics are reassuring, but the finite-sample reality — 252 days of a potentially non-stationary process — is what you actually face.

### 4.4 Linearity

The mean is a linear operator:

$$E[aX + bY] = aE[X] + bE[Y]$$

For a portfolio of two assets with weights $w_1, w_2$:

$$\bar{x}_{\text{portfolio}} = w_1\bar{x}_1 + w_2\bar{x}_2$$

The portfolio mean is the weighted sum of the component means. This is why portfolio expected return is so easy to compute — linearity does the work. (Portfolio variance is not like this — $w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\sigma_{12}$ — because variance is quadratic.)

### 4.5 The Mean Minimises Squared Error

For any constant $c$, the sum of squared deviations is minimised when $c = \bar{x}$:

$$\bar{x} = \arg\min_c \sum_{i=1}^{n} (x_i - c)^2$$

**Proof:** Take the derivative of $\sum (x_i - c)^2$ with respect to $c$ and set to zero:

$$\frac{d}{dc}\sum (x_i - c)^2 = -2\sum (x_i - c) = 0$$
$$\sum (x_i - c) = 0$$
$$\sum x_i - nc = 0$$
$$c = \frac{1}{n}\sum x_i = \bar{x}$$

The second derivative is $2n > 0$, confirming it's a minimum.

**Why this matters:** The mean and variance are a *matched pair.* Variance measures squared deviations from the mean. The mean is the point that makes those squared deviations as small as possible. If you used the median instead, and then computed "variance" as average squared deviations from the median — that number would always be larger than the actual variance. The mean is the *least squares* location measure.

### 4.6 Sensitivity to Outliers

Take a portfolio of 252 daily returns. On a typical day, it moves ±1%. One day, there's a flash crash: −8%. Then:

$$\bar{x}_{\text{with crash}} = \bar{x}_{\text{without crash}} - \frac{8\% - \bar{x}_{\text{without crash}}}{252} \approx \bar{x}_{\text{without crash}} - 0.032\%$$

A single −8% day shifts the annualised mean by about −8 percentage points (252 × 0.032%).

**This is a feature, not a bug.** The mean uses *all* the data. The crash happened — it should affect your estimate. The alternative — an estimator that ignores extreme observations — is systematically blind to the worst-case scenarios that VaR is supposed to capture.

**The trade-off:** unbiasedness vs precision. The mean is unbiased (it reflects the true expected value including crashes) but has high variance (a single crash can swing the estimate). The median is biased for the mean (in a skewed distribution, the median ≠ the mean) but has lower variance (it's robust). Which is better depends on what you're trying to estimate — the expected value (use the mean) or the typical value (use the median).

---

## 5. The Sampling Distribution of $\bar{x}$

### 5.1 What Is a Sampling Distribution?

$\bar{x}$ is a random variable. Different samples → different $\bar{x}$. The *distribution of $\bar{x}$ across all possible samples* is the sampling distribution of the mean.

This is a meta-distribution — a distribution of a statistic, not of the original data.

### 5.2 The Central Limit Theorem

If the $x_i$ are i.i.d. with mean $\mu$ and finite variance $\sigma^2$, then as $n \to \infty$:

$$\bar{x} \sim N\left(\mu, \frac{\sigma^2}{n}\right)$$

The sampling distribution of the mean approaches a normal distribution — **regardless of the shape of the original data.**

This is the magic of the CLT. Your daily returns can be skewed, fat-tailed, anything — as long as they have finite variance and you have enough of them, the *average* is approximately normal.

### 5.3 How Many Is "Enough"?

For well-behaved data: $n \approx 30$ is often enough. For financial returns (skewed, fat-tailed): $n$ needs to be larger — 100, maybe 252. The heavier the tails, the slower the convergence.

At $n = 252$ (one trading year of daily returns), the CLT is working reasonably but not perfectly. The sampling distribution of $\bar{x}$ is approximately normal, but the approximation degrades in the tails — which is exactly where you need it for risk.

### 5.4 Confidence Interval for $\mu$

Using the CLT, a $(1 - \alpha)\%$ confidence interval for $\mu$:

$$\bar{x} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}$$

For $\alpha = 0.05$ (95% confidence), $z_{0.025} = 1.96$:

$$\bar{x} \pm 1.96 \cdot \frac{\sigma}{\sqrt{n}}$$

**Example:** $\bar{x}_{\text{daily}} = 0.04\%$, $\sigma = 1.2\%$, $n = 252$:

$$\text{CI} = 0.04\% \pm 1.96 \cdot \frac{1.2\%}{\sqrt{252}} = 0.04\% \pm 1.96 \cdot 0.076\% = 0.04\% \pm 0.149\%$$

$$95\%\ \text{CI} = (-0.109\%, +0.189\%) \ \text{daily}$$

Annualised: $(-2.7\%, +4.8\%)$.

**Crucial observation:** Is zero inside this interval? For daily: yes — $-0.109\% < 0 < +0.189\%$. The data is consistent with the true daily mean being zero.

With 252 daily observations and typical volatility, you often **cannot distinguish the mean from zero** at standard confidence levels. This is why many practitioners assume $\mu = 0$ for short-horizon VaR — the data doesn't give you enough precision to reject that hypothesis.

### 5.5 The $t$-Distribution Refinement

The confidence interval above uses $z$ (normal quantiles), which assumes we *know* $\sigma$. In practice, we estimate $\sigma$ from the same data, using $s$ (the sample standard deviation). This adds uncertainty. The correct distribution for $\frac{\bar{x} - \mu}{s/\sqrt{n}}$ is the $t$-distribution with $n-1$ degrees of freedom:

$$\bar{x} \pm t_{n-1,\ \alpha/2} \cdot \frac{s}{\sqrt{n}}$$

For $n = 252$, $t_{251, 0.025} = 1.969$ (barely different from 1.96 — the $t$ converges to normal quickly). For small $n$ (e.g. $n = 10$, $t_{9, 0.025} = 2.262$), the difference is material.

At 252 observations in VaR, it barely matters. But the *concept* matters — every parameter you estimate from the data adds uncertainty that inflates your interval.

---

## 6. The Mean as the Empirical Moment Estimator

### 6.1 Method of Moments

The *method of moments* is a simple estimation principle: set the sample moment equal to the population moment and solve for the parameter.

For the mean, this is trivial:

$$\frac{1}{n}\sum x_i = \mu \quad \Longrightarrow \quad \hat{\mu} = \bar{x}$$

The sample first raw moment IS the method-of-moments estimator for $\mu$.

### 6.2 It's Also the Maximum Likelihood Estimator (Under Normality)

If returns are normally distributed with unknown $\mu$ and known $\sigma^2$, the MLE for $\mu$ is exactly $\bar{x}$. The sample mean is the most efficient estimator under normality.

But financial returns are not normal. Under a fat-tailed distribution, the mean is no longer optimal — it puts too much weight on extreme observations. Robust estimators (median, trimmed mean, Huber's M-estimator) can be more efficient.

### 6.3 The Sample Mean as a Plug-in Estimator

In parametric VaR, we plug $\bar{x}$ into the formula where $\mu$ belongs:

$$\widehat{\text{VaR}}_{95\%} = -(\bar{x} - 1.645\sigma)$$

We don't have $\mu$, so we use $\bar{x}$. This is a *plug-in estimator* — estimate the parameter, then use the estimate as if it were the truth.

The problem: plug-in estimators ignore estimation uncertainty. The VaR formula treats $\bar{x}$ as if it were $\mu$, with no adjustment for the fact that $\bar{x}$ is noisy. This makes parametric VaR overconfident — it reports a single number without reflecting how uncertain the inputs are.

---

## 7. Practical Considerations for Finance

### 7.1 The Window Length Trade-off

| Window | Precision of $\bar{x}$ | Relevance to current regime |
|--------|----------------------|---------------------------|
| 1 month (21 days) | Terrible — SE ≈ 0.26% daily | Excellent |
| 1 quarter (63 days) | Poor — SE ≈ 0.15% daily | Good |
| 1 year (252 days) | Modest — SE ≈ 0.08% daily | Reasonable |
| 5 years (1260 days) | Decent — SE ≈ 0.03% daily | Questionable |
| 20 years (5040 days) | Good — SE ≈ 0.017% daily | Almost certainly a different world |

The standard 252-day window is a compromise: precise enough to be useful, short enough to (hopefully) capture the current regime.

### 7.2 When the Mean Is (Nearly) Zero

For short-horizon equity returns, the daily mean is tiny relative to daily volatility:

$$\frac{|\bar{x}|}{\sigma} \ll 1$$

For SPY, often $|\bar{x}| \approx 0.01$–$0.05\%$ daily vs $\sigma \approx 1.0$–$1.5\%$. The signal-to-noise ratio is terrible — the mean is buried in noise.

This is why:
- Some practitioners set $\mu = 0$ for 1-day VaR (the error from doing so is small)
- The mean matters more for VaR at longer horizons (it scales with $h$, volatility with $\sqrt{h}$)
- Statistical tests for whether $\mu \neq 0$ are often inconclusive at 1-year horizons

### 7.3 The Bias-Variance Trade-off in Estimation

You can improve precision by:
1. **Using more data** — reduces variance but adds bias if the process changed
2. **Using a shrinkage estimator** — pull $\bar{x}$ toward zero (or a prior belief), trading some bias for less variance
3. **Using EWMA** — weight recent observations more (reduces old-process bias, but increases variance by using effectively fewer observations)

The standard VaR setup (252-day equal-weighted window) sits at one specific point on this trade-off. It's defensible, not optimal — a choice, not a law.

### 7.4 Common Pitfalls

| Pitfall | What it looks like | Why it's wrong |
|---------|-------------------|----------------|
| **Treating $\bar{x}$ as $\mu$** | "The mean return is 0.04% daily" | It's an *estimate* of the mean, with error bars. The true $\mu$ could easily be zero or double that |
| **Ignoring the confidence interval** | Computing VaR with $\bar{x}$ and reporting it to 3 decimal places | $\bar{x}$ itself has an 0.15% daily CI — the precision is fake |
| **Assuming independence for SE** | Using $\sigma/\sqrt{n}$ as if returns are i.i.d. | Volatility clustering makes the effective $n$ smaller, so the true SE is larger |
| **Forgetting horizon scaling** | "The mean is negligible, let's ignore it" — then computing a 1-year VaR | At 1 year, $\mu_{1y} = 252\mu_{1d}$, and this is no longer negligible |

---

## 8. From Sample Mean to VaR

### 8.1 Parametric VaR

$$\text{VaR}_{95\%} = -(\underbrace{\bar{x}}_{\text{First raw moment}} - 1.645\underbrace{\sigma}_{\text{sqrt of second central moment}})$$

The mean's contribution to 1-day VaR is small but real. For $\bar{x} = 0.04\%$, $\sigma = 1.2\%$:

$$\text{VaR without mean: } 1.645 \times 1.2\% = 1.974\%$$
$$\text{VaR with mean: } -(0.04\% - 1.974\%) = 1.934\%$$

Difference: 0.04% daily, ~10% annualised. Meaningful for risk limits? Sometimes. Dominant term? No — volatility is.

### 8.2 Historical VaR

Historical VaR doesn't explicitly use the mean. It uses the empirical quantile directly — sort the returns, pick the 13th worst.

But the mean IS implicitly present: the distribution's location determines where that quantile falls. Shift all returns up by 0.1% and the historical VaR improves by approximately 0.1%.

### 8.3 Expected Shortfall

$$\text{ES}_{95\%} = -\text{mean of returns below the 5th percentile}$$

Here the mean reappears — but as the conditional mean of the tail, not the unconditional mean of the whole distribution. ES is "what's the average loss, *given* you're in the 5% worst cases?"

---

## 9. Summary

| Concept | Key Point |
|---------|-----------|
| **Sample mean = first raw moment** | $\bar{x} = \frac{1}{n}\sum x_i = \mu'_1$ — the simplest moment, the foundation for every higher moment |
| **It's an estimate** | $\bar{x} \neq \mu$. It's $\mu$ + sampling error. The error shrinks with $\sqrt{n}$ |
| **Unbiased** | $E[\bar{x}] = \mu$ — not systematically too high or low |
| **Variance: $\sigma^2/n$** | Precision improves slowly. 4× data to halve the error |
| **CLT** | $\bar{x}$ is approximately normal for large $n$, even if returns aren't |
| **Confidence interval** | $\bar{x} \pm t_{n-1,\alpha/2} \cdot s/\sqrt{n}$ — for 252 days, often includes zero |
| **Load-bearing** | Every central moment depends on $\bar{x}$. Errors propagate upward |
| **In VaR** | Appears directly in parametric. Negligible for 1-day, dominant at long horizons |
| **Signal-to-noise** | For daily equity returns, S/N is terrible — the mean is barely distinguishable from zero |

---

## 10. Check-in Questions

1. **Compute $\bar{x}$ for these five returns: $+1.5\%, -2.0\%, +0.5\%, -1.0\%, +3.0\%$. What is the second raw moment $\mu'_2$ for this sample? (Remember: raw, not central.)**

2. **Why is $\text{Var}(\bar{x}) = \sigma^2/n$ a lower bound in finance? What makes the real variance larger?**

3. **For $\bar{x} = 0.06\%$ daily, $\sigma = 1.5\%$, $n = 126$ (6 months): compute the standard error and the 95% CI. Is zero inside?**

4. **If $E[\bar{x}] = \mu$, why don't we just use $\bar{x}$ as if it were $\mu$? What is the cost of ignoring estimation uncertainty?**

5. **The CLT says $\bar{x}$ is approximately normal for large $n$. For $n=252$, is this approximation good in the tails of the sampling distribution? Why might it fail exactly where we care most?**

6. **Why does the sample mean appear inside every central moment formula ($\sum (x_i - \bar{x})^k$) even though central moments are supposed to be "location-free"? What would happen if you used the true $\mu$ instead of $\bar{x}$?**

7. **A risk manager uses a 252-day mean of 0.04% daily for a 1-day VaR, then scales it to 10.08% annualised for an annual VaR. What's wrong with this? What two sources of error compound?**
