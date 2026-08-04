# Raw Moments vs Central Moments — the Two Ways to Measure a Distribution's Shape

**Date:** 2026-07-26
**Topic:** The distinction between raw moments (measured from zero) and central moments (measured from the mean), why central moments are what you actually use, and how they relate.

---

## Opening Question

> You have five daily returns: −2%, −1%, 0%, +1%, +2%. The average is 0%. If you square each return and average, you get $((-2)^2 + (-1)^2 + 0^2 + 1^2 + 2^2)/5 = 2$. That's a raw moment — the second raw moment. But the variance is also 2. Is that coincidence? What if the mean weren't zero — would the second raw moment and the variance still be the same?
>
> This is the raw-vs-central distinction. It's simple but it trips people up constantly. Let's make it concrete.

---

## 1. The Core Distinction — One Sentence Each

**Raw moment (moment about zero):** Take your data, raise each observation to the $k$-th power, average.

$$\mu'_k = \frac{1}{n}\sum_{i=1}^n x_i^k$$

**Central moment (moment about the mean):** First subtract the mean, *then* raise to the $k$-th power, then average.

$$\mu_k = \frac{1}{n}\sum_{i=1}^n (x_i - \bar{x})^k$$

The only difference is whether you measure deviations from **zero** (raw) or from **the mean** (central). That's it. Everything else follows from this one choice.

---

## 2. Why the Distinction Exists — a Concrete Example

Let's say you're measuring the "spread" of daily temperatures in two cities:

**London (temperatures in °C):** 10, 12, 11, 13, 14 — mean = 12°C
**Reykjavik (temperatures in °C):** 2, 4, 3, 5, 6 — mean = 4°C

Both cities have exactly the same *variation pattern* — the temperatures bounce around the local mean by ±2°C. But:

**Second raw moment for London:**
$$\frac{10^2 + 12^2 + 11^2 + 13^2 + 14^2}{5} = \frac{100 + 144 + 121 + 169 + 196}{5} = 146$$

**Second raw moment for Reykjavik:**
$$\frac{2^2 + 4^2 + 3^2 + 5^2 + 6^2}{5} = \frac{4 + 16 + 9 + 25 + 36}{5} = 18$$

The raw moments say London is massively more variable (146 vs 18). But that's nonsense — the variation is identical. The raw moment is contaminated by the fact that London's numbers are bigger to begin with.

**Second central moment for London:**
$$\frac{(10-12)^2 + (12-12)^2 + (11-12)^2 + (13-12)^2 + (14-12)^2}{5} = \frac{4 + 0 + 1 + 1 + 4}{5} = 2$$

**Second central moment for Reykjavik:**
$$\frac{(2-4)^2 + (4-4)^2 + (3-4)^2 + (5-4)^2 + (6-4)^2}{5} = \frac{4 + 0 + 1 + 1 + 4}{5} = 2$$

**Central moments say: identical spread. And they're right.** The centring removes the location — the fact that London is warmer — and isolates the shape.

> **The raw moment mixes location and shape. The central moment separates them. Raw moment = f(location, shape). Central moment = f(shape only).**

---

## 3. The First Moment — Where the Distinction Is Most Visible

### First raw moment

$$\mu'_1 = \frac{1}{n}\sum_{i=1}^n x_i = \bar{x}$$

The first raw moment *is* the mean. It tells you where the centre is.

### First central moment

$$\mu_1 = \frac{1}{n}\sum_{i=1}^n (x_i - \bar{x}) = \frac{1}{n}\left(\sum x_i - n\bar{x}\right) = \frac{1}{n}(n\bar{x} - n\bar{x}) = 0$$

**The first central moment is always exactly zero.** Always. For any dataset. Because the definition of the mean guarantees that positive and negative deviations cancel perfectly.

This is why nobody talks about "the first central moment." It's zero by construction, so it carries no information about the data. It's like asking "what's the average distance from the average?" — if you don't square or take absolute values, it's always zero.

### The takeaway

| Moment | Raw ($\mu'_k$) | Central ($\mu_k$) |
|--------|---------------|-------------------|
| 1st | The mean: $\bar{x}$ | Always 0 |
| 2nd | Average squared value | Variance |
| 3rd | Average cubed value | Skewness (unnormalised) |
| 4th | Average fourth-power value | Kurtosis (unnormalised) |

For $k \geq 2$, the central moment is what you actually want — it measures shape around the centre, not around zero.

---

## 4. The Algebraic Relationship — Central Moments from Raw Moments

You can express any central moment in terms of raw moments. This is useful because raw moments are computationally simpler (no need to pre-compute the mean), and some formulas are expressed in raw form.

### Second central moment (variance) from raw moments

$$\mu_2 = \mu'_2 - (\mu'_1)^2$$

**Derivation (every step):**

$$\begin{aligned}
\mu_2 &= \frac{1}{n}\sum_{i=1}^n (x_i - \bar{x})^2 \\[4pt]
&= \frac{1}{n}\sum_{i=1}^n (x_i^2 - 2x_i\bar{x} + \bar{x}^2) \quad \text{(expand the square)} \\[4pt]
&= \frac{1}{n}\sum x_i^2 - 2\bar{x} \cdot \frac{1}{n}\sum x_i + \bar{x}^2 \cdot \frac{1}{n}\sum 1 \\[4pt]
&= \mu'_2 - 2\bar{x} \cdot \bar{x} + \bar{x}^2 \cdot 1 \quad \text{(since } \frac{1}{n}\sum x_i = \bar{x} \text{)} \\[4pt]
&= \mu'_2 - 2\bar{x}^2 + \bar{x}^2 \\[4pt]
&= \mu'_2 - \bar{x}^2 \\[4pt]
&= \mu'_2 - (\mu'_1)^2
\end{aligned}$$

**What this says:** Variance = average of squares minus square of average. This is the formula you've probably seen before: $\text{Var}(X) = E[X^2] - (E[X])^2$. Now you know where it comes from — it's the relationship between the second central moment and the first two raw moments.

### Third central moment (unnormalised skewness) from raw moments

$$\mu_3 = \mu'_3 - 3\mu'_1\mu'_2 + 2(\mu'_1)^3$$

**Derivation (sketch — the pattern matters more than memorising):**

$$\begin{aligned}
\mu_3 &= \frac{1}{n}\sum (x_i - \bar{x})^3 \\[4pt]
&= \frac{1}{n}\sum (x_i^3 - 3x_i^2\bar{x} + 3x_i\bar{x}^2 - \bar{x}^3) \\[4pt]
&= \mu'_3 - 3\bar{x}\mu'_2 + 3\bar{x}^2\mu'_1 - \bar{x}^3 \\[4pt]
&= \mu'_3 - 3\mu'_1\mu'_2 + 3(\mu'_1)^2\mu'_1 - (\mu'_1)^3 \quad \text{(since } \bar{x} = \mu'_1\text{)} \\[4pt]
&= \mu'_3 - 3\mu'_1\mu'_2 + 2(\mu'_1)^3
\end{aligned}$$

### Fourth central moment (unnormalised kurtosis) from raw moments

$$\mu_4 = \mu'_4 - 4\mu'_1\mu'_3 + 6(\mu'_1)^2\mu'_2 - 3(\mu'_1)^4$$

The pattern: central moments are linear combinations of raw moments, with binomial-like coefficients. This is not a coincidence — it comes from expanding $(x - \bar{x})^k$ via the binomial theorem.

---

## 5. Worked Numerical Example — Raw and Central Side by Side

Let's use 5 daily returns: **−3%, −1%, 0%, +2%, +5%**

**Step 1: Compute the mean**
$$\bar{x} = \frac{-3 + (-1) + 0 + 2 + 5}{5} = \frac{3}{5} = 0.6\%$$

### Raw moments

| $k$ | Computation | $\mu'_k$ |
|-----|-------------|----------|
| 1 | $\frac{-3 + (-1) + 0 + 2 + 5}{5}$ | 0.6 |
| 2 | $\frac{(-3)^2 + (-1)^2 + 0^2 + 2^2 + 5^2}{5} = \frac{9 + 1 + 0 + 4 + 25}{5}$ | 7.8 |
| 3 | $\frac{(-3)^3 + (-1)^3 + 0^3 + 2^3 + 5^3}{5} = \frac{-27 + (-1) + 0 + 8 + 125}{5}$ | 21.0 |
| 4 | $\frac{(-3)^4 + (-1)^4 + 0^4 + 2^4 + 5^4}{5} = \frac{81 + 1 + 0 + 16 + 625}{5}$ | 144.6 |

### Central moments (direct computation)

First, deviations from the mean:

| $x_i$ | $x_i - \bar{x}$ | $(x_i - \bar{x})^2$ | $(x_i - \bar{x})^3$ | $(x_i - \bar{x})^4$ |
|-------|----------------|--------------------|--------------------|--------------------|
| −3% | −3.6 | 12.96 | −46.656 | 167.962 |
| −1% | −1.6 | 2.56 | −4.096 | 6.554 |
| 0% | −0.6 | 0.36 | −0.216 | 0.130 |
| +2% | +1.4 | 1.96 | 2.744 | 3.842 |
| +5% | +4.4 | 19.36 | 85.184 | 374.810 |

| $k$ | Sum of column | $\div 5$ | $\mu_k$ |
|-----|--------------|----------|---------|
| 1 | −3.6 + (−1.6) + (−0.6) + 1.4 + 4.4 = 0.0 | 0.0 | **0** (always) |
| 2 | 12.96 + 2.56 + 0.36 + 1.96 + 19.36 = 37.2 | 7.44 | **7.44** (variance) |
| 3 | −46.656 + (−4.096) + (−0.216) + 2.744 + 85.184 = 36.96 | 7.392 | **7.392** |
| 4 | 167.962 + 6.554 + 0.130 + 3.842 + 374.810 = 553.298 | 110.660 | **110.660** |

### Verify: central from raw

**Variance:** $\mu_2 = \mu'_2 - (\mu'_1)^2 = 7.8 - 0.6^2 = 7.8 - 0.36 = 7.44$ ✓

**Third central:** $\mu_3 = \mu'_3 - 3\mu'_1\mu'_2 + 2(\mu'_1)^3 = 21.0 - 3(0.6)(7.8) + 2(0.6)^3 = 21.0 - 14.04 + 0.432 = 7.392$ ✓

### Standardised moments (for interpretation)

$$\text{Standard deviation: } s = \sqrt{7.44} = 2.728\%$$

$$\text{Skewness: } \hat{\gamma}_1 = \frac{\mu_3}{s^3} = \frac{7.392}{2.728^3} = \frac{7.392}{20.30} = 0.364$$

$$\text{Excess kurtosis: } \hat{\gamma}_2 = \frac{\mu_4}{s^4} - 3 = \frac{110.660}{2.728^4} - 3 = \frac{110.660}{55.35} - 3 = 2.00 - 3 = -1.00$$

**Interpretation:** Slight positive skew (the +5% pulls the right tail out). Negative excess kurtosis (thinner tails than normal — not surprising with only 5 data points).

---

## 6. When Do Raw Moments Matter?

Raw moments aren't just an intermediate step. They matter in three contexts:

### 6.1 Computational efficiency

Computing all raw moments in one pass over the data (just raise to powers, no mean needed first) and then converting to central moments avoids a two-pass algorithm. In high-performance computing or streaming data, this matters.

### 6.2 Theoretical derivations

Many derivations use raw moments because they're algebraically cleaner. The relationship $\text{Var}(X) = E[X^2] - (E[X])^2$ is the most important example. You'll see this constantly:

$$\text{Cov}(X, Y) = E[XY] - E[X]E[Y]$$

This is the raw-moment form of covariance — it expresses it in terms of raw moments ($E[XY]$, $E[X]$, $E[Y]$) rather than central moments ($E[(X-\mu_X)(Y-\mu_Y)]$).

### 6.3 When zero is the meaningful reference point

For returns, the mean is usually close to zero (daily returns average ~0.04%). In this case, raw second moment ≈ central second moment, because $\bar{x}^2$ is tiny (0.04%² = 0.000016%², compared to a typical variance of ~1.44%²). For many practical purposes with daily returns, the distinction barely matters for the second moment.

But this is a *coincidence of the data*, not a property of the formula. For price levels (not returns), or for assets with large means, or for higher moments where $(\mu'_1)^k$ compounds, the distinction matters enormously.

---

## 7. Why Standardised Moments Use Central Moments

The standardised skewness and kurtosis formulas:

$$\hat{\gamma}_1 = \frac{\frac{1}{n}\sum(x_i - \bar{x})^3}{\left[\frac{1}{n}\sum(x_i - \bar{x})^2\right]^{3/2}} = \frac{\mu_3}{\mu_2^{3/2}}$$

$$\hat{\gamma}_2 = \frac{\frac{1}{n}\sum(x_i - \bar{x})^4}{\left[\frac{1}{n}\sum(x_i - \bar{x})^2\right]^2} - 3 = \frac{\mu_4}{\mu_2^2} - 3$$

Both build on central moments. The numerator is a central moment. The denominator is a power of the second central moment (variance). Everything is centred first, *then* standardised.

**Why?** Because you want pure shape, stripped of both location AND scale:
1. **Centring** (subtract $\bar{x}$) strips out location → central moments
2. **Standardising** (divide by $s^k$) strips out scale → standardised moments

What's left is pure shape: asymmetry and tail weight, independent of where the distribution sits and how wide it is.

---

## 8. The Intuition — Why Centring Changes Everything

Consider cubed deviations. Why does central vs raw matter so much for skewness?

**Raw third moment:** $\frac{1}{n}\sum x_i^3$

Take our five returns: −3, −1, 0, 2, 5.

- (−3)³ = −27 (large negative — pulls the average down)
- (−1)³ = −1 (small negative)
- 0³ = 0
- 2³ = 8 (positive)
- 5³ = 125 (very large positive — pulls the average up)

The +125 dominates. The raw third moment is +21.0 — it says "strongly positive." But is that because the distribution is actually positively skewed, or because the numbers happen to be mostly positive (mean = +0.6)?

**Central third moment:** $\frac{1}{n}\sum (x_i - 0.6)^3$

Now the deviations are: −3.6, −1.6, −0.6, +1.4, +4.4.

- (−3.6)³ = −46.66 (substantial negative)
- (−1.6)³ = −4.10 (small negative)
- (−0.6)³ = −0.22 (tiny negative)
- (+1.4)³ = +2.74 (small positive)
- (+4.4)³ = +85.18 (large positive)

The sum is +36.96 ÷ 5 = +7.39. Still positive, but much closer to the true shape story: moderate positive skew from that one +5% day.

The raw moment was inflated by the mean. The central moment removes the mean and reveals the actual asymmetry.

---

## 9. Summary Table — Everything at a Glance

| | Raw Moment ($\mu'_k$) | Central Moment ($\mu_k$) | Standardised Central |
|---|---|---|---|
| **Formula** | $\frac{1}{n}\sum x_i^k$ | $\frac{1}{n}\sum (x_i - \bar{x})^k$ | $\mu_k / \sigma^k$ |
| **Measures from** | Zero | The mean | The mean, then scaled by spread |
| **1st moment** | $\bar{x}$ (the mean) | 0 (always) | — |
| **2nd moment** | Average squared value | Variance ($\sigma^2$) | 1 (always — by definition) |
| **3rd moment** | Not interpretable | Directional asymmetry | Skewness ($\gamma_1$) |
| **4th moment** | Not interpretable | Tail weight | Kurtosis ($\gamma_2$ — excess) |
| **Uses** | Computation, derivations | Interpretation, analysis | Comparison across assets |
| **Contaminated by** | Location + scale + shape | Scale + shape (location removed) | Shape only |

---

## 10. Where This Shows Up In Your Phase 1 Work

| What you do | Which moment | Raw or central? |
|-------------|-------------|-----------------|
| `returns.mean()` | 1st raw | Raw — it IS the first raw moment |
| `returns.var()` or `returns.std()**2` | 2nd central | Central — computed as $\frac{1}{n-1}\sum(x_i - \bar{x})^2$ |
| `returns.skew()` | 3rd standardised central | Central, then divided by $\sigma^3$ |
| `returns.kurtosis()` | 4th standardised central | Central, then divided by $\sigma^4$ |
| `np.cov(X, Y)` | 2nd mixed central | Central — $E[(X-\mu_X)(Y-\mu_Y)]$ |
| `np.corrcoef(X, Y)` | 2nd standardised central | Central, then divided by $\sigma_X\sigma_Y$ |
| Parametric VaR: $\mu - z\sigma$ | 1st raw + 2nd central | Mixes raw ($\mu$) and central ($\sigma$) |
| Vol scaling: $r_t / \hat{\sigma}_t$ | 2nd central | Uses $\hat{\sigma}$ (standardised by it) |

---

## 11. Questions to Test Your Understanding

1. **Compute the second raw moment and the variance for these three numbers: 10, 12, 14.** Are they the same? Why or why not? (Hint: what's the mean?)

2. **If a dataset has mean zero, what is the relationship between raw and central moments?** (All raw moments equal their corresponding central moments. Because $\bar{x} = 0$, subtracting zero does nothing.)

3. **Why is $\mu_1$ (first central moment) always zero? Prove it.** (Show that $\sum(x_i - \bar{x}) = 0$ from the definition of $\bar{x}$.)

4. **You compute the skewness of SPY returns as −0.6. Someone else computes the *raw* third moment divided by the cube of the raw second moment. Will they get the same number?** (No — the raw version is contaminated by the mean. For SPY with a small positive mean, the difference is small but real. For something with a large mean — like a strongly trending asset — the difference would be enormous.)

5. **The relationship $\text{Var}(X) = E[X^2] - (E[X])^2$ is the raw-to-central bridge for the second moment. Can you write the equivalent bridge for the third moment?** (Yes: $\mu_3 = \mu'_3 - 3\mu'_1\mu'_2 + 2(\mu'_1)^3$. This is less commonly used but follows the same logic.)

6. **Why don't we talk about the "standardised first moment"?** (Because $\mu_1 = 0$ always, and $0/\sigma = 0$. Standardising zero gives zero. There's no information to extract.)

---

## What's Next

The natural next step is to deepen one of the central moments:

- **Variance deep dive:** the $n$ vs $n-1$ question (Bessel's correction), why it matters, what "unbiased" actually means, and the bias-variance trade-off in window length
- **Skewness deep dive:** what creates it, how to interpret it, why financial returns are negatively skewed, and what that means for VaR
- **Standardised vs unstandardised moments:** the full story of dividing by powers of $\sigma$ — why standardisation makes comparison possible and when it can mislead
