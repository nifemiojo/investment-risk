# The Empirical Distribution Is Discrete — What That Means and Why It Matters

**Date:** 2026-07-26
**Topic:** Why the empirical distribution is always discrete even when the underlying process is continuous, and the practical consequences for quantile estimation, VaR, and risk measurement.

---

## Opening Question

> You download 252 SPY daily returns from yfinance. SPY prices can move in increments of $0.01 — effectively continuous at the return level. The true process can produce any real number. But your empirical distribution says: "There are exactly 252 possible outcomes, each with probability 1/252." That's a discrete distribution trying to represent a continuous reality. What breaks? What still works?

---

## 1. The Discreteness — Why It Happens

### The construction forces it

The empirical CDF is built from indicator functions:

$$\hat{F}_n(x) = \frac{1}{n}\sum_{i=1}^n \mathbf{1}\{x_i \leq x\}$$

Each indicator is either 0 or 1. The sum is an integer count (0, 1, 2, ..., n). Dividing by n gives fractions: 0/n, 1/n, 2/n, ..., n/n. The function can only take $n+1$ possible values.

Between data points, the function is flat — it holds its value until it hits the next observation, then jumps by exactly $1/n$ (or $k/n$ for $k$ tied values).

**A concrete picture with 5 observations:**

Sorted returns: −1.5%, −0.5%, +0.2%, +0.8%, +2.0%

The ECDF:

```
1.0 ┤                                    ┌─────
    │                                    │
0.8 ┤                              ┌─────┘
    │                              │
0.6 ┤                        ┌─────┘
    │                        │
0.4 ┤                  ┌─────┘
    │                  │
0.2 ┤            ┌─────┘
    │            │
0.0 ┤──────┐─────┘
    │      │
    └──────┴──────┴──────┴──────┴──────┴──────
       −1.5%   −0.5%   +0.2%   +0.8%   +2.0%
```

Every horizontal segment says: "No observations fell in this range, so the cumulative probability doesn't change." Every vertical jump says: "Here's an observation — the cumulative count increments."

This staircase is the ECDF. It is fundamentally discrete. The flat segments contain zero probability mass. All the mass is at the jump points.

### The probability mass function — all atoms, no density

The empirical probability mass function (EPMF) is:

$$P(X = x) = \begin{cases} \frac{k}{n} & \text{if } x \text{ appears } k \text{ times in the sample} \\ 0 & \text{otherwise} \end{cases}$$

For 252 unique returns: $P(X = x_i) = 1/252$ for each observed $x_i$, and $P(X = x) = 0$ for every other real number.

**This means the empirical distribution assigns zero probability to 99.999...% of the real number line.** Everything between −1.50% and −1.49%? Zero probability. Even though the true process can certainly produce returns in that interval.

---

## 2. The Tension — Continuous Process, Discrete Summary

### What you have vs what you're trying to describe

| | True process (SPY returns) | Empirical distribution |
|---|---|---|
| **Nature** | Continuous | Discrete |
| **Possible values** | Uncountably infinite (any real number) | Exactly $n$ values (your observed returns) |
| **Probability of a specific value** | Zero (for any exact return) | $1/n$ (for each observed return) |
| **Probability of an interval** | Positive, smooth | Positive, but lumpy (depends on which observations fall in the interval) |
| **PDF exists?** | Yes — a smooth density curve | No — it's a set of probability atoms. To get a density you need kernel smoothing. |

The empirical distribution is a **step-function approximation** of a smooth curve. It's like representing a circle with a polygon — the more sides you add, the closer it gets, but it's never truly smooth.

### With 5 observations — the staircase is obvious

Every step is $1/5 = 0.20$. You can only estimate quantiles at 0.20, 0.40, 0.60, 0.80. Your "resolution" is 20 percentage points. This is terrible for VaR.

### With 252 observations — the staircase is still there, just finer

Each step is $1/252 \approx 0.004 = 0.4\%$. Your resolution is 0.4 percentage points. You can estimate quantiles at 0.4%, 0.8%, 1.2%, ... — much better, but still not continuous.

The 5th percentile: $252 \times 0.05 = 12.6$. You're between the 12th and 13th worst days. The ECDF says $\hat{F}(x_{12}) = 12/252 = 0.0476$ and $\hat{F}(x_{13}) = 13/252 = 0.0516$. Neither equals exactly 0.05.

**The ECDF can't give you an exact 5th percentile.** It always gives you a percentile that's a multiple of $1/n$. Everything between those steps requires interpolation.

---

## 3. Interpolation — Bridging the Gaps in the Staircase

Since the ECDF is a step function, reading a quantile at an arbitrary probability $p$ requires a rule for what to do when $n \times p$ is not an integer. Different rules give different answers.

### The five main methods

Let's work with: sorted returns $x_{(1)} \leq x_{(2)} \leq \ldots \leq x_{(n)}$, and we want the $p$-th quantile.

| Method | What it does | `np.percentile` name | VaR implication |
|--------|-------------|---------------------|-----------------|
| **Lower (inverse of ECDF)** | $x_{(\lceil np \rceil)}$ — take the next observation | `'lower'` | Most conservative. Always rounds up. |
| **Higher** | $x_{(\lfloor np \rfloor + 1)}$ | `'higher'` | Least conservative. Rounds down (in rank terms). |
| **Linear interpolation** | Weighted average of $x_{(\lfloor h \rfloor)}$ and $x_{(\lfloor h \rfloor+1)}$ | `'linear'` (default) | Smooth. The value may not be any actual return. |
| **Midpoint** | $(x_{(\lfloor h \rfloor)} + x_{(\lceil h \rceil)}) / 2$ | `'midpoint'` | Simple average of neighbours. |
| **Nearest** | Closest observation | `'nearest'` | Rounds to an actual observed return. |

Where $h = (n-1)p + 1$ in the default method, or $h = np$ in others. (Yes, different software uses different definitions of $h$ — this alone causes confusion.)

### Worked example — 5th percentile from 252 returns

Suppose the 12th and 13th worst returns are:

- $x_{(12)} = -2.12\%$
- $x_{(13)} = -2.08\%$

The 5th percentile ($p = 0.05$) from $n = 252$:

| Method | Result | Interpretation |
|--------|--------|---------------|
| `'lower'` | −2.12% | "At least 5% of returns are ≤ −2.12%" |
| `'higher'` | −2.08% | "At most 5% of returns are < −2.08%" |
| `'linear'` | ≈−2.10% (0.6×−2.12 + 0.4×−2.08) | "Interpolated between the two bracketing observations" |
| `'midpoint'` | −2.10% | "Simple average of the two neighbours" |
| `'nearest'` | −2.12% | "The nearest actual observation" |

**Your VaR number changes by 4 basis points depending on which interpolation method you choose.** That's not huge, but it's real. The discreteness of the ECDF means there's no single "correct" answer — only conventions.

### With small $n$, the differences are dramatic

Same question with $n = 10$, $p = 0.05$:

- $10 \times 0.05 = 0.5$
- $\lceil 0.5 \rceil = 1$ → `'lower'` gives $x_{(1)}$ (the worst day)
- `'linear'` interpolates between $x_{(0)}$ (which doesn't exist — extrapolation needed)

With 10 observations, the 5th percentile is deeply ambiguous. Every method gives a different answer, and some methods break entirely. This is why historical VaR with fewer than ~100 observations is unreliable — not because the method is wrong, but because the ECDF's discreteness makes quantile estimation unstable.

---

## 4. What the Discreteness Means for VaR in Practice

### The good — the discreteness is the feature

Historical VaR reads a quantile from the ECDF. The ECDF is discrete. That's fine — the discreteness is *why* the method works. You're not claiming the true distribution is discrete. You're saying: "Based on the 252 days I observed, here's the return at the relevant rank." You're computing a summary statistic from a finite sample, and summary statistics from finite samples are always discrete.

The discreteness is honest. It doesn't pretend to know what happens between observations.

### The bad — the discreteness limits resolution

At 95% confidence with 252 days: you're reading the ~13th worst day. You have 12 observations in the tail. That's enough for a reasonable estimate.

At 99% confidence with 252 days: you're reading the ~3rd worst day. You have 2 observations in the tail. The ECDF says the VaR is $x_{(3)}$, but the step function only has two steps between $x_{(1)}$ and $x_{(3)}$. Your estimate of the 1st percentile is based on the 3rd-worst day — it's not the 1st percentile, it's the $3/252 \approx 1.2$th percentile. Close enough for government work, perhaps, but you should know what you're actually reading.

At 99.9% confidence with 252 days: you're trying to read the ~0th worst day. The ECDF literally can't do this — $0.001 \times 252 = 0.25$, which rounds to 0. You have no observations at or beyond that quantile. The empirical distribution fails.

### The rule of thumb

If $n \times (1 - \text{confidence}) < 5$, you don't have enough observations in the tail for a reliable historical VaR estimate. The ECDF's discreteness makes the estimate too noisy. For $n = 252$:
- 95% VaR: $252 \times 0.05 = 12.6$ ✓ (fine)
- 99% VaR: $252 \times 0.01 = 2.5$ ✗ (too few tail observations)
- 99.9% VaR: $252 \times 0.001 = 0.25$ ✗ (effectively impossible)

---

## 5. Beyond Equal Weights — Weighted and Smoothed Empirical Distributions

The standard empirical distribution gives every observation equal mass $1/n$. But you can modify this.

### Weighted empirical distribution (decay-weighted VaR)

Assign weight $w_i$ to observation $i$, with $\sum w_i = 1$. The weighted ECDF:

$$\hat{F}_n^w(x) = \sum_{i=1}^n w_i \cdot \mathbf{1}\{x_i \leq x\}$$

For decay weighting with parameter $\lambda$, recent observations get larger $w_i$:

$$w_i \propto \lambda^{n-i} \quad \text{(for observations ordered oldest to newest)}$$

The staircase still exists, but the step heights are unequal. Recent observations create bigger steps.

**What this changes:** the quantile is pulled toward recent observations. If recent returns have been more negative, the decay-weighted VaR is more conservative. But it's still a discrete step function — just with uneven steps.

### Kernel density estimation — creating a continuous density from discrete atoms

Kernel density estimation (KDE) replaces each probability atom with a smooth bump (a kernel) and sums them:

$$\hat{f}_h(x) = \frac{1}{nh}\sum_{i=1}^n K\left(\frac{x - x_i}{h}\right)$$

Where $K$ is a smooth kernel function (usually Gaussian) and $h$ is the bandwidth (controls smoothness).

Each observation is no longer a discrete atom — it's a smooth bump centred at $x_i$ that spreads probability mass into the surrounding region. The result is a continuous density estimate.

**What this gives you:**
- A smooth PDF estimate (no staircase)
- Probability mass between observations (no gaps)
- Ability to compute any quantile, at any confidence level
- Tails that extend beyond the observed extremes (because Gaussian kernels have infinite support)

**What this costs you:**
- A bandwidth choice ($h$). Too small → wiggly, overfit. Too large → oversmoothed, destroys features.
- The tails are shaped by the kernel, not the data. If you use Gaussian kernels, the estimated tails are Gaussian even if the data has fat tails. This is dangerous for VaR.
- KDE is unreliable in the tails regardless — there's little data there, so the estimate is driven by the kernel choice and bandwidth, not by the observations.

> **KDE is useful for visualisation and for estimating the body of the distribution. For tail quantiles (exactly what VaR needs), it's usually worse than the raw ECDF because it imposes smoothness where the data is sparse — and the tail is the sparsest region.**

---

## 6. The Empirical PDF? It Doesn't Exist (Without Help)

A genuine PDF (probability density function) requires continuity — probability is spread smoothly over intervals, and the probability of any exact value is zero. The empirical distribution is a set of probability atoms — the probability of each observed value is $1/n$, and the PDF would be infinite at those points.

So the empirical distribution has:
- ✅ A well-defined PMF (probability mass function) — the list of values and their frequencies
- ✅ A well-defined CDF (cumulative distribution function) — the step function $\hat{F}_n$
- ❌ No well-defined PDF — unless you smooth it (KDE, histogram)

When you see a histogram of returns with a smooth density curve overlaid, that smooth curve is either:
1. A KDE estimate (smoothed from the discrete empirical distribution), or
2. A fitted parametric distribution (e.g., normal curve)

Neither is the empirical distribution itself. Both are transformations from discrete to continuous.

---

## 7. What This Means for Your Workflow

| Situation | Implication |
|-----------|------------|
| Computing VaR at 95% from 252 days | Fine. $252 \times 0.05 = 12.6$ tail observations. The discreteness is manageable. |
| Computing VaR at 99% from 252 days | Unreliable. Only 2–3 tail observations. The discreteness dominates. Use parametric or Monte Carlo with a reasonable distribution assumption. |
| Comparing VaR across two windows (60d vs 252d) | Be aware: the 60d window has $60 \times 0.05 = 3$ tail observations. The discreteness noise is much higher. The comparison is noisy by construction. |
| Plotting the distribution of returns | A histogram or KDE is fine for visualisation, but remember it's a smoothed approximation. The raw empirical distribution is the 252 observations themselves. |
| Bootstrapping VaR | The bootstrap naturally handles discreteness — it samples from the discrete ECDF, and the resulting bootstrap distribution smooths out the discreteness through averaging. |
| Communicating VaR to stakeholders | Don't say "VaR is −2.10%." Say "VaR is approximately −2.1%, based on the 13th-worst day among 252, interpolated." The discreteness should be acknowledged, not hidden. |

---

## 8. The Deep Point — Discreteness Is Not a Bug

It's tempting to think of the ECDF's discreteness as a flaw — an artefact of finite sampling that we need to smooth away. But the discreteness is actually informative.

**The ECDF doesn't pretend to know what it doesn't know.** The flat segments between observations say: "I have no data here. I'm not going to guess." The vertical jumps say: "Here's exactly where the data is." This honesty is the empirical distribution's greatest strength.

A smoothed estimate (KDE, fitted normal, fitted t) *does* pretend to know — it fills in the gaps with assumptions. Sometimes those assumptions are reasonable. Sometimes they're dangerous. The art of risk measurement is knowing when the gaps are small enough that smoothing helps, and when the gaps are in the tail — exactly where smoothing is most unreliable.

> **For the body of the distribution: smooth away. For the tail: the discreteness of the ECDF, with all its noise and limitations, is usually more honest than a smooth curve built on assumptions.**

---

## 9. Check-in Questions

1. **You have 50 daily returns and need VaR at 95%. $50 \times 0.05 = 2.5$ tail observations. Is this reliable? What problems do you expect?**

2. **`np.quantile(returns, 0.05)` and `np.percentile(returns, 5)` give the same answer. But they use linear interpolation by default. What does this mean for a VaR number — does −2.10% (interpolated) correspond to any actual day's return?**

3. **If you use decay weighting, the step sizes in the ECDF become unequal. Does this make the distribution more or less "discrete"? Does it change anything fundamental about the ECDF?**

4. **Why is KDE dangerous for estimating VaR at 99%?** (Hint: where does KDE have the least data to work with? What determines the shape of the KDE in sparse regions?)

5. **A colleague says: "The empirical distribution is discrete and ugly. Let's fit a smooth distribution instead — it looks more like what the true process must be." What's the counterargument?**

---

## What's Next

This sets up several natural next steps:

- **Quantiles deep dive** — the inverse CDF, all 9 interpolation methods in `np.percentile`, why they exist, and which one you should use for VaR
- **Kernel density estimation deep dive** — bandwidth selection, kernel choice, boundary bias, and why it's simultaneously useful and dangerous for risk
- **The PDF/CDF/PPF triad** — the three ways to characterise a distribution, which one dominates in risk management (the inverse CDF / PPF), and why
- **A practical exercise** — take your SPY data, compute VaR with all 5 interpolation methods, compare the answers, and bootstrap to see how much of the variation is sampling noise vs method choice
