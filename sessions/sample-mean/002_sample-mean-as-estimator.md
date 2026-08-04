# The Sample Mean as an Estimator

**Session:** sample-mean  
**Topic:** What it means to estimate — the sample mean through the lens of estimation theory  
**Prerequisites:** sample-mean/001 (sample mean as first raw moment), location/001 (location overview), moments/002 (empirical vs theoretical distributions)

---

## 1. What Does It Mean to "Estimate"?

### 1.1 The Fundamental Setup

There is a true state of the world. You can't see it. You observe data. You use the data to guess the truth.

$$
\underbrace{\bar{x}}_{\text{estimator applied}} = \underbrace{\mu}_{\text{truth}} + \underbrace{\varepsilon}_{\text{error you can't avoid}}
$$

That is estimation in one line. Every estimator, no matter how sophisticated, is truth plus error. The question is never "is my estimate right?" — it's "how wrong is it, in what way, and can I live with that?"

### 1.2 Three Things You Can Say About an Estimate

| Question | Formal name | What it asks |
|----------|-------------|-------------|
| Is it right on average? | **Bias** | If I could repeat this infinitely, would I get the truth on average? |
| How much does it bounce around? | **Variance** | If I drew a new sample tomorrow, how different could the answer be? |
| Is the total error acceptable? | **MSE / RMSE** | Bias² + variance — the total expected penalty for being wrong |

An estimator is a *decision rule* — given data, produce a number. Estimation theory gives us the tools to evaluate that decision rule before we apply it.

---

## 2. Estimators Are Random Variables

### 2.1 $\bar{x}$ Is a Function of the Sample

$$
\bar{x} = f(x_1, x_2, \ldots, x_n) = \frac{1}{n}\sum_{i=1}^{n} x_i
$$

The $x_i$ are random (before you observe them). Therefore $\bar{x}$ is random. Its value depends on which specific observations happen to land in your sample.

### 2.2 Two Distributions, Two Meanings

| Distribution | What it is | Example |
|-------------|-----------|---------|
| **Data distribution** | How individual returns are distributed | Daily SPY returns: mean ~0.04%, std ~1.2%, left-skewed, fat-tailed |
| **Sampling distribution of $\bar{x}$** | How $\bar{x}$ is distributed across possible samples | Approximately $N(\mu, \sigma^2/n)$ |

They are different objects. The data distribution is skewed and fat-tailed. The sampling distribution of $\bar{x}$ is approximately normal — the CLT compresses the shape toward normality.

### 2.3 A Simulation to Build Intuition

Imagine the true daily return distribution is $N(0.04\%, 1.2\%^2)$. You draw 252 days, compute $\bar{x}$. Repeat this 10,000 times.

What you'd see:
- The 10,000 $\bar{x}$'s cluster around 0.04%
- Most are within ±0.15% of 0.04%
- A few are as far as ±0.3% away
- The histogram of the 10,000 $\bar{x}$'s looks normal — much more normal than the original daily returns

This histogram IS the sampling distribution of $\bar{x}$. It shows you every possible $\bar{x}$ you could get from this process, and their relative frequencies.

Your *one actual* $\bar{x}$ is a single draw from this distribution. You don't know where in the distribution it falls. That's the fundamental uncertainty of estimation.

---

## 3. Desirable Properties of an Estimator

### 3.1 Unbiasedness: $E[\hat{\theta}] = \theta$

On average, the estimator hits the target.

For the sample mean: $E[\bar{x}] = \mu$. The proof is two lines (linearity of expectation). Under the assumption that each $x_i$ has mean $\mu$, the sample mean is unbiased.

**What unbiasedness does NOT mean:**
- It does NOT mean a specific $\bar{x}$ equals $\mu$ — it almost certainly doesn't
- It does NOT mean $\bar{x}$ is close to $\mu$ — it could be far off, just not systematically in one direction
- It does NOT mean unbiased estimators are always better — a biased estimator with much lower variance can have lower total error

**The dartboard analogy:**

```
Unbiased, high variance:        Biased, low variance:
    ·  ·                              ·
  ·   ·   ·                          ·· ·
    ·  ·                             ·····
   ·    ·                             ···
                                      ·
  Scattered around centre          Clustered off to the side
  Average = bullseye               Average ≠ bullseye
```

Which is better? Depends. If you're firing once and one miss kills you, you might prefer the biased one — all shots land in a tight group, just consistently off. If you're aggregating over many shots (diversifying), unbiasedness matters more.

### 3.2 Consistency: $\hat{\theta}_n \xrightarrow{p} \theta$ as $n \to \infty$

As the sample grows, the estimator converges to the truth.

For the sample mean, the Weak Law of Large Numbers guarantees consistency — provided the data has finite mean and comes from the same distribution.

$$P(|\bar{x}_n - \mu| > \varepsilon) \to 0 \quad \text{for any } \varepsilon > 0$$

**Intuition:** More data → less noise → closer to truth. At $n = \infty$, you'd know $\mu$ exactly. At $n = 252$, you're somewhere on the journey.

**The catch in finance:** "As $n \to \infty$" assumes the process stays the same. If the true $\mu$ drifts over decades, adding more old data doesn't help — you're converging to a historical average that's not the current $\mu$. Consistency is a mathematical property; practical relevance depends on stationarity.

### 3.3 Efficiency: Smallest Variance Among a Class

An estimator is efficient if no other unbiased estimator has lower variance.

For normally distributed data, $\bar{x}$ is the **minimum variance unbiased estimator (MVUE)** of $\mu$. No other unbiased estimator can beat it — it extracts the maximum possible information from the data.

For fat-tailed data, $\bar{x}$ is NOT efficient. The median, or a trimmed mean, or an M-estimator, can have lower variance — because they downweight the extreme observations that inflate the mean's variance.

| Data | Efficient estimator of location |
|------|-------------------------------|
| Normal | Mean ($\bar{x}$) |
| Laplace (double-exponential) | Median |
| Student's t (fat-tailed) | Trimmed mean or M-estimator |
| Cauchy (infinite variance) | Median (mean doesn't even converge) |

Financial returns are somewhere between normal and Student's t. $\bar{x}$ is still unbiased, still consistent — but no longer optimal. The extremes inflate its variance.

---

## 4. Measuring Estimation Error

### 4.1 Mean Squared Error (MSE)

MSE is the expected squared distance between the estimator and the truth:

$$\text{MSE}(\hat{\theta}) = E[(\hat{\theta} - \theta)^2]$$

It decomposes beautifully:

$$\text{MSE}(\hat{\theta}) = \underbrace{\text{Var}(\hat{\theta})}_{\text{how much it bounces}} + \underbrace{(\text{Bias}(\hat{\theta}))^2}_{\text{systematic offset squared}}$$

**Proof:**

$$
\begin{aligned}
\text{MSE}(\hat{\theta}) &= E[(\hat{\theta} - \theta)^2] \\
&= E[(\hat{\theta} - E[\hat{\theta}] + E[\hat{\theta}] - \theta)^2] \\
&= E[(\hat{\theta} - E[\hat{\theta}])^2] + (E[\hat{\theta}] - \theta)^2 + 2E[\hat{\theta} - E[\hat{\theta}]](E[\hat{\theta}] - \theta) \\
&= \text{Var}(\hat{\theta}) + \text{Bias}^2(\hat{\theta}) + 0
\end{aligned}
$$

The cross term vanishes because $E[\hat{\theta} - E[\hat{\theta}]] = 0$.

### 4.2 Bias-Variance Decomposition for $\bar{x}$

Since $\bar{x}$ is unbiased — $\text{Bias}(\bar{x}) = 0$ — its MSE is pure variance:

$$\text{MSE}(\bar{x}) = \text{Var}(\bar{x}) = \frac{\sigma^2}{n}$$

| $n$ | $\text{Var}(\bar{x})$ if $\sigma = 1.2\%$ | $\text{RMSE} = \sqrt{\text{MSE}}$ |
|-----|------------------------------------------|----------------------------------|
| 21 | $(0.262\%)^2 = 0.0686$ | 0.262% |
| 63 | $(0.151\%)^2 = 0.0229$ | 0.151% |
| 252 | $(0.076\%)^2 = 0.0057$ | 0.076% |
| 1260 | $(0.034\%)^2 = 0.0011$ | 0.034% |

RMSE is the "typical" error magnitude — it's in the same units as the data. With 252 days and $\sigma = 1.2\%$, your $\bar{x}$ is typically off by about 0.076% daily, or 1.9% annualised. That's the precision you're working with.

### 4.3 Standard Error vs RMSE

For an unbiased estimator, RMSE = standard error. They're the same thing — the standard deviation of the sampling distribution.

$$\text{SE}(\bar{x}) = \frac{\sigma}{\sqrt{n}}$$

But we estimate $\sigma$ from the data too, so we use:

$$\widehat{\text{SE}}(\bar{x}) = \frac{s}{\sqrt{n}}$$

The hat on SE means "estimated" — we're estimating the standard deviation of our estimator. Estimation all the way down.

---

## 5. The Sample Mean vs Other Estimators of Location

### 5.1 The Competitors

| Estimator | Formula | Robust to outliers? | Efficient for normal? | Efficient for fat-tailed? |
|-----------|---------|---------------------|----------------------|--------------------------|
| **Mean** | $\frac{1}{n}\sum x_i$ | No | Yes | No |
| **Median** | Middle value | Yes | No (~64% efficiency) | Yes |
| **Trimmed mean (5%)** | Mean after discarding top/bottom 5% | Moderately | Moderately | Moderately |
| **Winsorised mean (5%)** | Cap extremes at 5th/95th percentile, then mean | Moderately | Moderately | Moderately |

### 5.2 When Each Makes Sense in Finance

| Scenario | Best estimator | Why |
|----------|---------------|-----|
| Computing expected portfolio return for optimisation | Mean | You need mathematical expectation — all observations count |
| Describing "typical daily return" to a board | Median | "Half the days are better, half are worse" — communicates clearly |
| Estimating the location of a strategy with occasional blow-ups | Trimmed mean | You want to capture central tendency without letting one disaster dominate |
| Backtesting a VaR model | Mean (in parametric) | The formula requires it; consistency of methodology matters |

### 5.3 A Concrete Comparison

Five returns: $−2.0\%, −1.0\%, +0.5\%, +1.5\%, +12.0\%$ (the +12% is an outlier)

| Estimator | Value |
|-----------|-------|
| Mean | $+2.2\%$ |
| Median | $+0.5\%$ |
| Trimmed mean (20% — remove one each side) | $+0.33\%$ |

The +12% drags the mean up to 2.2% — four times the median. Which is right? Neither. They answer different questions.

- The mean says: "the expected value of one random day from this distribution is +2.2%" — correct, because the +12% day happens occasionally
- The median says: "the typical day is +0.5%" — also correct, because most days are ordinary
- The trimmed mean says: "stripping the extreme, the central tendency is +0.33%" — useful if you think the +12% is a one-off that won't repeat

---

## 6. Confidence Intervals: Quantifying Estimation Uncertainty

### 6.1 The Logic

You have one $\bar{x}$. It's a point estimate — a single number. But you know the sampling distribution, so you can construct an interval that captures $\mu$ with specified probability.

### 6.2 The Formula

$$\bar{x} \pm t_{n-1,\ \alpha/2} \cdot \frac{s}{\sqrt{n}}$$

This is NOT a probability statement about $\mu$ — $\mu$ is fixed, not random. It's a probability statement about the *interval*: "if I repeated this procedure on many samples, 95% of the resulting intervals would contain $\mu$."

### 6.3 Worked Example

$\bar{x} = 0.06\%$ daily, $s = 1.5\%$, $n = 252$

$$\text{SE} = \frac{1.5\%}{\sqrt{252}} = 0.0945\%$$

$$t_{251, 0.025} \approx 1.969$$

$$95\%\ \text{CI} = 0.06\% \pm 1.969 \times 0.0945\% = 0.06\% \pm 0.186\% = (-0.126\%, +0.246\%)$$

Interpretation:
- The data is consistent with $\mu$ being anywhere from −0.126% to +0.246% daily
- Zero is inside the interval — you cannot reject $\mu = 0$ at the 5% level
- The width of the interval (0.372% daily, ~9.4% annualised) is enormous — the mean is poorly estimated

### 6.4 The Width Grows When...

| Factor | Effect on CI width | Why |
|--------|-------------------|-----|
| Higher volatility ($\sigma$) | Wider | More noise in the data |
| Smaller sample ($n$) | Wider | Less information |
| Higher confidence level ($1-\alpha$) | Wider | You're demanding more certainty |
| Volatility clustering | Wider (but formula doesn't capture it) | Effective $n$ is smaller than actual $n$ |

The formula assumes i.i.d. data. Financial returns violate this — volatility clustering means consecutive returns aren't independent. The true confidence interval is wider than the formula suggests.

---

## 7. What Makes a "Good" Estimate in Finance?

### 7.1 The Trilemma

You want three things. You get to pick two.

| Want | What it means | How to get it |
|------|--------------|---------------|
| **Low bias** | Estimate is centred on the truth | Equal weights, long window, no shrinkage |
| **Low variance** | Estimate doesn't bounce around much | Shrinkage, short window (if regime matters), robust methods |
| **Relevance** | Estimate reflects current regime | Short window, decay weighting |

The standard VaR setup (252-day equal-weighted) chooses low bias + moderate relevance, at the cost of high variance. It's a defensible choice, but it's a *choice* — not a law of nature.

### 7.2 The Bias-Variance Trade-off Visualised

```
Bias²                          Variance
  │                              │
  │  Long window                 │  Long window
  │  252 days → low bias         │  252 days → high variance
  │                              │  (covers multiple mini-regimes)
  │                              │
  │  Short window                │  Short window
  │  63 days → higher bias       │  63 days → lower variance
  │  (may miss the full picture) │  (tighter, but possibly wrong regime)
  │                              │
  ▼                              ▼
```

There's no free lunch. Every methodological choice trades one source of error for another.

### 7.3 The Most Honest Answer

Q: "What's the mean daily return?"

The full answer:

> "Based on the last 252 trading days, the sample mean is 0.04% daily. The 95% confidence interval is (−0.11%, +0.19%), which means the data is consistent with the true mean being anywhere in that range — including zero. The standard error is 0.076%, so if I drew a different 252-day window, the answer could easily differ by ±0.15%. The mean is estimated poorly from 252 days, and I haven't even adjusted for the fact that volatility clustering makes the real uncertainty larger than the formula says."

The short answer people actually use:

> "About 4 basis points."

This tension — between what you know statistically and what you communicate practically — is central to being an effective quant in finance.

---

## 8. The Sample Mean in the Broader Estimation Hierarchy

Every quantity in VaR is estimated. The mean is just the first — and arguably the simplest.

| Quantity | Estimator | Estimation difficulty |
|----------|-----------|----------------------|
| $\mu$ | $\bar{x}$ | Moderate — imprecise but unbiased, CLT helps |
| $\sigma^2$ | $s^2 = \frac{1}{n-1}\sum(x_i - \bar{x})^2$ | Moderate — chi-squared sampling distribution, CLT helps less |
| Skewness | $\hat{\gamma}_1$ | Hard — converges slowly, very sensitive to outliers |
| Kurtosis | $\hat{\gamma}_2$ | Very hard — one extreme observation can dominate, needs thousands of points |
| VaR (historical) | $\hat{q}_{0.05}$ | Hard — only ~13 observations in the tail region, high variance |
| ES | $\widehat{\text{ES}}_{0.05}$ | Very hard — mean of ~13 observations, maximum instability |

The mean is the best-behaved estimator in finance. It's still not great — wide confidence intervals, poor S/N ratio. Every quantity below it in this table is worse. This hierarchy is why higher moments and tail risk measures are so challenging — you're estimating harder things with the same limited data.

---

## 9. Summary

| Concept | Key Point |
|---------|-----------|
| **Estimation** | Truth + error. You never know $\mu$; you guess it from data |
| **$\bar{x}$ is a random variable** | Different samples → different $\bar{x}$. The sampling distribution describes this variation |
| **Unbiased** | $E[\bar{x}] = \mu$ — right on average, wrong in any specific instance |
| **Consistent** | $\bar{x} \to \mu$ as $n \to \infty$ — if the process is stationary |
| **Not efficient for fat tails** | The mean is optimal for normal data. Financial returns aren't normal — the median can beat it |
| **MSE = Variance + Bias²** | For $\bar{x}$, MSE = $\sigma^2/n$ (unbiased so bias term is zero) |
| **Confidence interval** | $\bar{x} \pm t_{n-1,\alpha/2} \cdot s/\sqrt{n}$ — with 252 days, typically spans ~±0.15% daily |
| **Bias-variance trade-off** | Longer window = less bias, more variance from regime mixing. Shorter = less variance, more bias from incomplete data |
| **The honest answer** | Your estimate of the mean is noisy, and the noise is large enough that you often can't reject $\mu = 0$ |

---

## 10. Check-in Questions

1. **Why is $\bar{x}$ a random variable but $\mu$ is not? What makes one random and the other fixed?**

2. **If $E[\bar{x}] = \mu$, does that mean my specific $\bar{x} = 0.06\%$ is correct? Explain the gap between "unbiased on average" and "correct in this instance."**

3. **The MSE decomposition is $\text{MSE} = \text{Var} + \text{Bias}^2$. For $\bar{x}$, the bias term is zero so $\text{MSE} = \sigma^2/n$. Consider a *shrinkage* estimator: $\tilde{x} = 0.9 \times \bar{x}$ (pull everything 10% toward zero). This is biased: $E[\tilde{x}] = 0.9\mu \neq \mu$. When might $\tilde{x}$ have lower MSE than $\bar{x}$? Write the condition in terms of $\mu$, $\sigma$, and $n$.**

4. **You compute $\bar{x} = 0.08\%$ daily, $s = 1.3\%$, $n = 63$ (one quarter). Construct the 95% confidence interval for $\mu$. Is zero inside? Compare the width to the $n=252$ case from Section 6.3 — is the ratio of widths exactly $\sqrt{252/63} = 2$? Why or why not?**

5. **The data distribution of daily SPY returns is skewed and fat-tailed. The sampling distribution of $\bar{x}$ is approximately normal (CLT). Explain this transformation. What property of $\bar{x}$ causes the shape to change?**

6. **A colleague says "the sample mean is the best estimator of the population mean — it's the MVUE." Under what assumption is this true? Is that assumption satisfied for financial returns? What happens when it's violated?**

7. **Why don't we just use 5,000 trading days (~20 years) of data to get a razor-sharp estimate of the mean? What's the practical problem?**
