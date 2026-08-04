# Histograms and Visualising the Empirical Distribution

**Date:** 2026-07-26
**Topic:** How to visualise a return distribution honestly — histograms, ECDFs, density plots, rug plots, box plots, and QQ plots. What each one shows, what each one hides, and which to use when.

---

## Opening Question

> You plot your SPY returns as a histogram. It looks roughly bell-shaped with a fat left tail. You tweak the bin width from 20 bins to 50 bins — and suddenly the shape looks different. More bumps. A different impression of "how normal" the data is. Which one is right? Neither. Or rather: the histogram is never the distribution. It's a visualisation choice. Every visualisation of the empirical distribution makes choices — and every choice hides something.

---

## 1. What a Histogram Actually Is

A histogram takes your $n$ observations, divides the range into $k$ bins (intervals), and counts how many observations fall into each bin.

### The two flavours — frequency vs density

**Frequency histogram:** the bar height = count of observations in that bin.

| Bin | Count |
|-----|-------|
| [−2.5%, −2.0%) | 12 |
| [−2.0%, −1.5%) | 18 |
| [−1.5%, −1.0%) | 31 |
| ... | ... |

**Density histogram:** the bar *area* = proportion of observations in that bin, so the bar *height* = proportion / bin width. The total area of all bars = 1.

$$\text{bar height} = \frac{\text{count in bin}}{n \times \text{bin width}}$$

For the same data, if bin width is 0.5%, the first bar has height = 12 / (252 × 0.005) = 9.52.

> **Density histograms integrate to 1. Frequency histograms sum to n. For comparing distributions with different sample sizes, always use density — otherwise the larger sample looks "more probable" everywhere purely from having more observations.**

### The histogram formula

For bin $j$ with boundaries $[b_j, b_{j+1})$ and width $h = b_{j+1} - b_j$:

$$\hat{f}_j = \frac{1}{nh} \sum_{i=1}^n \mathbf{1}\{b_j \leq x_i < b_{j+1}\}$$

This is a **histogram density estimator** — the simplest nonparametric density estimator. It's piecewise constant (like the ECDF is piecewise constant — the histogram inherits the discreteness).

---

## 2. The Bin Width Problem — Same Data, Different Stories

Let's see this concretely. Here are 252 fictional SPY returns drawn from a distribution with negative skew and fat tails. I'll describe what you'd see with different bin counts.

### 10 bins — oversmoothed

```
Frequency
 60 ┤              ┌───┐
    │              │   │
 40 ┤      ┌───┐   │   │   ┌───┐
    │      │   │   │   │   │   │
 20 ┤  ┌───┐   │   │   │   │   │   ┌───┐
    │  │   │   │   │   │   │   │   │   │
  0 ┤──┴───┴───┴───┴───┴───┴───┴───┴───┴──
      -4   -3  -2  -1   0   +1  +2  +3  +4
```

Smooth. Clean. Looks roughly bell-shaped. The left tail seems only slightly fatter than the right. You'd say: "Pretty close to normal." **This is the oversmoothed view — bins so wide that the fat left tail gets averaged into a single bar.**

### 50 bins — moderate resolution

```
Frequency
 30 ┤          ┌──┐
    │          │  │      ┌──┐
 20 ┤     ┌──┐ │  │  ┌──┐│  │
    │  ┌──┐│  │ │  │  │  ││  │  ┌──┐
 10 ┤  │  ││  │ │  │  │  ││  │  │  │  ┌─┐
    │  │  ││  │ │  │  │  ││  │  │  │  │ │
  0 ┤──┴──┴┴──┴┴──┴┴──┴──┴┴──┴──┴──┴──┴─┴─
      -4   -3   -2   -1   0   +1  +2  +3  +4
```

The left tail extends further. There's a noticeable bump around −3.5% that was invisible before. The right tail looks thinner. You'd say: "There's some negative skew — the left tail is fatter."

### 200 bins — undersmoothed (too few obs per bin)

```
Frequency
 10 ┤┌┐  ┌┐  ┌┐    ┌┐┌┐  ┌┐    ┌┐
    │││  ││  ││┌┐┌┐││││┌┐││┌┐┌┐││
  5 ┤││┌┐││┌┐││││││││││││││││││││││┌┐
    │││││││││││││││││││││││││││││││││││
  0 ┤┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴
      -4   -3   -2   -1   0   +1  +2  +3  +4
```

Noisy. Irregular. Many bins are empty. You can't really see the shape at all. You'd say: "I don't know what this is." **This is the undersmoothed view — bins so narrow that sampling noise dominates the shape.**

### The lesson

**All three histograms are correct.** They all represent the same data. The difference is purely the bin width — a visualisation choice, not a data property. There is no "right" bin width. There is only: what question are you trying to answer?

| Bin count | Good for | Bad for |
|-----------|----------|---------|
| 10–20 | Seeing the overall shape, comparing to a theoretical distribution | Detecting skewness, kurtosis, or multimodality |
| 30–60 | General-purpose. Balance of shape and detail. | Extremely fine features |
| 100+ | Detecting multimodality, gaps, or data artefacts | Seeing the overall shape — noise dominates |
| $> n/5$ | Nothing. You're counting individual observations. | Everything. |

### Rules of thumb for bin width

| Rule | Formula | Best for |
|------|---------|----------|
| **Sturges** | $k = \lceil \log_2 n + 1 \rceil$ | Small $n$ (works poorly for $n > 200$) |
| **Scott** | $h = 3.5 \cdot s / n^{1/3}$ | Normal-ish data |
| **Freedman-Diaconis** | $h = 2 \cdot \text{IQR} / n^{1/3}$ | Robust to outliers (uses IQR not std) |
| **Square root** | $k = \lceil \sqrt{n} \rceil$ | Simple, reasonable for moderate $n$ |

For $n = 252$:
- Sturges: $k = \lceil \log_2 252 + 1 \rceil = \lceil 8.98 \rceil = 9$ bins (too few)
- Scott: depends on $s$, typically 15–25 bins
- Freedman-Diaconis: typically 20–35 bins
- Square root: $k = \lceil \sqrt{252} \rceil = 16$ bins

None is "correct." Scott and Freedman-Diaconis are the most commonly recommended. But for financial returns, you should also just *look* at several bin counts and see what's stable across them.

---

## 3. The Starting Point Problem — Bin Boundaries Matter Too

Bin width isn't the only choice. **Where the first bin starts** also changes what you see.

Imagine returns from −2.0% to +2.0% with 4 bins of width 1%:

### Start at −2.0%:
```
Bin 1: [−2.0%, −1.0%)
Bin 2: [−1.0%,  0.0%)
Bin 3: [ 0.0%, +1.0%)
Bin 4: [ +1.0%, +2.0%)
```

### Start at −2.5%:
```
Bin 1: [−2.5%, −1.5%)
Bin 2: [−1.5%, −0.5%)
Bin 3: [−0.5%, +0.5%)
Bin 4: [ +0.5%, +1.5%)
Bin 5: [ +1.5%, +2.5%)
```

Same data, same bin width, different starting point → different bin boundaries → different counts per bin → different visual impression. This is the **binning artefact** — a feature of the histogram that has nothing to do with the data.

**Mitigation:** Use enough bins that the starting point doesn't materially change the picture. Or use a visualisation that doesn't bin at all (ECDF, KDE with a reasonable bandwidth).

---

## 4. Histogram vs ECDF — What Each Shows and Hides

These are the two fundamental visualisations of the empirical distribution. They show different things.

### The histogram

```
Shows: approximate density — where the data clusters
Hides: quantiles, tail probabilities, exact cumulative proportions
Best for: seeing the overall shape, comparing to a theoretical density
```

### The ECDF (empirical CDF)

```
Shows: cumulative proportions — exactly what proportion is ≤ any value
Hides: density, clustering, multimodality
Best for: reading quantiles, comparing distributions, seeing tail behaviour
```

### Side-by-side with the same data

**Histogram (density):**
```
Density
0.4 ┤          ┌───┐
    │          │   │
0.3 ┤    ┌───┐ │   │  ┌───┐
    │    │   │ │   │  │   │
0.2 ┤  ┌─┤   │ │   │  │   │
    │  │ │   │ │   │  │   │
0.1 ┤  │ │   │ │   │  │   │  ┌─┐
    │  │ │   │ │   │  │   │  │ │
0.0 ┤──┴─┴───┴─┴───┴──┴───┴──┴─┴──
      -3   -2   -1   0  +1  +2  +3
```
The mode (peak) is visible. The asymmetry is visible (left tail extends further). But you can't read the 5th percentile precisely.

**ECDF:**
```
1.0 ┤                              ┌────────
    │                          ┌───┘
0.8 ┤                      ┌───┘
    │                  ┌───┘
0.6 ┤              ┌───┘
    │          ┌───┘
0.4 ┤      ┌───┘
    │  ┌───┘
0.2 ┤──┘
    │
0.0 ┤────────────────────────────────
      -3   -2   -1   0  +1  +2  +3
```
The 5th percentile is immediately readable: draw a horizontal line at 0.05, find where it hits the curve. The fat left tail shows as a longer stretch of the curve between 0.0 and 0.1. But the mode (peak density) is invisible — the steepest part of the curve tells you where the median is, not the mode.

### The key insight: they're complements, not substitutes

| Question | Best visualisation |
|----------|-------------------|
| "What's the most common daily return?" | Histogram |
| "What's the 5th percentile?" | ECDF |
| "Are there two distinct regimes?" | Histogram (bimodality is obvious) |
| "Is the left tail fatter than normal?" | ECDF or QQ plot |
| "What proportion of days had losses > 2%?" | ECDF (read it directly) |
| "What does the distribution look like, generally?" | Histogram |

For VaR work, the ECDF is more directly useful — VaR is a quantile, and the ECDF is the quantile function's graph. The histogram shows shape but not quantiles. **Show both.**

---

## 5. Beyond Histograms — the Full Visualisation Toolkit

### Rug plot — the raw data, unadorned

A rug plot draws a tick mark for every observation on a number line. No binning. No smoothing. Just the data.

```
    ││  │││ │  ││││││  │ ││││  │ │││ │││ │ │
  ──┴┴──┴┴┴─┴──┴┴┴┴┴┴──┴─┴┴┴┴──┴─┴┴┴─┴┴┴─┴─┴──
    -3   -2   -1    0    +1   +2   +3
```

**What it shows:** where observations actually are. Gaps are genuine — no observations fell there. Clusters are genuine — many observations fell in a narrow range.

**What it hides:** the overall shape is hard to read. Too much ink for large $n$.

**Best for:** small $n$ (< 100), or as an addition to a histogram or KDE plot (rug underneath, smooth curve above).

### Kernel density plot — a smoothed density estimate

A KDE plot replaces each observation with a small Gaussian bump and sums them. The bandwidth controls smoothness.

```
Density
0.4 ┤            _───_ 
    │          _/     \_
0.3 ┤        _/         \_
    │      _/             \_
0.2 ┤   _/                  \_
    │ _/                      \___
0.1 ┤/                            \____
    │
0.0 ┤────────────────────────────────────
      -3   -2   -1   0   +1   +2   +3
```

**What it shows:** a smooth approximation of the density. Much cleaner than a histogram. No binning artefacts.

**What it hides:** the discreteness of the data (you can't tell if a bump is real or a kernel artefact). The tails are shaped by the kernel, not the data — a Gaussian KDE will always have Gaussian-looking tails, even if the data has fat tails.

**Best for:** visualisation, comparing distribution shapes, presentations. **Not for** estimating tail quantiles or reading exact probabilities.

### Box plot — five-number summary

```
         whisker    box        whisker
    ───────|──────[|══════|]──────|──────
          min     Q1  med  Q3     max
                         
         or with outliers:
         
    ───────|──────[|══════|]──────|── ○  ○
          min     Q1  med  Q3     |  outliers
                               upper fence
```

**What it shows:** minimum, Q1 (25th percentile), median, Q3 (75th percentile), maximum. Outliers beyond 1.5 × IQR shown as points.

**What it hides:** everything about the shape between these five numbers. Bimodality is invisible. The density of the middle 50% is invisible.

**Best for:** comparing many distributions side by side (e.g., returns by year, or by asset). Compact. Good for detecting skew (median offset from centre of box) and outliers.

### Violin plot — box plot + density

A violin plot shows the full density shape, mirrored, with a miniature box plot inside.

```
      _───_
    _/     \_
   /         \        ← density (width = frequency)
  /           \
 │   ═══[|]═══   │     ← miniature box plot inside
  \           /
   \         /
    \_     _/
      ─────
```

**What it shows:** the full shape of the distribution, plus key quantiles. Combines the best of histograms and box plots.

**What it hides:** nothing major — it's quite honest. The smoothing is by KDE, so tail behaviour is still kernel-dependent.

**Best for:** comparing multiple distributions with full shape information. More informative than box plots, more compact than multiple histograms.

---

## 6. The QQ Plot — the Most Important Plot for VaR Work

A **Q-Q plot** (quantile-quantile plot) compares the empirical quantiles of your data to the theoretical quantiles of a reference distribution (usually normal).

### How it works

1. Sort your $n$ returns
2. For each sorted return $x_{(i)}$, compute its empirical quantile: $(i - 0.5)/n$
3. Find the theoretical quantile of the reference distribution at the same probability
4. Plot: theoretical quantile on x-axis, empirical quantile on y-axis

If the data matches the reference distribution, the points fall on the $y = x$ diagonal line.

### What a QQ plot reveals

**Normal data (points on the diagonal):**
```
Empirical
  +3 ┤                          ●
     │                       ●
   0 ┤                   ●
     │               ●
  -3 ┤ ●
     └──┴──────┴──────┴──────┴──
       -3      0     +2     +3
            Theoretical (Normal)
```

**Fat-tailed data (S-shape):**
```
Empirical
  +3 ┤                        ●●
     │                     ●
   0 ┤                ●
     │            ●
  -3 ┤ ●●
     └──┴──────┴──────┴──────┴──
       -3      0     +2     +3
            Theoretical (Normal)
```
The points curve away from the diagonal in both tails → fatter tails than normal. **This is exactly what SPY returns look like.**

**Negatively skewed data (J-shape in left tail):**
```
Empirical
  +3 ┤                      ●
     │                    ●
   0 ┤                ●
     │             ●
  -3 ┤ ●●
     │●●
     └──┴──────┴──────┴──────┴──
       -3      0     +2     +3
            Theoretical (Normal)
```
The left tail points fall below the diagonal (empirical is more negative than normal predicts), while the right tail is closer to normal. **Also typical for equity returns.**

### Why the QQ plot is essential for VaR

Parametric VaR assumes normality. The QQ plot shows you exactly *where* and *how* that assumption breaks.

- **Left tail below the diagonal:** negative skew and/or fat left tail → parametric VaR understates risk
- **S-shape in both tails:** excess kurtosis → parametric VaR understates risk at extreme confidence levels
- **Points on the diagonal:** normality holds → parametric and historical VaR should roughly agree

The QQ plot is the single most honest visualisation of whether parametric VaR is appropriate for your data.

---

## 7. A Practical Visualisation Workflow for VaR

When you're exploring a new return series and need to understand the distribution for VaR, here's the sequence:

### Step 1: Histogram + rug + normal overlay

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

returns = ...  # your 252 daily returns

fig, ax = plt.subplots(figsize=(10, 5))

# Histogram (density)
ax.hist(returns, bins=40, density=True, alpha=0.6, label='Empirical')

# Rug plot
ax.plot(returns, np.zeros_like(returns), '|', color='black', alpha=0.3)

# Fitted normal curve
x = np.linspace(returns.min(), returns.max(), 200)
mu, sigma = returns.mean(), returns.std()
ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', lw=2, label='Normal fit')

ax.set_xlabel('Daily Return')
ax.set_ylabel('Density')
ax.legend()
```

**What this tells you:** overall shape, deviation from normality, where the data clusters, the raw observations (rug).

### Step 2: ECDF

```python
fig, ax = plt.subplots(figsize=(10, 5))

# ECDF
sorted_returns = np.sort(returns)
cumulative = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)
ax.step(sorted_returns, cumulative, where='post', lw=2, label='Empirical CDF')

# Fitted normal CDF
x = np.linspace(returns.min(), returns.max(), 200)
ax.plot(x, stats.norm.cdf(x, mu, sigma), 'r-', lw=2, label='Normal CDF')

# VaR line
var_95 = np.quantile(returns, 0.05)
ax.axvline(var_95, color='red', linestyle='--', alpha=0.7, label=f'VaR 95% = {var_95:.2%}')
ax.axhline(0.05, color='red', linestyle=':', alpha=0.5)

ax.set_xlabel('Daily Return')
ax.set_ylabel('Cumulative Probability')
ax.legend()
```

**What this tells you:** exact quantiles, tail probabilities, where the ECDF deviates from the normal CDF (visible as gaps between the step function and the smooth curve).

### Step 3: QQ plot vs normal

```python
fig, ax = plt.subplots(figsize=(6, 6))
stats.probplot(returns, dist='norm', plot=ax)
ax.set_title('Q-Q Plot: Returns vs Normal')
```

**What this tells you:** where exactly the empirical distribution deviates from normality, especially in the tails. This is the honesty check for parametric VaR.

### Step 4: Box plot by period (optional)

```python
import pandas as pd

# If you have dates
returns_df = pd.DataFrame({'date': dates, 'return': returns})
returns_df['year'] = returns_df['date'].dt.year

fig, ax = plt.subplots(figsize=(12, 5))
returns_df.boxplot(column='return', by='year', ax=ax)
ax.set_xlabel('Year')
ax.set_ylabel('Daily Return')
ax.set_title('Return Distribution by Year')
plt.suptitle('')
```

**What this tells you:** how the distribution changes over time. Did 2020 have fatter tails? Did 2022 have more negative skew? This connects distribution shape to market regimes.

---

## 8. What Visualisations Hide — a Candid List

Every visualisation lies a little. Here's what each one hides:

| Visualisation | What it hides |
|--------------|--------------|
| **Histogram** | Quantiles, exact values, sensitivity to bin choice, starting point dependence |
| **ECDF** | Density, clustering, modes. Hard to see where data concentrates — steep = many observations, flat = few, but this is not visually obvious. |
| **KDE** | Discreteness, tail behaviour (kernel dominates where data is sparse), bandwidth sensitivity |
| **Box plot** | Everything about shape. Multimodality. The distribution could be a camel and the box plot would show a symmetric box. |
| **Violin plot** | Similar to KDE — tails are kernel-driven, bandwidth matters |
| **QQ plot** | Density information. You can't tell where the mode is or whether there are multiple modes. |
| **Rug plot** | Shape. Too much visual noise for large $n$. |

### The fundamental trade-off

Every visualisation reduces $n$ numbers to a picture. Information is lost. The question is: does the visualisation lose the information you *need* for the decision you're making?

If you're deciding whether to use parametric or historical VaR, the QQ plot tells you exactly what you need — and a histogram doesn't. If you're presenting to a risk committee, the violin plot is informative but the box plot may be clearer. Match the visualisation to the question.

---

## 9. Common Mistakes in Visualising Return Distributions

### Mistake 1: Using frequency instead of density when overlaying a fitted distribution

```python
# WRONG
ax.hist(returns, bins=40)  # frequency — bar heights sum to n
ax.plot(x, stats.norm.pdf(x, mu, sigma))  # density — integrates to 1
# The normal curve will look tiny — it's on a completely different scale.
```

```python
# RIGHT
ax.hist(returns, bins=40, density=True)  # density — bar areas sum to 1
ax.plot(x, stats.norm.pdf(x, mu, sigma))
# Now they're on the same scale. Comparison is valid.
```

### Mistake 2: Using too few bins and concluding the data is normal

10 bins can hide fat tails. Always try multiple bin counts. If the conclusion depends on the bin count, it's not a conclusion — it's an artefact.

### Mistake 3: Using KDE for tail assessment

The KDE's tail behaviour is determined by the kernel (Gaussian by default) and the bandwidth, not by the data. A Gaussian KDE will always show Gaussian-looking tails. If you're assessing tail fatness, use the ECDF or QQ plot instead.

### Mistake 4: Not showing the ECDF alongside the histogram

The histogram shows shape but hides quantiles. The ECDF shows quantiles but hides shape. For VaR work, you need both. Show them as a pair.

### Mistake 5: Fitting a normal distribution to the histogram and calling it "the distribution"

The normal curve overlaid on a histogram is a *hypothesis*, not a *fact*. Label it "Normal fit (for comparison)" not "The distribution." The data's distribution is the histogram (or ECDF) itself — the normal curve is a model you're testing.

---

## 10. Check-in Questions

1. **You plot a histogram with 10 bins and it looks normal. You plot with 50 bins and see a fat left tail. Which one is "right"? What would you report to a risk manager?**

2. **A density histogram has bar heights that depend on bin width. If you double the bin width, what happens to the bar heights?** (The area of each bar must be the proportion in that bin. Double the width → halve the height to keep area constant.)

3. **The QQ plot shows points below the diagonal in the left tail. What does this mean for parametric VaR — is it overstating or understating risk?**

4. **You show a colleague a box plot of SPY returns by year. They ask: "Was 2020 bimodal or just wide?" Can the box plot answer this? What would you need instead?**

5. **You have 1,000 days of returns and want to assess tail behaviour for VaR at 95%. Rank these visualisations from most to least useful: histogram, ECDF, QQ plot, KDE, box plot.** Explain your ranking.

---

## What's Next

- **The PDF/CDF/PPF triad** — the three mathematical functions that describe a distribution, and why the inverse CDF (PPF) is the one that matters most for VaR
- **Quantiles deep dive** — interpolation methods, the inverse CDF, and why `np.quantile(returns, 0.05)` gives the number it does
- **A practical exercise** — take your SPY data and produce the full visualisation workflow. Compare across different lookback windows (60d, 252d, 504d)
