# Quantiles and Percentiles — A Quick Refresher

**Date:** 2026-07-07
**Topic:** Clarifying quantiles, percentiles, and how they connect to VaR

---

## The One-Sentence Definition

A **quantile** is a threshold value below which a given fraction of the data falls.

That's it. Everything else is just naming conventions.

---

## Quantile vs Percentile — Same Thing, Different Units

| Term | Unit | Example | Meaning |
|---|---|---|---|
| **Quantile** | fraction (0 to 1) | 0.05-quantile | 5% of data below this value |
| **Percentile** | percentage (0 to 100) | 5th percentile | same thing |

They're interchangeable. The 0.05-quantile **is** the 5th percentile.

$$q_{0.05} = P_5$$

**Terms:**
- $q_{\alpha}$: the $\alpha$-quantile (fraction notation)
- $P_k$: the $k$th percentile (percentage notation)

---

## Concrete Example with Heights

```
100 students, sorted shortest to tallest:

Height:  5'0"  5'2"  5'4"  5'6"  5'8"  5'10"  6'0"  6'2"
         ↑                    ↑                    ↑
    0.05-quantile        0.50-quantile        0.95-quantile
    5th percentile       50th percentile      95th percentile
    (5% shorter)         (median)             (95% shorter)
```

Each quantile is a **position on the x-axis**, not a count or a probability. It's the *value* at that position.

---

## The Key Relationship: Quantile = Inverse CDF

This is the mathematical link you need:

$$\text{If } F(x) = P(X \leq x) \text{ is the CDF, then the } \alpha\text{-quantile } = F^{-1}(\alpha)$$

In words: **the α-quantile is the value x such that the CDF at x equals α.**

```
CDF:  probability → value          F(x) = "prob of being ≤ x"
Quantile: value ← probability      F⁻¹(α) = "value where prob ≤ value = α"
```

They're inverses of each other.

---

## Connecting to What You Already Know

### In the Standard Normal

```
z_0.05 = Φ⁻¹(0.05) = -1.6449

"z_0.05" means: the 0.05-quantile of N(0,1)
               = the 5th percentile of the standard normal
               = the value below which 5% of N(0,1) mass sits
```

The notation $z_{\alpha}$ literally means "the α-quantile of the standard normal."

### In VaR

```
Confidence = 95%  →  α = 0.05  →  we want the 0.05-quantile of returns

Historical approach:  find 0.05-quantile by sorting → position 13
Parametric approach:   find 0.05-quantile via N(μ,σ) → μ + z_0.05 × σ
```

Both methods are trying to find the same thing — the 0.05-quantile of (expected) returns. They just use different models to estimate it.

---

## The Full Chain for Parametric VaR

```
Confidence level  →  α (quantile)  →  z_α (standard normal quantile)  →  VaR
     95%                0.05                  -1.6449                    μ - 1.6449σ
```

Each arrow is a precise operation:
1. **Confidence → α:** $\alpha = 1 - \text{confidence}$
2. **α → z_α:** $z_{\alpha} = \Phi^{-1}(\alpha)$ (inverse CDF of standard normal)
3. **z_α → VaR:** $\text{VaR} = \mu - |z_{\alpha}| \cdot \sigma$

---

## Common Confusion: Quantile Notation

You'll see notation like:

| Notation | Meaning |
|---|---|
| $z_{0.05}$ | 0.05-quantile of the standard normal |
| $q_{0.05}$ | 0.05-quantile of whatever distribution |
| $\text{VaR}_{0.95}$ | VaR at 95% confidence (which uses the 0.05-quantile!) |

The VaR subscript convention is opposite to the quantile convention:
- $\text{VaR}_{0.95}$ means "95% confidence"
- But it's computed from the **0.05**-quantile
- Because $\text{VaR}_{1-\alpha}$ = the α-quantile of the loss distribution

This is a perennial source of confusion. The way to keep it straight:

$$\text{VaR}_{95\%} = \text{the } 0.05\text{-quantile of the return distribution}$$

The confidence level tells you what's ABOVE the threshold. The quantile tells you what's BELOW.

---

## In Code

```python
from scipy.stats import norm
import numpy as np

# Quantile of standard normal (α = 0.05)
z = norm.ppf(0.05)        # → -1.6449  (ppf = percent point function = inverse CDF)

# Quantile of empirical data
returns = np.array([-2.1, 0.8, -3.2, 1.1, ...])
empirical_quantile = np.percentile(returns, 5)   # → 0.05-quantile (5th percentile)

# Same thing, fraction notation
empirical_quantile = np.quantile(returns, 0.05)  # same result
```

---

## One-Line Summary

| You say | You mean |
|---|---|
| "5th percentile" | 0.05-quantile — the value where 5% of data is below |
| "$z_{0.05}$" | The 0.05-quantile of N(0,1) |
| "95% VaR" | The 0.05-quantile of the return distribution |
| $\Phi^{-1}(0.05)$ | The 0.05-quantile of the standard normal (same as $z_{0.05}$) |

All roads lead to the same thing: **a threshold value on the x-axis where α fraction of probability sits to the left.**

---

Does that clear it up? Or is there still fuzziness around why the VaR subscript (0.95) and the quantile (0.05) are complements?
