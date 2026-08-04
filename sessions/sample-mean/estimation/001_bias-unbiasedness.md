# Bias and the Unbiasedness Property

**Session:** sample-mean → estimation  
**Topic:** Bias — what it is, why it matters, and why unbiasedness isn't everything  
**Prerequisites:** sample-mean/001 (sample mean as first raw moment), sample-mean/002 (sample mean as estimator)

---

## 1. What Is Bias? Start with a Story

### 1.1 The Bathroom Scale

You buy a cheap bathroom scale. Every morning you step on it.

- **Monday:** 80.2 kg
- **Tuesday:** 79.8 kg
- **Wednesday:** 80.5 kg
- **Thursday:** 79.9 kg
- **Friday:** 80.1 kg

The average is 80.1 kg. The scale bounces around day to day — that's variance. But here's the real question: **is the scale telling the truth on average?**

You go to the doctor's office, where they have a calibrated medical scale. Your true weight: 78.0 kg.

Your bathroom scale is consistently reading about 2.1 kg too high. Over five days, it averaged 80.1 kg — but the truth is 78.0 kg. That gap — the **systematic** overstatement, the error that doesn't cancel out no matter how many times you weigh yourself — **that is bias.**

$$\text{Bias} = \text{Average reading} - \text{True weight} = 80.1 - 78.0 = +2.1 \text{ kg}$$

The formula is simple, but every piece means something specific: **Average reading** (80.1 kg) is what your procedure — the scale — produces on average. **True weight** (78.0 kg) is reality. The difference (+2.1 kg) is the systematic error — it's positive, so the scale overestimates. A negative bias would mean underestimation. Zero would mean the scale is right on average.

### 1.2 Bias in Returns — Same Idea, Different Units

You have 252 daily SPY returns. You compute the sample mean, written as $\bar{x}$ (pronounced "x-bar"):

$$\bar{x} = \frac{\text{return}_1 + \text{return}_2 + \cdots + \text{return}_{252}}{252} = 0.04\%\text{ per day}$$

The true expected daily return of the S&P 500 — the actual value baked into the return-generating process — is some number we can never know. We call it $\mu$ (the Greek letter "mu," the standard symbol for a population mean). Let's say, for the sake of this example, it's really $\mu = 0.03\%$ per day.

Your 252-day average gives $\bar{x} = 0.04\%$. The truth is $\mu = 0.03\%$. Is your procedure systematically off? You can't tell from one sample — maybe this particular 252-day window happened to be slightly above average. But if you repeated the exercise on thousands of different 252-day windows, and the average of all those $\bar{x}$'s came out to 0.04% instead of 0.03% — then your estimator is biased by +0.01% per day. It systematically overestimates.

### 1.3 The Formal Definition — Every Symbol Explained

Here is the formal definition of bias:

$$\text{Bias}(\hat{\theta}) = E[\hat{\theta}] - \theta$$

Let me unpack every symbol:

| Symbol | What it is | In plain English |
|--------|-----------|-----------------|
| $\theta$ | The **parameter** — the true, fixed, unknown value you want to know | The bullseye. The real expected daily return of the S&P 500. You never get to see it |
| $\hat{\theta}$ | The **estimator** — your formula or procedure applied to data. The hat ($\hat{\ }$) means "estimate of" | Your bathroom scale. Your $\bar{x}$ formula. It's a random variable because it depends on which data you got |
| $E[\hat{\theta}]$ | The **expected value** of the estimator — what it averages to over all possible samples you could have drawn | If you weighed yourself on 10,000 different mornings and averaged all the readings, what would that average be? |
| $\text{Bias}(\hat{\theta})$ | The **difference** between where your procedure lands on average and the truth | $E[\hat{\theta}] - \theta$. If positive → overestimates. If negative → underestimates. If zero → **unbiased** |

Applied to estimating the mean: $\hat{\theta}$ is $\bar{x}$, and $\theta$ is $\mu$. So:

$$\text{Bias}(\bar{x}) = E[\bar{x}] - \mu$$

If $E[\bar{x}] = \mu$ (the average of all possible sample means equals the true population mean), then $\text{Bias}(\bar{x}) = 0$ — the sample mean is an **unbiased** estimator.

### 1.4 The Dartboard — Bias vs Variance in One Picture

Picture three dart players:

- **Alice (unbiased, high variance):** Her darts scatter evenly around the bullseye. Some left, some right, some high, some low. Her *average* shot is dead centre. But any individual dart can be way off.
- **Bob (biased, low variance):** Bob's darts cluster in a tight group — but the group is 3 inches above and right of the bullseye. He's consistent (low variance) and systematically wrong (biased).
- **Carol (biased, high variance):** Carol's darts are all over the board, and they tend to land below the bullseye more often than above. She's both imprecise and off-target.

**Key insight:** "Unbiased" is not a compliment about any single throw. It's a statement about the *process* — over a thousand throws, Alice's average lands on the bullseye. Any individual throw can be way off. Bob's throws are all tight and predictable, just in the wrong place. Which is better depends on what you need.

---

## 2. The Sample Mean Is Unbiased — Here's the Proof, Explained

### 2.1 The Formula for the Sample Mean

$$\bar{x} = \frac{x_1 + x_2 + \cdots + x_n}{n}$$

Each $x_i$ is one daily return. $n$ is how many returns you have (typically 252). The numerator adds them all up. The denominator divides by the count. That's it — the simplest possible summary of "what was the typical return."

### 2.2 What We Need to Prove

We want to show: $E[\bar{x}] = \mu$. Read this as: "the expected value of the sample mean equals the true population mean." If this holds, $\text{Bias}(\bar{x}) = E[\bar{x}] - \mu = \mu - \mu = 0$, and $\bar{x}$ is unbiased.

### 2.3 The Proof — Step by Step with Commentary

**Step 1:** Write down what we want to find.

$$E[\bar{x}] = E\left[\frac{x_1 + x_2 + \cdots + x_n}{n}\right]$$

Read as: "the expected value of (the sum of all returns divided by n)."

**Step 2:** Pull the constant $1/n$ outside the expectation. A fundamental rule: $E[c \cdot Y] = c \cdot E[Y]$ for any constant $c$. Here, $c = 1/n$ and $Y$ is the sum inside.

$$= \frac{1}{n} \cdot E[x_1 + x_2 + \cdots + x_n]$$

Read as: "one over n, times the expected value of the sum of all returns."

**Step 3:** The expected value of a sum is the sum of expected values. This is called **linearity of expectation** and it's one of the most powerful properties in all of probability — it always holds, regardless of whether the $x_i$ are independent or correlated.

$$= \frac{1}{n} \cdot (E[x_1] + E[x_2] + \cdots + E[x_n])$$

**Step 4:** We assume every day's return has the same true mean. That is: $E[x_1] = E[x_2] = \cdots = E[x_n] = \mu$. This is the "identical distribution" part of "independent and identically distributed" (i.i.d.). It says each day is drawn from the same return-generating process with the same expected value $\mu$.

$$= \frac{1}{n} \cdot (\mu + \mu + \cdots + \mu)$$

There are $n$ copies of $\mu$ inside the parentheses.

**Step 5:** The sum of $n$ copies of $\mu$ is $n \cdot \mu$.

$$= \frac{1}{n} \cdot n\mu = \mu$$

Done. $E[\bar{x}] = \mu$. The sample mean is unbiased.

### 2.4 What the Proof Assumes — And What It Doesn't

**Only one assumption needed:** every observation has the same mean $\mu$. That's it. We did NOT assume:
- Returns are normally distributed
- Returns are independent (linearity of expectation works even with correlated data)
- Returns have finite variance
- Anything about skewness or kurtosis

This is remarkably mild. The proof is robust.

### 2.5 A Concrete Example — Enumerating All Possible Samples

The proof is abstract. Here's a concrete demonstration you can verify by hand.

Imagine the true daily return process for a stock: each day, flip a fair coin. Heads = +2%. Tails = −1%. The true expected return is:

$$\mu = (0.5 \times +2\%) + (0.5 \times -1\%) = 1.0\% - 0.5\% = +0.5\%$$

Now consider 2-day samples. There are $2^2 = 4$ possible sequences. Let's compute $\bar{x}$ for each:

| Sequence | Day 1 | Day 2 | $\bar{x} = \frac{x_1 + x_2}{2}$ |
|----------|-------|-------|--------------------------------|
| HH | +2% | +2% | $(2 + 2) / 2 = +2.00\%$ |
| HT | +2% | −1% | $(2 + (-1)) / 2 = +0.50\%$ |
| TH | −1% | +2% | $((-1) + 2) / 2 = +0.50\%$ |
| TT | −1% | −1% | $((-1) + (-1)) / 2 = -1.00\%$ |

Now average the four $\bar{x}$ values (each sequence is equally likely — probability 1/4):

$$E[\bar{x}] = \frac{+2.00 + 0.50 + 0.50 + (-1.00)}{4} = \frac{2.00}{4} = +0.50\% = \mu$$

The average of all possible sample means exactly equals the true mean. **That** is unbiasedness — the procedure, averaged over every possible sample, recovers the truth.

### 2.6 What the Proof Does NOT Say

The proof does NOT say your specific $\bar{x} = 0.06\%$ equals $\mu$. Look at the table above — only two of the four samples produced $\bar{x} = 0.50\%$ (the true $\mu$). The other two were way off (+2.00% and −1.00%). Half the time, your estimate is wrong. But the *method itself* is honest — it doesn't systematically push you too high or too low. The errors are symmetric.

---

## 3. The Sample Variance Is Biased — A Worked Example

### 3.1 The Two Variance Formulas

The natural, intuitive way to compute variance from data:

$$\hat{\sigma}^2_{\text{naive}} = \frac{1}{n}\sum_{i=1}^{n} (x_i - \bar{x})^2$$

Let me unpack this notation:
- $x_i$ = each individual return (day $i$)
- $\bar{x}$ = the sample mean (computed from these same returns)
- $(x_i - \bar{x})$ = the deviation — how far day $i$'s return was from the average
- $(x_i - \bar{x})^2$ = the squared deviation (squaring makes negatives positive and penalises large deviations more)
- $\sum_{i=1}^{n}$ = add up all $n$ of these squared deviations
- $\frac{1}{n}$ = divide by the number of observations to get an average

The corrected version (Bessel's correction) divides by $n-1$ instead:

$$s^2 = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar{x})^2$$

Same numerator, different denominator. The $n-1$ instead of $n$ is the correction.

### 3.2 Concrete Computation with Five Returns

Five daily returns: −3%, −1%, 0%, +2%, +5%. First, the sample mean:

$$\bar{x} = \frac{-3 + (-1) + 0 + 2 + 5}{5} = \frac{3}{5} = 0.60\%$$

Now compute each deviation and square it:

| Day $i$ | $x_i$ | Deviation: $x_i - \bar{x}$ | Squared deviation: $(x_i - \bar{x})^2$ |
|--------|-------|---------------------------|---------------------------------------|
| 1 | −3.0% | −3.0 − 0.60 = −3.60% | (−3.60)² = 12.96 |
| 2 | −1.0% | −1.0 − 0.60 = −1.60% | (−1.60)² = 2.56 |
| 3 | 0.0% | 0.0 − 0.60 = −0.60% | (−0.60)² = 0.36 |
| 4 | +2.0% | 2.0 − 0.60 = +1.40% | (1.40)² = 1.96 |
| 5 | +5.0% | 5.0 − 0.60 = +4.40% | (4.40)² = 19.36 |

Sum of squared deviations = 12.96 + 2.56 + 0.36 + 1.96 + 19.36 = **37.20**.

**Naive variance** (divide by $n=5$): $\frac{37.20}{5} = 7.44$  
**Corrected variance** (divide by $n-1=4$): $\frac{37.20}{4} = 9.30$

The difference is $9.30 - 7.44 = 1.86$ — the naive version is 20% smaller. Which is right? The corrected one (9.30). The naive one (7.44) is **biased downward.**

### 3.3 Why Is It Biased? The $\bar{x}$ Problem

The deviations use $\bar{x}$ = 0.60%, which we estimated from the same five returns. But $\bar{x}$ has a special property: it's the exact number that **minimises** the sum of squared deviations. No other number produces a smaller sum.

Let's verify: what if we used a different centre point — say, the true $\mu = 0\%$?

| Day | $x_i$ | $x_i - \mu$ | $(x_i - \mu)^2$ |
|-----|-------|------------|-----------------|
| 1 | −3.0% | −3.00% | 9.00 |
| 2 | −1.0% | −1.00% | 1.00 |
| 3 | 0.0% | 0.00% | 0.00 |
| 4 | +2.0% | +2.00% | 4.00 |
| 5 | +5.0% | +5.00% | 25.00 |

Sum = 39.00. Divide by 5 → 7.80.

Notice: $7.80 > 7.44$. The squared deviations from $\mu$ are larger than the squared deviations from $\bar{x}$. That's not a coincidence — $\bar{x}$ is the point that makes squared deviations as small as possible. **Any other point — including the true $\mu$ — gives a larger sum.**

So when you use $\bar{x}$ in the variance formula, you're systematically making the spread look smaller than it really is. The "double use" of the data — once to find the centre, again to measure spread from that centre — creates a downward bias. Bessel's correction ($n-1$ instead of $n$) inflates the result to compensate.

### 3.4 A Physical Analogy

Measure the height of five people. Compute the average: 172 cm. Now measure how far each person is from that average.

But your "average" was computed from those same five people. If one person is unusually tall (195 cm), they pull the average upward — making their own deviation (195 − 172 = 23 cm) smaller than it "should" be relative to the true population average (maybe 170 cm, giving 195 − 170 = 25 cm). Every person's deviation is slightly shrunk because the centre was fitted to them.

That shrinkage always happens. Bessel's correction inflates the variance to undo it.

### 3.5 How Much Does It Matter for Different Sample Sizes?

| Sample size $n$ | Bias factor = $(n-1)/n$ | Example: true $\sigma^2 = 2.25$ |
|---|---|---|
| 5 | 4/5 = 0.80 | Naive estimate averages 1.80 instead of 2.25 (20% low) |
| 10 | 9/10 = 0.90 | Naive estimate averages 2.025 (10% low) |
| 30 | 29/30 ≈ 0.967 | Naive estimate averages 2.175 (3.3% low) |
| 252 | 251/252 ≈ 0.996 | Naive estimate averages 2.241 (0.4% low) |

At $n = 252$ (one trading year), the bias is trivial — 0.4%. At $n = 5$, it's massive — 20%. For VaR with 252-day windows, this correction barely matters numerically. But the *concept* is crucial: naive plug-in estimators are often biased, and understanding why is part of estimation literacy.

---

## 4. Where Does Bias Come From? Five Stories

### 4.1 Story 1: Double-Using the Data (Variance Bias)

You use your data to estimate the centre ($\bar{x}$), then reuse the same data to measure spread from that centre. The centre was chosen to make spread look as small as possible → spread is biased downward. The fix: Bessel's correction ($n-1$).

**The lesson:** Anytime you estimate a parameter and then reuse the data as if that estimate were the truth, bias creeps in.

### 4.2 Story 2: Nonlinear Transformations — Jensen's Inequality

You estimate variance: $s^2 = 2.25$ (unbiased, using $n-1$). Then you take the square root to get standard deviation: $s = \sqrt{2.25} = 1.50$.

Seems fine — but here's the trap. $s^2$ is unbiased *on average across samples*. The square root function $\sqrt{\ }$ is curved (concave) — it bends downward. The average of the square roots is NOT the square root of the average.

**Concrete example with two possible samples:**

| Sample | $s^2$ (unbiased) | $s = \sqrt{s^2}$ |
|--------|-----------------|------------------|
| 1 | 1.00 | 1.00 |
| 2 | 4.00 | 2.00 |

Average $s^2$ across samples: $(1.00 + 4.00) / 2 = 2.50$  
If true $\sigma^2 = 2.50$, then $s^2$ is unbiased — its average equals the truth.

Average $s$ across samples: $(1.00 + 2.00) / 2 = 1.50$  
Square root of the average $s^2$: $\sqrt{2.50} = 1.58$

$1.50 < 1.58$. The average $s$ is below the square root of the average $s^2$. The estimator $s = \sqrt{s^2}$ is biased downward — even though $s^2$ itself is unbiased. At $n = 252$, this bias is tiny (~0.1%). At small $n$, it's material.

**The lesson:** Unbiasedness doesn't survive nonlinear transformations. If you take a nonlinear function $f$ of an unbiased estimator, $f(\text{estimate})$ is generally not unbiased for $f(\text{truth})$. This is Jensen's inequality: for a concave function like $\sqrt{\ }$, $E[f(X)] < f(E[X])$.

### 4.3 Story 3: Survivorship Bias

You download historical stock returns for the S&P 500 and compute the average annual return: 10.2%. Impressive.

But the S&P 500 index composition changes. Companies that go bankrupt get removed. Companies that thrive get added. The historical returns you see are the *survivors* — the ones that made it. Enron, Lehman, WorldCom? Not in your dataset for the years after they collapsed.

If you'd included the delisted, bankrupted companies, the average might be 8.7%. Your estimator is biased upward by about 1.5% per year — because your sample systematically excludes the worst outcomes.

**The lesson:** What's NOT in your data can bias you just as much as what IS in it.

### 4.4 Story 4: Look-Ahead Bias

You're backtesting a value strategy: buy the 20% of stocks with the lowest P/E ratios, hold for a year. You compute each stock's P/E using its *trailing* earnings for the full year. Average return: 15% annualised. Looks great.

The problem: at the start of the year, you wouldn't have known the full-year earnings — they hadn't been reported yet. Your backtest used information from the future to select stocks in the past. That's look-ahead bias. Real-time performance would be worse.

**The lesson:** Your estimator must only use information available at the time the decision was made.

### 4.5 Story 5: Model Misspecification

You assume daily returns are normally distributed. Under normality, the 1st percentile (the 99% VaR threshold) sits exactly at $\mu - 2.326\sigma$. You compute parametric VaR using this formula.

But real returns have fat tails. The actual 1st percentile might sit at $\mu - 3.1\sigma$. Your normality assumption systematically understates the distance to the tail. Even if your estimates of $\mu$ and $\sigma$ are perfectly unbiased, the model itself is wrong — and that structural error produces biased risk estimates.

**The lesson:** Even with perfectly unbiased parameter estimates, the wrong model introduces bias into your conclusions.

---

## 5. Why Unbiasedness Isn't the Only Goal

### 5.1 The Bias-Variance Trade-off

Recall Alice (unbiased, darts scattered widely around bullseye) and Bob (biased, darts clustered tightly 3 inches off-centre).

Who's better? It depends on the game:

- **If you're averaging thousands of throws:** Alice. Her errors are symmetric — they cancel. Her average is the bullseye.
- **If you get ONE throw and a miss costs you the tournament:** Bob. He's predictably 3 inches off — you can aim 3 inches low and left to compensate. Alice might hit the bullseye or miss by a foot. You can't predict which.

The same logic applies to estimators. The total expected penalty for being wrong is captured by **Mean Squared Error (MSE):**

$$\text{MSE} = E[(\hat{\theta} - \theta)^2]$$

Let me unpack: $\hat{\theta}$ is your estimate, $\theta$ is the truth, $(\hat{\theta} - \theta)^2$ is the squared error for one sample, and $E[\cdot]$ averages that squared error over all possible samples. MSE answers: "on average, how far off am I, with large errors penalised heavily?"

MSE decomposes into two pieces:

$$\text{MSE} = \text{Variance} + \text{Bias}^2$$

Where:
- **Variance** = how much your estimate bounces around from sample to sample (the scatter of the darts)
- **Bias²** = the square of the systematic offset (how far the cluster is from the bullseye, squared)

If Bias = 0 (Alice), then MSE = Variance. If Bias ≠ 0 but Variance is tiny (Bob), MSE could still be lower than Alice's — the tight cluster outweighs being off-centre.

### 5.2 Shrinkage: Deliberately Introducing Bias to Reduce Total Error

Here's a deliberately biased estimator for the mean:

$$\tilde{\mu} = 0.95 \times \bar{x}$$

Take your sample mean and multiply it by 0.95 — shrink it 5% toward zero. This is clearly biased: if $\mu = 0.05\%$, then on average $E[\tilde{\mu}] = 0.95 \times 0.05\% = 0.0475\%$, which is short of the truth by 0.0025%.

**Why would anyone do this?** Because shrinking reduces variance — and variance may be the bigger enemy.

Every estimate bounces around. $\bar{x}$ has variance $\sigma^2/n$. The shrunk version has variance:

$$\text{Var}(\tilde{\mu}) = \text{Var}(0.95 \times \bar{x}) = 0.95^2 \times \text{Var}(\bar{x}) = 0.9025 \times \frac{\sigma^2}{n}$$

The variance is reduced by about 10% (since $0.95^2 = 0.9025$). You pay for this with bias. The question is whether the trade is worth it.

**Concrete example:** $\bar{x} = 0.15\%$ from a volatile period ($\sigma = 1.5\%, n = 100$). The shrunk estimate is $0.95 \times 0.15\% = 0.1425\%$.

| Scenario | True $\mu$ | Error of $\bar{x}$ | Error of shrunk | Which wins? |
|----------|-----------|-------------------|-----------------|-------------|
| Mean near zero | 0.05% | 0.15 − 0.05 = +0.10% | 0.1425 − 0.05 = +0.0925% | Shrunk (slightly) |
| Mean equals estimate | 0.15% | 0.15 − 0.15 = 0% | 0.1425 − 0.15 = −0.0075% | $\bar{x}$ (barely) |
| Mean is negative | −0.05% | 0.15 − (−0.05) = +0.20% | 0.1425 − (−0.05) = +0.1925% | Shrunk |

Across these scenarios, the shrunk estimator is *never much worse* (max loss: 0.0075%) and *sometimes meaningfully better* (gains of 0.0075%). This pattern holds for daily returns where the true mean is small relative to the noise — the variance reduction reliably outweighs the small bias cost.

### 5.3 The James-Stein Shock — When Unbiasedness Is Provably Suboptimal

In 1961, Charles Stein proved something that stunned statisticians.

You're estimating the expected returns of three completely unrelated stocks: a US tech company, a Japanese bank, and a Brazilian miner. Their true means ($\mu_1, \mu_2, \mu_3$) are totally independent — knowing one tells you nothing about the others. You compute $\bar{x}_1 = 0.12\%, \bar{x}_2 = 0.03\%, \bar{x}_3 = 0.18\%$ from 252 days of data.

The standard approach: use each $\bar{x}_i$ as your estimate of $\mu_i$. Unbiased, straightforward.

Stein showed you can **beat this** — for all three estimates simultaneously — by shrinking each one toward the overall average of the three ($0.11\%$). Even though the true means have nothing to do with each other, the shrinkage estimator has uniformly lower total MSE.

**Why does this work?** Think about the one that's 0.18%. It's the highest of the three. Is it high because that stock genuinely has a higher expected return? Or partly because it got lucky — positive sampling error in that particular 252-day window? You can't know, but *on average*, the highest sample mean in a group is inflated by positive sampling error (regression to the mean). Shrinking it downward toward the group centre corrects for that. Same logic in reverse for the lowest one (0.03%).

**This is profound:** when estimating three or more quantities at once, the best estimator deliberately introduces bias. Unbiasedness is not the optimal strategy.

### 5.4 When Unbiasedness Really Matters

| Scenario | Unbiasedness critical? | Why |
|----------|----------------------|-----|
| Regulator computing risk charges for 500 banks | **Yes** | Biases accumulate — 500 small upward biases = one large systemic undercharge |
| Your single VaR number for tomorrow's limit | **Not necessarily** | Total error (bias² + variance) is what bites you on one decision |
| Averaging expected returns across a diversified portfolio of 1,000 stocks | **Yes** | You're aggregating; biases add up across positions |
| Nuisance parameter feeding into a larger model | **Not necessarily** | Small bias in an intermediate step may be tolerable if variance drops substantially |

---

## 6. When the Sample Mean ISN'T Unbiased

### 6.1 Story: The Regime Change

It's January 2021. You want to estimate the expected daily return of a volatility-targeting fund *going forward*. You use 252 days of data, going back to January 2020.

March 2020 happened in between. COVID crash. VIX at 82. The fund's returns during that month were extreme — nothing like the calm periods before or after.

Your 252-day average includes March 2020. That crash month pulls the average down. If you're trying to estimate the fund's expected return in the *current, post-crash* environment, that average is contaminated. The crash represents a different regime — a different return-generating process with a different mean.

**Is the estimator biased?** For the question "what was the average return over Jan 2020–Jan 2021?" — no, it's perfectly unbiased. For the question "what is the expected return going forward?" — yes, because you're averaging across two different regimes and the answer is an average of two different $\mu$'s, neither of which equals today's $\mu$.

### 6.2 When the Assumptions Break

The proof that $\bar{x}$ is unbiased requires $E[x_i] = \mu$ — every observation has the same mean. When that fails:

| Problem | Example | What $E[\bar{x}]$ actually equals |
|---|---|---|
| **Regime change** | Pre- and post-crisis data in one average | $\frac{1}{n}(\mu_{\text{pre}} \times n_{\text{pre}} + \mu_{\text{post}} \times n_{\text{post}})$ — a blend, not today's $\mu$ |
| **Survivorship** | Only analysing funds that still exist today | $\mu_{\text{survivors}}$ — upward-biased for the full universe |
| **Selection** | Only studying stocks priced above $5 | $\mu_{\text{selected}}$ — biased upward because the worst performers get excluded |
| **Wrong data** | Using bid prices when you trade at the offer | Unbiased for the bid-ask midpoint, biased for your actual transaction cost |

---

## 7. Bias in Finance: Practical Examples

### 7.1 Maximum Drawdown Is Always Too Optimistic

You backtest a strategy over 5 years. The worst peak-to-trough decline was 22%. You tell investors: "maximum drawdown is 22%."

The uncomfortable truth: the true maximum drawdown this strategy *can* produce over a longer horizon is almost certainly worse than 22%. You observed one 5-year sample path. The worst thing that happened in that path is unlikely to be the worst thing the process is capable of. The sample maximum is a biased estimator of the population maximum — biased downward, always.

Same logic applies to: worst daily loss ever observed, maximum consecutive losing days, maximum correlation spike during a crisis. **Extreme value statistics are almost always biased from finite samples** — and the bias is always in the reassuring direction.

### 7.2 Sample Correlations Are Too Close to Zero

You estimate the correlation between two assets using 60 daily returns. Sample correlation $r = 0.45$.

The true correlation $\rho$ might be 0.52. Sample correlations are biased toward zero — the bias is worse when $|\rho|$ is far from zero and $n$ is small. At $n = 252$, negligible. At $n = 20$ (one month), real — your diversification benefit looks better than it actually is.

### 7.3 VaR Backtesting Looks Too Good in Calm Markets

Your 95% VaR model was calibrated during a calm period. Last year, out of 252 days, only 7 days broke the VaR limit. Expected exceptions: 13 (5% of 252).

Is your model excellent? Or is your estimate of exception frequency biased? You can't tell. If the true tail probability is 5%, then 7/252 is just sampling variation — you got a quiet year. But if your model was calibrated to calm data and the true exception probability is only 3%, then the 7 exceptions reflect a biased, overconfident model — and the next volatile year will expose it catastrophically.

---

## 8. Can You Detect Bias? (Usually Not)

### 8.1 The Fundamental Problem

$$\text{Bias} = E[\hat{\theta}] - \theta$$

This formula compares your estimator's average to the truth. You don't know $\theta$ — that's the whole reason you're estimating. Therefore you cannot compute bias from your data.

You can never look at a single $\bar{x} = 0.06\%$ and say "this is biased by +0.02%." To know the bias, you'd need to know $\mu$ — and if you knew $\mu$, you wouldn't need $\bar{x}$.

### 8.2 Three Things You CAN Do

**Approach 1: Simulation.** Assume a specific data-generating process (e.g., $\mu = 0.03\%, \sigma = 1.2\%$, normally distributed). Simulate 10,000 samples of 252 days. Compute your estimator on each. If the average of those 10,000 estimates equals 0.03%, your procedure is unbiased (under this assumed process). If it's 0.04%, you've found a +0.01% bias. This doesn't prove anything about reality — it proves your estimator works under your assumptions.

**Approach 2: Theoretical analysis.** Derive the bias mathematically, as we did for sample variance. Requires knowing your estimator's properties and your data's distribution.

**Approach 3: Compare estimators.** If the sample mean gives 0.15% and the median gives 0.03% on the same data, something is off. One (or both) is biased. The discrepancy flags a problem, even if it can't tell you which one is wrong.

### 8.3 What to Do When You Find or Suspect Bias

| Situation | Action |
|---|---|
| Bias is known and the correction is simple | Fix it (use $n-1$ for variance) |
| Bias is tiny at your working sample size | Accept it (std dev bias at $n=252$ is ~0.1%) |
| Bias is inherent to the estimator's design | Switch estimators (use median instead of mean for fat-tailed data) |
| Bias depends on unknown parameters | Bootstrap: resample your data, estimate the bias from the resamples, subtract it from your original estimate |

---

## 9. The Big Picture

### 9.1 Unbiasedness Is About the Procedure, Never the Result

"The sample mean is unbiased" is a statement about the formula $\frac{1}{n}\sum x_i$ applied to well-behaved data. It is not a statement about your specific $\bar{x} = 0.06\%$.

It's like saying "this coin is fair." It doesn't mean the next flip will be heads exactly 50% of the time — obviously it can't be, it's one flip. It means the *process* of flipping this coin produces heads 50% of the time in the long run. Your one flip could be heads or tails. The process is fair; the outcome is uncertain.

### 9.2 Error Is the Real Enemy, Not Bias Alone

Total expected squared error = Variance + Bias².

A bathroom scale that always reads exactly 2 kg high (biased, zero variance) beats a scale that's correct on average but swings ±5 kg day to day (unbiased, high variance). You can subtract 2 kg. You can't subtract random ±5 kg swings. The biased scale has lower total error.

In estimation, this means: **a small, known bias is often preferable to large, unpredictable variance.** This is especially true for financial returns, where variance dominates bias in the error budget.

### 9.3 Stationarity Is the Hidden Assumption

The biggest practical threat to unbiasedness in finance isn't a math error — it's averaging across different market regimes. When the world changes, old data has a different mean from new data. Your 252-day window innocently averages them together, producing an estimate that's unbiased for the *historical blend* but biased for *today*. The estimator is honest about the past but dishonest about the present — and you usually can't tell.

---

## 10. Summary

| Concept | The idea | Concrete anchor |
|---|---|---|
| **Bias** | $E[\hat{\theta}] - \theta$ — the systematic gap between your procedure's average and the truth | Bathroom scale always reads 2 kg high. No amount of re-weighing fixes it |
| **Unbiasedness** | $E[\hat{\theta}] = \theta$ — the procedure is centred on the truth | Coin-flip stock: average of all possible 2-day $\bar{x}$'s = true $\mu = +0.5\%$ |
| **$\bar{x}$ is unbiased** | Proof requires only $E[x_i] = \mu$. No normality, no independence needed | Works for any distribution with a finite mean |
| **Sample variance is biased** | Using $\bar{x}$ makes deviations too small — $\bar{x}$ was chosen to minimise them | 5 returns: naive gives 7.44, corrected gives 9.30. Divide by $n-1$ |
| **Bias-variance trade-off** | MSE = Variance + Bias². A little bias can be worth a lot less variance | Shrinking $\bar{x}$ by 5%: lose ~0.0025% to bias, gain ~10% lower variance |
| **Regime change breaks it** | Averaging across different market regimes blends different means | Including March 2020 crash in your "normal" expected return estimate |
| **Extreme values are biased** | Worst thing seen < worst thing possible — always | Historical max drawdown of 22% — the process can almost certainly do worse |
| **Can't detect bias from data** | Requires knowing the truth, which you don't | A single $\bar{x} = 0.06\%$ contains zero information about systematic error |

---

## 11. Check-in Questions

1. **You step on a bathroom scale five times: 79.8, 80.2, 79.9, 80.1, 80.0 kg. Your true weight is 78.0 kg. Is the scale biased? Is it precise? Explain the difference between bias and variance in your own words.**

2. **For the coin-flip stock (heads = +2%, tails = −1%): list all 8 possible 3-day sequences. Compute $\bar{x}$ for each. Average them. Show the average equals the true $\mu$ of +0.5%.**

3. **Your friend computes variance as $\frac{1}{n}\sum(x_i - \bar{x})^2$ on 10 returns and gets 4.50. You recalculate with $n-1$ and get 5.00. Explain to your friend — in plain language, with a concrete example — why dividing by 9 is right and dividing by 10 systematically underestimates.**

4. **Your $\bar{x} = 0.12\%$ daily, $s = 1.5\%$, $n = 100$. Compare $\bar{x}$ (unbiased) to the shrunk estimator $0.9 \times \bar{x} = 0.108\%$ (biased). If true $\mu = 0.05\%$, which is closer to the truth? If true $\mu = 0.12\%$, which is closer? Why might the shrunk estimator still be preferable overall?**

5. **You have 10 years of daily data on a hedge fund. The fund changed strategy 3 years ago. 10-year average: 15% annualised. Post-change 3-year average: 8%. Is the 10-year average biased as an estimate of the fund's *current* expected return? Explain why the estimator can be unbiased for one question and biased for another.**

6. **Why is "the worst drawdown I've ever seen" a biased estimator of "the worst drawdown this strategy can produce"? Use the dartboard analogy — why can't the bias ever go the other way (overstating the worst possible drawdown)?**

7. **A risk manager says: "my 95% VaR model had exactly 13 exceptions last year out of 252 days — exactly 5%, so it's perfectly calibrated." Is one year of "right" exceptions evidence that the model is unbiased? What would you need to actually assess bias in the exception rate?**