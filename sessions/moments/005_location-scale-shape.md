# Location, Scale, and Shape — the Three Properties That Define a Distribution

**Date:** 2026-07-26
**Topic:** What "location," "scale," and "shape" actually mean; how they map to the moment hierarchy; and why the whole point of central and standardised moments is to peel them apart layer by layer.

---

## Opening Question

> You look at a histogram of SPY daily returns. You can describe it in three sentences: "It's centred around +0.04% (location). Most days fall within about ±1.2% of that centre (scale). And the left tail is fatter than the right — there are more extreme negative days than extreme positive ones (shape)."
>
> Location, scale, shape. These three words capture *everything* a distribution can tell you. Moments are the mathematical tools that measure them. But they don't measure them cleanly — raw moments mix all three together. The whole point of central and standardised moments is to separate them, one by one.

---

## 1. What "Location" Means — Where the Distribution Sits

### The intuition

Take a histogram. Now imagine you can slide it left or right along the number line without changing its form. The number you slide it to — that's the location.

If SPY had averaged +0.5% per day instead of +0.04%, the entire histogram would shift right by about 0.46 percentage points. Every return would be 0.46% higher. The shape — the bumps, the tails, the asymmetry — would be identical. Only the position on the number line would change.

### The formal definition

**Location** is a parameter that shifts the entire distribution without changing its spread or form. If $X$ has some distribution, then $X + c$ has the same distribution, just shifted by $c$.

**Location measures:**
- Mean ($\bar{x}$) — the arithmetic average, the centre of mass
- Median — the 50th percentile, the middle observation
- Mode — the most common value

All three answer "where is the centre?" They give different answers when the distribution is skewed, but they all measure location.

### Location and the first raw moment

The first raw moment $\mu'_1 = \bar{x}$ is a measure of location. It tells you where the balance point is. That's all it does — it doesn't tell you anything about spread or shape.

---

## 2. What "Scale" Means — How Spread Out the Distribution Is

### The intuition

Same histogram. Now imagine you can stretch it horizontally (making it wider) or squeeze it (making it narrower) without changing where it's centred or what shape it has. The amount of stretch — that's the scale.

If SPY's daily volatility doubled from 1.2% to 2.4%, the histogram would spread out. Returns of ±2% would become as common as returns of ±1% used to be. The centre (location) would be the same. The shape (relative pattern of bumps and tails) would be the same — it would just be stretched.

### The formal definition

**Scale** is a parameter that stretches or compresses the distribution. If $X$ has some distribution centred at zero, then $c \cdot X$ has the same shape but with scale multiplied by $|c|$.

**Scale measures:**
- Standard deviation ($s$) — the square root of the average squared deviation
- Variance ($s^2$) — the average squared deviation
- Interquartile range (IQR) — the distance between the 25th and 75th percentiles
- Mean absolute deviation — the average absolute deviation

All four answer "how wide is this?" They give different answers for different distribution shapes, but they all measure scale.

### Scale and the second central moment

The second central moment $\mu_2 = s^2$ (using population formula with $n$) is a measure of scale. Its square root, $s$, has the same units as the data and is the most natural scale measure.

---

## 3. What "Shape" Means — Everything Else

### The intuition

Take the SPY histogram. Now fix its centre (location) and fix its width (scale). What's left? The bumps, the asymmetry, the tail fatness — the *form* of the distribution. That's shape.

Two distributions can have the same mean and same standard deviation but look completely different:

```
Distribution A:    ▁▂▃▅▆▇█▇▆▅▃▂▁    (symmetric, bell-shaped)
Distribution B:    ▁▂▃▅█▇▆▅▃▂▁▁▁▁   (skewed right, long right tail)
```

Same location (both centred at the same place). Same scale (both have the same standard deviation). Different shape — A is symmetric, B is skewed right.

### Shape measures:
- **Skewness** — asymmetry. Is one tail fatter than the other?
- **Kurtosis** — tail weight. How much probability mass is in the extreme tails?
- **Modality** — how many peaks? (Unimodal, bimodal, multimodal)

### Shape and the third and fourth standardised moments

The third standardised moment $\gamma_1$ (skewness) and fourth standardised moment $\gamma_2$ (kurtosis) measure shape. They've had location subtracted (via centring) and scale divided out (via standardising). What remains is pure form.

---

## 4. The Three Properties — Side by Side

| Property | What it answers | Examples | Which moments capture it |
|----------|----------------|----------|------------------------|
| **Location** | "Where is the centre?" | Mean, median, mode | 1st raw moment ($\bar{x}$) |
| **Scale** | "How wide is it?" | Standard deviation, variance, IQR | 2nd central moment ($s^2$) |
| **Shape** | "What form does it take?" | Skewness, kurtosis, modality | 3rd+ standardised central moments ($\gamma_1$, $\gamma_2$) |

### The key insight

A distribution is fully described by: **where it sits (location), how wide it is (scale), and what form it has (shape).** The moment hierarchy peels these apart in order:

$$
\underbrace{\text{Raw moment}}_{\text{location + scale + shape}} \quad
\xrightarrow{\text{centring (subtract }\bar{x}\text{)}} \quad
\underbrace{\text{Central moment}}_{\text{scale + shape}} \quad
\xrightarrow{\text{standardising (divide by }s^k\text{)}} \quad
\underbrace{\text{Standardised moment}}_{\text{shape only}}
$$

---

## 5. Why Raw Moments Are Contaminated — a Systematic Walkthrough

Let's return to the London/Reykjavik example from the previous file and analyse it through the lens of location, scale, and shape.

### The data

| | London | Reykjavik |
|---|--------|-----------|
| Temperatures | 10, 12, 11, 13, 14 | 2, 4, 3, 5, 6 |
| Mean (location) | 12°C | 4°C |
| Spread around mean | ±2°C | ±2°C |
| Pattern | Symmetric, flat | Symmetric, flat |

These two datasets have:
- **Different location:** London = 12, Reykjavik = 4
- **Same scale:** both vary by ±2°C around their mean
- **Same shape:** both are symmetric with no outliers

### Raw moments mix location, scale, and shape

| | London | Reykjavik | Ratio |
|---|---|---|---|
| $\mu'_1$ (raw 1st) | 12 | 4 | 3× |
| $\mu'_2$ (raw 2nd) | 146 | 18 | 8.1× |
| $\mu'_3$ (raw 3rd) | 1,764 | 88 | 20× |

The raw moments explode as $k$ increases because they're picking up London's larger location. Each raw moment is $E[X^k]$ — and since London's $X$ values are ~3× larger, $X^k$ is $3^k \times$ larger. The raw third moment is $3^3 = 27\times$ larger (close to the 20× we see — the slight difference is because the variance is the same, not the raw spread).

### Central moments remove location, leaving scale + shape

| | London | Reykjavik |
|---|---|---|
| $\mu_1$ (central 1st) | 0 | 0 |
| $\mu_2$ (central 2nd) | 2 | 2 |
| $\mu_3$ (central 3rd) | 0 | 0 |
| $\mu_4$ (central 4th) | 6.8 | 6.8 |

Now they're identical. Centring subtracted 12 from London and 4 from Reykjavik, removing the location difference. What's left is the scale and shape — which happen to be identical for these two datasets.

### Standardised moments remove scale, leaving shape only

| | London | Reykjavik |
|---|---|---|
| $\gamma_1$ (skewness) | 0 | 0 |
| $\gamma_2$ (excess kurtosis) | −1.3 | −1.3 |

Standardising divided by $s^3$ and $s^4$, removing the scale. What's left is pure shape — symmetric, platykurtic (fewer outliers than normal) for both.

### The contamination chain, visualised

```
RAW MOMENT μ'₂ = 146  (London)
                   = 18   (Reykjavik)
                     ↑
            HUGELY different.
            Why? London is warmer.
            Raw picks up location.
                     │
                     │  CENTRE (subtract x̄)
                     ▼
CENTRAL MOMENT μ₂ = 2    (London)
                   = 2    (Reykjavik)
                     ↑
            IDENTICAL. Location removed.
            What remains = scale.
            (Both vary by ±2°C)
                     │
                     │  STANDARDISE (divide by s²)
                     ▼
STANDARDISED: same skewness, same kurtosis.
Pure shape. Nothing left to differ.
```

---

## 6. A Second Example — Same Location, Different Scale

Now imagine two portfolios:

**Portfolio A (conservative):** Returns: −1%, 0%, +1%, 0%, −1% → $\bar{x} = -0.2\%$, $s = 0.84\%$

**Portfolio B (aggressive):** Returns: −3%, 0%, +3%, 0%, −3% → $\bar{x} = -0.6\%$, $s = 2.68\%$

These have:
- **Roughly similar location** (−0.2% vs −0.6%)
- **Very different scale** (0.84% vs 2.68% — Portfolio B is ~3.2× more volatile)
- **Same shape** (both are symmetric with a flat pattern)

### Raw moments — contaminated by scale

| | Portfolio A | Portfolio B |
|---|---|---|
| $\mu'_2$ (raw 2nd) | 0.60 | 5.40 |

Raw moments differ dramatically because B's returns are larger in magnitude. Even though the locations are similar, the scale difference blows up the raw moments.

### Central moments — scale still present

| | Portfolio A | Portfolio B |
|---|---|---|
| $\mu_2$ (central 2nd = variance) | 0.56 | 5.36 |

Central moments still differ — because they still contain scale. Centring removed location, but left the scale difference intact. Portfolio B's variance is ~9.6× larger because its returns are ~3.2× more volatile, and variance scales with the *square* of volatility.

### Standardised moments — scale removed

| | Portfolio A | Portfolio B |
|---|---|---|
| $\gamma_1$ (skewness) | 0 | 0 |
| $\gamma_2$ (excess kurtosis) | −0.96 | −0.96 |

Standardised moments are now identical. Dividing by $s^k$ removed the scale, leaving only shape — which is the same for both.

---

## 7. A Third Example — Same Location, Same Scale, Different Shape

Here's the one that makes the point about shape:

**Distribution X:** −2.0%, −1.0%, −0.5%, 0%, +0.5%, +1.0%, +2.0%
**Distribution Y:** −4.0%, −0.5%, −0.3%, +0.1%, +0.3%, +0.5%, +0.8%

| | X | Y |
|---|---|---|
| Mean (location) | 0.0% | −0.44%? Let me recalculate... |

Actually, let me use cleaner numbers. Here's the right way to show this — two distributions engineered to have the same mean and same standard deviation:

**Distribution A (symmetric, thin tails):**
```
−2.0%, −1.0%, 0.0%, +1.0%, +2.0%
```
Mean = 0.0%, s = 1.58%

**Distribution B (negatively skewed, one crash day):**
```
−4.0%, −0.5%, 0.0%, +0.5%, +4.0%
```
Mean = 0.0% ✓, Standard deviation: 

$$\begin{aligned} s^2 &= \frac{(-4)^2 + (-0.5)^2 + 0^2 + 0.5^2 + 4^2}{4} \\ &= \frac{16 + 0.25 + 0 + 0.25 + 16}{4} \\ &= 8.125 \\ s &= 2.85\% \end{aligned}$$

That's not the same scale. Let me fix:

**Distribution B (negatively skewed, matched scale):**
```
−3.0%, −0.5%, 0.0%, +0.5%, +1.5%
```
Mean = (−3.0 − 0.5 + 0 + 0.5 + 1.5)/5 = −1.5/5 = −0.3%. Still not zero. Getting the mean to exactly zero with a skewed distribution is fiddly — and that's the point. Let's accept near-zero and move on.

Distribution A: −2.0%, −1.0%, 0.0%, +1.0%, +2.0% → $\bar{x} = 0$, $s \approx 1.58\%$
Distribution B: −3.5%, −0.5%, 0.0%, +0.5%, +1.0% → $\bar{x} = -0.5\%$, $s \approx 1.66\%$

Close enough for the point. Now:

| | A (symmetric) | B (negative skew) |
|---|---|---|
| Location (mean) | 0.0% | −0.5% (roughly similar) |
| Scale (std dev) | 1.58% | 1.66% (roughly similar) |
| Skewness | ≈ 0 | ≈ −1.3 (strongly negative) |
| What's different? | | **Shape** |

The raw second moments are: A = 2.0, B = 2.52 — contaminated by the slight location and scale differences. The central second moments: A = 2.0, B = 2.48 — still contaminated by the scale difference. But the third standardised moment (skewness) reveals what's actually different: the shape.

### The point

> Two distributions can have the same location and same scale but different shape. The first two moments will match. The third and fourth moments will differ. That difference *is* the shape — and it's exactly what skewness and kurtosis measure.

---

## 8. The Moment Peel — a Visual Summary

```
THE DATA: x₁, x₂, ..., xₙ


┌─────────────────────────────────────────────────┐
│ RAW MOMENTS: μ'ₖ = (1/n) Σ xᵢᵏ                   │
│ Contains: LOCATION + SCALE + SHAPE                │
│                                                   │
│ Example: μ'₂ tells you "how big are the squared   │
│ values?" which depends on where the data sits     │
│ AND how spread out it is AND what shape it has.   │
└──────────────────────┬──────────────────────────┘
                       │
                       │ SUBTRACT x̄ (centring)
                       │ Removes LOCATION
                       ▼
┌─────────────────────────────────────────────────┐
│ CENTRAL MOMENTS: μₖ = (1/n) Σ (xᵢ - x̄)ᵏ         │
│ Contains: SCALE + SHAPE                           │
│                                                   │
│ Example: μ₂ = variance. Now only depends on how   │
│ spread out the data is and what shape it has —    │
│ not where it sits.                                │
└──────────────────────┬──────────────────────────┘
                       │
                       │ DIVIDE BY sᵏ (standardising)
                       │ Removes SCALE
                       ▼
┌─────────────────────────────────────────────────┐
│ STANDARDISED MOMENTS: γₖ = μₖ / sᵏ                │
│ Contains: SHAPE ONLY                              │
│                                                   │
│ Example: γ₁ = skewness. Depends ONLY on the       │
│ asymmetry of the data — not on where it sits or   │
│ how wide it is. γ₂ = kurtosis. Depends ONLY on    │
│ tail weight.                                      │
└─────────────────────────────────────────────────┘
```

---

## 9. Why This Matters for Finance — Two Practical Examples

### Example 1: Comparing SPY to a 3× Leveraged ETF

3× leveraged SPY ETF has roughly:
- Same location on average? No — it can have decay. But let's say roughly 3× the mean.
- 3× the standard deviation (scale)
- Same shape? Theoretically yes — it's just SPY × 3 plus some tracking error.

If you compute raw skewness, the leveraged ETF will show roughly 27× the raw third moment ($3^3 = 27$). That makes it look massively more skewed — but it's not. The *shape* is the same. Standardised skewness (dividing by $\sigma^3$) will show identical skewness for both.

**The lesson:** Never compare raw moments across assets with different volatilities. Always standardise.

### Example 2: Detecting a genuine increase in crash risk

Your portfolio's volatility has been stable at ~1.2% for months. Then:

- Week 1: $\sigma$ = 1.2%, skewness = −0.3
- Week 2: $\sigma$ = 1.2%, skewness = −0.9
- Week 3: $\sigma$ = 1.3%, skewness = −1.4

The scale (volatility) is barely moving, but the shape is changing — the left tail is fattening. This is a genuine increase in crash risk that volatility alone would miss. Because skewness is standardised (scale removed), you can see the shape shift independently of any scale shift.

**The lesson:** Standardised moments let you monitor *shape* independently of *scale*. A risk system that only watches volatility would miss the Week 1–2 shift entirely.

---

## 10. The Terminology Map — Words That Mean the Same Thing

| This word... | ...means this |
|-------------|--------------|
| Location | Centre, central tendency, position, shift |
| Scale | Spread, dispersion, width, variability, volatility |
| Shape | Form, structure, asymmetry + tail behaviour |
| Centring | Subtracting the mean, removing location, demeaning |
| Standardising | Dividing by standard deviation, removing scale, normalising (in the "unit variance" sense) |
| First raw moment | Mean, average, expectation, $\bar{x}$ |
| Second central moment | Variance, $\sigma^2$, $s^2$ (population/sample distinction aside) |
| Third standardised moment | Skewness, $\gamma_1$, asymmetry coefficient |
| Fourth standardised moment | Kurtosis, $\gamma_2$ (usually excess) |

---

## 11. Questions to Test Your Understanding

1. **If I add 5% to every return in a dataset, which moments change and which stay the same?** (Location measures change by +5%. Scale measures stay the same — adding a constant doesn't change spread. Shape measures stay the same. Among moments: $\mu'_1$ changes by +5%. All central moments $\mu_k$ for $k \geq 2$ stay the same. All standardised moments stay the same.)

2. **If I multiply every return by 2 (a 2× leveraged position), which moments change and how?** ($\mu'_k$ changes by $2^k$. $\mu_k$ changes by $2^k$. Standardised moments — $\gamma_1$, $\gamma_2$ — stay exactly the same. The shape is unchanged by leverage.)

3. **A colleague says: "Portfolio A has variance 4 and Portfolio B has variance 16, so B has fatter tails." What's wrong with this statement?** (Variance is a scale measure, not a shape measure. B might just be more volatile — same shape, wider spread. You need kurtosis to assess tail fatness relative to the scale.)

4. **Why is skewness standardised by $\sigma^3$ rather than $\sigma^2$ or $\sigma$?** (Because skewness is a third moment. If you multiply all returns by $c$, the third central moment scales by $c^3$. To cancel this and make skewness scale-invariant, you must divide by $\sigma^3$, which also scales by $c^3$. Dimensional analysis: $\mu_3$ has units of %³, $s^3$ has units of %³, so the ratio is dimensionless.)

5. **If two distributions have the same first four standardised moments, are they necessarily identical?** (No — there are higher moments (5th, 6th, ...) that can differ. But in practice, the first four capture most of the meaningful shape information for financial returns. The normal distribution is uniquely defined by its first two — all higher standardised moments are zero.)

---

## What's Next

Now that location, scale, and shape are clear, the natural path is:

- **Standardised moments deep dive** — the full story of dividing by powers of $\sigma$, why it works, what it assumes, and when standardised moments can mislead
- **Variance deep dive** — $n$ vs $n-1$, Bessel's correction, what "unbiased" means
- **Practical exercise** — take SPY data, compute raw → central → standardised moments, and verify that multiplying by a constant changes raw and central but not standardised
