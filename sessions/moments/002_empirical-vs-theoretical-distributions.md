# Empirical Distributions vs Probability Distributions — and Why Moments Bridge Them

**Date:** 2026-07-26
**Topic:** The distinction between the shape your data actually has and the shape a model assumes, with moments as the comparison tool.

---

## Opening Question

> You have 252 daily SPY returns. You plot a histogram. You also draw a bell curve on top. They don't match — the histogram has a fatter left tail and more extreme bumps on both sides. What exactly are you comparing? Two different kinds of "distribution." Understanding the difference is understanding everything parametric VaR gets wrong.

---

## 1. Start With a Concrete Example

Let's work with actual numbers so the concepts have something to attach to.

Here are 10 daily SPY returns (fictional but realistic):

```
−1.8%, +0.5%, −0.3%, +2.1%, −2.4%, +0.1%, +0.8%, −0.6%, +1.5%, −0.2%
```

### The empirical distribution — what the data actually looks like

If I ask "what's the distribution of these returns?", the honest answer is: **this exact set of 10 numbers, each appearing once.** The empirical distribution is just the data itself, summarised:

| Return | Frequency | Relative frequency |
|--------|-----------|-------------------|
| −2.4% | 1 | 0.1 |
| −1.8% | 1 | 0.1 |
| −0.6% | 1 | 0.1 |
| −0.3% | 1 | 0.1 |
| −0.2% | 1 | 0.1 |
| +0.1% | 1 | 0.1 |
| +0.5% | 1 | 0.1 |
| +0.8% | 1 | 0.1 |
| +1.5% | 1 | 0.1 |
| +2.1% | 1 | 0.1 |

The empirical CDF is simple: $F(x) = \frac{\text{count of returns} \leq x}{n}$. At $x = -0.3\%$, $F(-0.3\%) = 4/10 = 0.4$. At $x = +0.5\%$, $F(+0.5\%) = 6/10 = 0.6$. The 5th percentile (VaR at 95% confidence) is the smallest observation: −2.4%.

> **The empirical distribution is a description of what happened. It has no opinions, no assumptions, no model. It is the data, tabulated.**

### The theoretical distribution — a mathematical model

Now someone says: "These returns probably come from a normal distribution. Let me fit one."

They compute $\bar{x} = -0.03\%$ and $s = 1.41\%$. Then they declare: "The returns follow $N(-0.03\%, 1.41\%^2)$." This is a theoretical distribution — an equation:

$$f(x) = \frac{1}{1.41\% \times \sqrt{2\pi}} \cdot e^{-\frac{(x + 0.03\%)^2}{2 \times (1.41\%)^2}}$$

> **The theoretical distribution is a model of how the data was generated. It's a claim: "the underlying random process that produces these returns follows this equation."**

---

## 2. The Fundamental Difference, Laid Out

| | Empirical Distribution | Theoretical (Probability) Distribution |
|---|---|---|
| **What it is** | A summary of observed data | A mathematical model |
| **Where it comes from** | Your data. Sort it, count it, plot it. | An equation. Someone (you) *chooses* it. |
| **What it answers** | "What happened?" | "What should happen, on average, in the long run?" |
| **Is it "true"?** | It's what you observed. It's a fact about your sample. | It's an assumption. It might be wrong. |
| **Does it have parameters?** | Not really — just the data points themselves | Yes — μ, σ, degrees of freedom, etc. |
| **Does it change with more data?** | Yes — each new observation changes the histogram | No — the equation stays the same, though your parameter estimates change |
| **Can you draw from it?** | Sampling with replacement (bootstrapping) | Sampling from the equation (Monte Carlo simulation) |
| **Does it generalise?** | Only to the observed range. You can't observe a −8% day if none occurred. | Yes — the model extends to infinity. It predicts probabilities for events you've never seen. |

### The critical distinction in one sentence

> The empirical distribution tells you what *did* happen. The theoretical distribution is a bet on what *could* happen — including things that haven't happened yet.

---

## 3. Why This Distinction Is the Heart of VaR Methodology Choice

Every VaR method takes a position on this distinction:

### Historical VaR — uses the empirical distribution

**What it does:** Sort the 252 returns. Take the 13th-worst. That's VaR.

**What it assumes:** The future will look like the past — not in a parametric sense, but literally: tomorrow's return will be drawn from the same empirical distribution as the last 252 days. No model. No equation. Just: "what was the 5th percentile of the actual returns?"

**What it gains:** No distributional assumptions. Whatever shape your returns actually have — negative skew, fat tails, weird multimodality — historical VaR respects it. The empirical distribution *is* the shape.

**What it loses:** You can't see beyond your data. If the worst return in 252 days was −4.2%, your VaR at 99% confidence (the 1st percentile, roughly the 3rd-worst day) is bounded by −4.2%. You cannot estimate a −8% VaR if no −8% day occurred. The empirical distribution has a hard edge at the most extreme observation.

### Parametric VaR — uses a theoretical distribution

**What it does:** Fit a normal distribution to the data. Compute $\text{VaR}_{95\%} = \hat{\mu} - 1.645\hat{\sigma}$.

**What it assumes:** The returns *come from* a normal distribution. The data you observed is a sample from $N(\mu, \sigma^2)$. The true shape has skewness = 0 and kurtosis = 3.

**What it gains:** Extrapolation. The normal distribution extends to $-\infty$. You can compute a 99.9% VaR even if your 252-day sample has nothing close to that extreme. The model fills in the tail.

**What it loses:** If the theoretical distribution is wrong about the shape — specifically about skewness and kurtosis — then VaR is wrong. For financial returns, it's wrong in a specific direction: VaR is *understated* (too optimistic) because real returns have fatter left tails than normal.

### Monte Carlo VaR — samples from a theoretical distribution

**What it does:** Pick a theoretical distribution (normal, t, something else). Draw 10,000 random returns from it. Sort. Take the 5th percentile.

**What it assumes:** Same as parametric — the returns come from whatever distribution you chose. The difference is computational: instead of using a formula for the quantile, you simulate and read it off, the same way historical VaR reads off the empirical distribution.

**Where it sits:** Monte Carlo is parametric VaR with a simulation engine. It uses a theoretical distribution but computes everything empirically. This lets you use distributions that don't have a nice quantile formula (mixture models, regime-switching models) — but it's still a theoretical distribution underneath.

---

## 4. Moments — the Common Language Between the Two Worlds

You can compute moments from both:

### From the empirical distribution (sample moments)

$$\hat{\mu} = \frac{1}{n}\sum_{i=1}^n x_i \quad\quad \hat{\sigma}^2 = \frac{1}{n-1}\sum_{i=1}^n (x_i - \bar{x})^2$$

$$\hat{\gamma}_1 = \frac{1}{n}\sum_{i=1}^n \left(\frac{x_i - \bar{x}}{s}\right)^3 \quad\quad \hat{\gamma}_2 = \frac{1}{n}\sum_{i=1}^n \left(\frac{x_i - \bar{x}}{s}\right)^4 - 3$$

These are *estimates*. They describe the shape of the data you observed. They have sampling error — a different sample of 252 days gives different numbers.

### From the theoretical distribution (population moments)

For a normal distribution $N(\mu, \sigma^2)$:

$$E[X] = \mu \quad\quad \text{Var}(X) = \sigma^2 \quad\quad \text{Skew}(X) = 0 \quad\quad \text{Kurt}(X) = 3$$

These are *parameters* — fixed properties of the equation. They don't have sampling error. They are true by definition for the model.

### The comparison

| Moment | Empirical (your SPY data) | Theoretical (normal fit) | Match? |
|--------|--------------------------|--------------------------|--------|
| Mean | ≈ +0.04% | $\hat{\mu} \approx +0.04\%$ | By construction |
| Std Dev | ≈ 1.2% | $\hat{\sigma} \approx 1.2\%$ | By construction |
| Skewness | ≈ −0.6 | 0 (forced) | **No — the mismatch** |
| Kurtosis | ≈ 6–8 (excess = 3–5) | 3 (forced) | **No — the mismatch** |

> The empirical and theoretical distributions match on the first two moments *because we forced them to* — those are the parameters we fitted. They disagree on moments 3 and 4 because the normal distribution *cannot* produce negative skew or excess kurtosis. The empirical distribution can — because it's the actual shape of the data.

---

## 5. The Parameter vs Estimate Distinction (Don't Skip This)

This is a subtle but critical concept that ties together everything above.

### Parameters live in the theoretical world

A **parameter** is a fixed, unknown number that describes the theoretical distribution. $\mu$ and $\sigma^2$ are parameters of the normal distribution. They exist whether or not you have data. They are properties of the *model*, not of the *sample*.

Think of it like this: if returns truly come from $N(0.04\%, 1.2\%^2)$, then $\mu = 0.04\%$ is a fact about the universe. You don't know it — you can only estimate it from data — but it exists.

### Estimates live in the empirical world

An **estimate** (or **statistic**) is a number you compute from data. $\bar{x}$ and $s^2$ are estimates of $\mu$ and $\sigma^2$. They are functions of your sample. A different sample gives a different estimate.

### The relationship

$$\underbrace{\bar{x}}_{\text{estimate — from data}} \xrightarrow{\text{is our best guess of}} \underbrace{\mu}_{\text{parameter — a property of the model}}$$

The distinction matters because:
- You can never *know* $\mu$. You can only estimate it.
- Your estimate has error. $\bar{x} \neq \mu$ almost surely.
- As $n$ grows, the error shrinks (if the estimator is consistent).
- But the parameter $\mu$ never changes — only your estimate of it does.

### Why this matters for VaR

When you compute parametric VaR, you plug *estimates* into a formula derived for *parameters*:

$$\widehat{\text{VaR}}_{95\%} = \bar{x} - 1.645 \cdot s$$

This is an estimate of the true parametric VaR, which would be:

$$\text{VaR}_{95\%} = \mu - 1.645 \cdot \sigma$$

The error in your VaR number comes from two sources:
1. **Estimation error:** $\bar{x} \neq \mu$ and $s \neq \sigma$. Your sample didn't perfectly capture the true parameters.
2. **Model error:** The true distribution isn't normal at all, so even if you knew $\mu$ and $\sigma$ exactly, the formula $\mu - 1.645\sigma$ doesn't give the right quantile — because the true distribution has $\gamma_1 \neq 0$ and $\gamma_2 \neq 3$.

Historical VaR avoids model error (no distributional assumption) but not estimation error (the empirical distribution is an *estimate* of the true distribution — 252 days might not be representative of the true return-generating process).

---

## 6. A Worked Example — Same Data, Two Distributions, Different VaR

Let's use the 10-return example from Section 1 and compute VaR at 80% confidence (we need a coarser quantile with only 10 observations).

**The data:**
```
−2.4%, −1.8%, −0.6%, −0.3%, −0.2%, +0.1%, +0.5%, +0.8%, +1.5%, +2.1%
```

### Historical VaR (empirical distribution)

Sort ascending. The 20th percentile (2nd observation out of 10):

Sorted: −2.4%, −1.8%, −0.6%, −0.3%, −0.2%, +0.1%, +0.5%, +0.8%, +1.5%, +2.1%

$\text{VaR}_{80\%}^{\text{historical}} = -1.8\%$

"That's how bad the 2nd-worst day was."

### Parametric VaR (normal distribution)

Fitted parameters: $\bar{x} = -0.03\%$, $s = 1.41\%$

For 80% confidence, the normal quantile is $z_{0.20} = -0.842$ (20th percentile of standard normal).

$\text{VaR}_{80\%}^{\text{parametric}} = -0.03\% - 0.842 \cdot 1.41\% = -1.22\%$

"The normal distribution says the 20th percentile should be −1.22%."

### The gap

$$\text{Gap} = -1.8\% - (-1.22\%) = -0.58\%$$

The empirical distribution says things are worse. Why? Because the data has negative skew — the left tail extends further than a symmetric normal distribution would predict. The two worst returns (−2.4% and −1.8%) pull the empirical quantile further left than the mathematical quantile from the normal curve.

**This gap — -0.58% — is the higher moments at work.** It's the cost of assuming normality when the data isn't normal.

---

## 7. The Full Picture — How These Concepts Stack

```
REALITY                          YOUR TOOLKIT
───────                          ────────────
                                 
The true return-generating       You never see this.
process (unknown)                It's what you're trying
    │                            to understand.
    │ generates                  
    ▼                            
Observed returns                 THE EMPIRICAL DISTRIBUTION
(x₁, x₂, ..., x₂₅₂)             • Sort, count, plot
    │                            • Sample moments: x̄, s², γ̂₁, γ̂₂
    │                            • Historical VaR reads directly from it
    │                            
    ├── "I'll assume these       THE THEORETICAL DISTRIBUTION
    │    came from N(μ,σ²)"      • An equation: f(x) = ...
    │                            • Population moments: μ, σ², γ₁=0, γ₂=3
    │                            • Parametric VaR = μ − z·σ
    │                            
    ├── "I'll compare the        MOMENTS AS THE BRIDGE
    │    moments"                • Compare γ̂₁ vs 0, γ̂₂ vs 3
    │                            • The gap tells you how wrong normality is
    │                            
    └── "I'll pick a better      BETTER THEORETICAL DISTRIBUTIONS
         distribution"           • Student's t (adjustable kurtosis)
                                 • Skewed-t (adjustable skew + kurtosis)
                                 • Cornish-Fisher (adjust normal quantile 
                                   using empirical γ̂₁, γ̂₂)
```

---

## 8. Three Traps to Avoid

### Trap 1: "The empirical distribution IS the true distribution"

It's not. It's a sample from the true distribution. If you observed 252 calm days because you happened to sample a low-volatility period, your empirical distribution understates risk. The true process might generate much worse days — you just haven't seen them yet.

This is why a 252-day window during 2017 gave a VaR that was useless in February 2018 (the "volmageddon" event). The empirical distribution from 2017 said "volatility is low, the worst day was −1.5%." The true process had much fatter tails — they just hadn't been sampled recently.

### Trap 2: "The theoretical distribution is just a fitted version of the empirical one"

No. Fitting is the *estimation* step — you compute $\hat{\mu}$ and $\hat{\sigma}$ from the data. But the *model* itself is a claim about the shape: it forces $\gamma_1 = 0$ and $\gamma_2 = 3$. These aren't fitted — they're *assumed*. The normal distribution can't produce skewness no matter how much data you feed it.

### Trap 3: "If I use a better theoretical distribution, I don't need to worry about moments"

The Student's t-distribution has a parameter $\nu$ (degrees of freedom) that controls kurtosis. Lower $\nu$ → fatter tails. You can estimate $\nu$ from data, so the theoretical distribution *can* match the empirical kurtosis. But you're still making an assumption: that the data comes from a t-distribution. What if the true process is a mixture of two normals? Or has time-varying parameters? The model is always an approximation.

---

## 9. Where This Shows Up In Your Phase 1 Work

| Phase 1 location | What's happening |
|-----------------|-----------------|
| `np.quantile(returns, 0.05)` | Reading from the empirical distribution. No model. |
| `mu - 1.645 * sigma` | Using a normal theoretical distribution. Forces $\gamma_1=0$, $\gamma_2=3$. |
| Vol scaling (Notebook 08) | Standardising by $\hat{\sigma}$. Assumes the empirical distribution's shape is stable when you divide by volatility. Implicitly assumes higher standardised moments are constant. |
| The combined method (Notebook 09) | Mixes two estimates of the same parameter ($\hat{\sigma}_{\text{equal}}$ and $\hat{\sigma}_{\text{decay}}$). Neither is the true $\sigma$ — both are estimates with different bias-variance properties. |
| QQ plots vs normal (you've seen these) | Directly compares the empirical quantiles to the theoretical quantiles of $N(0,1)$. The deviation from the diagonal line *is* the higher moments. |

---

## 10. Questions to Test Your Understanding

1. **You have 252 returns and fit a normal distribution. The fitted normal has the same mean and variance as your data by construction. Does it have the same VaR at 95%? Why or why not?**

2. **What happens to the empirical distribution when you get a new day of data? What happens to the theoretical distribution $N(\hat{\mu}, \hat{\sigma}^2)$?**

3. **If the true return distribution has $\gamma_1 = -0.5$ and $\gamma_2 = 5$, and you use parametric VaR, are you overstating or understating risk?** Draw it mentally: the left tail of the true distribution is fatter than normal. The 5th percentile is further left. Parametric VaR, which assumes normal, will be less negative — it understates risk.

4. **Why can't you just use the empirical distribution for everything? What's the downside?**

5. **A colleague says: "I computed VaR using a normal distribution because the Central Limit Theorem says everything becomes normal with enough data." What's wrong with this?** (The CLT is about the distribution of the *sample mean*, not the distribution of the *individual observations*. Returns don't become normal with more data — you just get more precise estimates of their non-normal shape.)

---

## What's Next

The natural next steps, depending on where your curiosity pulls:

- **The normal distribution deep dive** — why it's the starting point, what makes it special (its moments uniquely and completely define it), and why finance keeps rejecting it
- **Estimators and their properties** — bias, variance, consistency, Bessel's correction ($n-1$), why these concepts determine how much you trust your sample moments
- **A practical exercise** — take your SPY data, compute all four sample moments, compare to the normal, and quantify the gap. Make it a notebook.
