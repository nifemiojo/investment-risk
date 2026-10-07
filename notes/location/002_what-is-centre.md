# What Do We Mean by the Centre of a Distribution?

**Date:** 2026-07-28
**Topic:** The conceptual meaning of "centre" — multiple definitions, one word
**Turn:** 002

---

## User request

"What do we mean by the centre of a distribution?"

## Work and response

### 1. The Problem with "Centre"

"Centre" feels obvious. A circle has a centre. A room has a centre. Surely a distribution does too — just look at the histogram and point at the middle?

The problem: **"middle" isn't one thing.** It depends on what you're trying to balance, split, or maximise. The same distribution can have three different centres — and they're all correct under their own definition.

Take three questions about the same 252 daily SPY returns:

| Question | "Centre" means | Answer |
|----------|---------------|--------|
| "If I randomly pick a day, what return should I expect?" | The arithmetic mean of all outcomes | $\bar{x}$ |
| "What return splits history in half — 50% of days better, 50% worse?" | The value at the 50th percentile | Median |
| "What's the most common daily return?" | The peak of the histogram | Mode |

Same data. Three questions. Three different centres. So what *do* we mean?

---

### 2. Centre as Balance Point — The Mean

Imagine you plot every daily return as a weight on a number line. Each weight is exactly 1 unit of mass (every day counts equally).

```
   -2%    -1%     0%    +1%    +2%
    ●       ●      ●      ●      ●
    ↑
  If returns are symmetric, the
  balance point sits at zero
```

Now imagine placing a fulcrum under the line. Slide it left and right until the line balances perfectly — no tilt, no rotation. That point is the **mean**.

**Why it balances:** The mean is the point where the sum of distances to the left equals the sum of distances to the right:

$$\sum_{x_i < \bar{x}} (\bar{x} - x_i) = \sum_{x_i > \bar{x}} (x_i - \bar{x})$$

Every observation pulls with force proportional to its distance. An observation at −5% pulls five times harder than one at −1%. The mean is where those forces cancel.

**What this means conceptually:** The mean is the centre of **mass.** It answers: "If I had to replace every observation with a single number that preserves the total weight, what would it be?"

#### Example: The Seesaw

```
A child (30 kg) sits 2m to the right. You (60 kg) sit 1m to the left.

       ●               ●
    ← 1m →  ▲  ←—— 2m ——→
    [you]      [child]
    60 kg      30 kg
    
    60 × 1 = 60  |  30 × 2 = 60
    Moments balance → the seesaw is level
```

The balance point is at the fulcrum. The mean works the same way: observations further from the centre exert more "torque." That's why an outlier at +10% has disproportionate influence — it's sitting far from the centre, pulling hard.

---

### 3. Centre as Halfway Point — The Median

Now think differently. Instead of balancing mass, sort everything and find the exact middle.

```
Sorted SPY daily returns (n = 252):

  Rank 1:   -9.8%   ← worst day
  Rank 2:   -6.2%
  ...
  Rank 126: -0.03%  ← middle observation (half above, half below)
  Rank 127: +0.01%  ← for even n, median is the average of 126 and 127
  ...
  Rank 251: +4.5%
  Rank 252: +8.1%   ← best day

  Median ≈ (−0.03% + 0.01%) / 2 = −0.01%
```

The median is the centre of **count.** It answers: "What value splits the observations into two equal halves?"

**Critical difference from the mean:** The median doesn't care about the actual values — only their order. If the best day had been +80% instead of +8%, the mean would jump; the median wouldn't move at all. The median treats every observation as a vote for "above" or "below," not as a weight proportional to its distance.

| Change | Effect on mean | Effect on median |
|--------|---------------|-----------------|
| Best day goes from +8% to +80% | Increases by ~0.3% | **Zero** |
| Worst day goes from −10% to −5% | Increases by ~0.02% | **Zero** (unless it crosses the middle) |
| Moderate day crosses from below median to above | Negligible | Small shift |

The median is democratic — one observation, one vote. The mean is plutocratic — distant observations have more influence.

---

### 4. Centre as Most Typical — The Mode

Forget balancing and splitting. Just look at the histogram and ask: what value occurs most often?

```
Histogram of daily SPY returns (binned):

    Frequency
       ↑
    40 │        ██
    35 │       ████
    30 │      ██████
    25 │     ████████
    20 │    ███████████
    15 │   ██████████████
    10 │  ████████████████
     5 │ ██████████████████
     0 ├────────────────────→ Return
       -2%      0%     +2%

    Mode ≈ 0% (the tallest bin)
```

The mode is the centre of **density.** It answers: "If I had to bet on one specific value, what's my best guess?"

**Problem for financial returns:** With continuous data, every observation is unique (to many decimal places). The "mode" depends entirely on how you bin the data. Change the bin width from 0.1% to 0.5%, and the mode changes. For continuous distributions, the mode is a property of the *theoretical* density function, not something you reliably estimate from a sample.

But conceptually: the mode is the single most likely value under the distribution. It's where the probability density peaks.

---

### 5. Why They Diverge — Skewness Splits the Centres

For a perfectly symmetric distribution, all three centres coincide:

```
Symmetric distribution (e.g., Normal):

         ██
        ████
       ██████         mean = median = mode
      ████████            all at 0
     ██████████
    ────────────→
```

For a skewed distribution, they pull apart:

```
Right-skewed distribution (typical for returns):

       ██
      ████
     ██████           mode (peak, leftmost)
    ████████
   ███████████        median (halfway, middle)
  ██████████████
 █████████████████    mean (balance point, pulled RIGHT by tail)
────────────────→
    ↑    ↑     ↑
  mode  median mean
```

The long right tail pulls the mean to the right. The median, immune to the magnitude of tail observations, stays closer to the peak. The mode — the peak itself — is leftmost.

**The ordering tells you about skewness:**

| Ordering | What it means |
|----------|---------------|
| mode < median < mean | Right-skewed (positive skew) |
| mode = median = mean | Symmetric |
| mean < median < mode | Left-skewed (negative skew) |

For equity returns, you typically see: mode ≈ 0%, median ≈ 0.05%, mean ≈ 0.04%. Actually, with the negative skew typical of equity markets, the mean is often *below* the median — left-skewed returns. The relationship is an empirical question.

---

### 6. Which Centre Is the "Real" One?

This is a trick question. They're all real — they just answer different questions.

| When you care about... | The relevant centre is... |
|------------------------|--------------------------|
| Expected return — what you'd earn on average over many repetitions | **Mean** |
| Typical or representative day | **Median** |
| Most likely single outcome | **Mode** (but unreliable for samples) |
| Total P&L over a period (mean × n) | **Mean** |
| Whether more than half your days are profitable | **Median** |
| The "central tendency" in a skewed distribution for communication | **Median** (more intuitive to non-technical audiences) |

In finance, there's no single correct answer — you pick the one that answers the question you're asking.

**But here's the deeper point:** when you talk about the "location" of a distribution, you're usually talking about the mean — because the mean is the first moment, and moments are the language we use to decompose distributions. The mean is the centre in the **moment framework.** The median is the centre in the **quantile framework.** Both are valid; they're just different coordinate systems.

---

### 7. The Moment Framework vs the Quantile Framework

| | Moment framework | Quantile framework |
|---|---|---|
| **Location** | Mean ($\mu'_1$) | Median (50th percentile) |
| **Scale** | Standard deviation ($\sqrt{\mu_2}$) | IQR (75th − 25th percentile) |
| **Shape (asymmetry)** | Skewness ($\mu_3 / \sigma^3$) | (Median − Lower) vs (Upper − Median) |
| **Shape (tails)** | Kurtosis ($\mu_4 / \sigma^4$) | Tail percentiles (1st, 5th, 95th, 99th) |
| **Sensitive to outliers?** | Yes — by design | No — robust |
| **Used in parametric VaR?** | Yes | No (except indirectly via Cornish-Fisher) |
| **Used in historical VaR?** | No | Yes — VaR IS a quantile |

This is why historical and parametric VaR give different answers: **they use different frameworks.** Parametric VaR uses moments (mean, variance) and assumes the rest. Historical VaR uses quantiles directly — no assumptions about shape.

---

### 8. Summary

**"Centre" isn't one thing. It's three things, each answering a different version of "where?"**

| Centre | Definition | Sensitive to extremes? | Is it a moment? |
|--------|-----------|----------------------|-----------------|
| Mean | Balance point — centre of mass | **Yes** — distant observations pull hard | **Yes** — $\mu'_1$ |
| Median | Halfway point — centre of count | **No** — only order matters | No |
| Mode | Peak — centre of density | No | No |

The mean is the centre in the moment framework — the one we build all higher moments on. That doesn't make it the "right" centre. It makes it the centre that's mathematically convenient for the task of decomposing distributions into location, scale, and shape.

---

## Next step

The user may want to explore: how does the choice of centre affect VaR estimation? When should a risk manager prefer median-based measures over mean-based ones? Or move on to the scale property.