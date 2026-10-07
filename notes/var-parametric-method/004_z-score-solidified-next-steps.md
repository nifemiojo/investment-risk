# Z-Score Solidified — Your Answers and What They Reveal

**Date:** 2026-07-07
**Topic:** Verifying Z-score understanding and confirming readiness to move forward

---

## Your Answers — All Correct

### Q1 (implicit): 99% VaR uses z₀.₀₁

You correctly identified that for 99% confidence, we want the 1st percentile in the standard normal.

$$z_{0.01} \approx -2.326$$

Meaning: only 1% of the probability mass in N(0,1) sits below -2.326 standard deviations.

### Q2: 99% Parametric VaR for SPY

$$\text{VaR}_{99\%} = 0.04\% - 2.326 \times 1.2\% = -2.75\%$$

Correct.

Compare with 95% VaR for the same asset:

$$\text{VaR}_{95\%} = 0.04\% - 1.645 \times 1.2\% = -1.93\%$$

The 99% VaR is about 42% larger in magnitude — you're going 2.33σ out instead of 1.64σ.

### Q3: Geometric Intuition

Your answer is exactly right. Let me add a visual:

```
N(μ, σ) for SPY:

          ___
        /     \
      /         \         ← 95% VaR = -1.93% (z = 1.645)
    /             \
   /   ░░░░░░░░░░░░\____  ← 99% VaR = -2.75% (z = 2.326)
──┼─────────────────────────
  0  -1.93%    -2.75%
     ↑          ↑
    5% area    1% area
    to left    to left
```

Higher confidence = further left = larger z-score = larger loss number = fewer days worse than it.

---

## What You've Demonstrated

| Concept | Status |
|---|---|
| Z-score = distance in σ units | ✅ Solid |
| Standard normal as the "universal translator" | ✅ Solid |
| z_α = the value where Φ(z_α) = α | ✅ Solid |
| Formula derivation: μ − z·σ | ✅ Solid |
| Higher confidence → larger z → further into tail | ✅ Solid |

**The Z-score is no longer hazy.**

---

## The Only Thing Worth Adding

You mentioned "the std normal table which if I remember gives us the z score for different cdf probabilities." You're right — but let me make one thing explicit:

The standard normal CDF $\Phi(z)$ is **not analytically invertible**. There's no closed-form formula to go from "I want the 5th percentile" to "z = 1.6449." It's computed numerically (or looked up in a table).

In code, this is:

```python
from scipy.stats import norm

# Probability → Z-score (inverse CDF / percent point function)
z = norm.ppf(0.05)        # → -1.6449

# Z-score → Probability (CDF)
p = norm.cdf(-1.6449)     # → 0.05
```

`ppf` stands for "percent point function" — it's the inverse CDF. That's the bridge from confidence level to Z-score.

---

## Where We Are

You now understand:
- ✅ **What** the parametric method does (compresses data to μ, σ, imposes normal)
- ✅ **Why** the formula works (standardization + inverse CDF)
- ✅ **What** the Z-score is (distance, not probability)
- ✅ **How** confidence level maps to Z-score to VaR

The next natural step is implementation: write parametric VaR on real data, compare with historical, and watch where they diverge.

**Three options for the next step:**

1. **Code it.** Build parametric VaR on SPY/BND data side by side with historical — see the divergence live
2. **Deepen.** Explore when the normality assumption breaks and what that does to parametric VaR (diagnostics: Jarque-Bera, QQ plots)
3. **Extend.** Expected Shortfall — what happens *beyond* the VaR threshold (builds directly on what we just learned)

What calls to you?
