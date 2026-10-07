# From Paths to VaR: The Aggregation Step

**Date:** 2026-07-10
**Topic:** How 10,000 paths of 10 days each become a single VaR number

---

## The Key: Each Path → One Number

You don't take a quantile *within* each path. Each path produces exactly one number: the cumulative return over the 10 days.

```
Path 1:  r₁, r₂, ..., r₁₀  →  R₁ = r₁ + r₂ + ... + r₁₀   (one 10-day return)
Path 2:  r₁, r₂, ..., r₁₀  →  R₂ = r₁ + r₂ + ... + r₁₀
...
Path 10000: r₁, r₂, ..., r₁₀ → R₁₀₀₀₀
```

Then you have 10,000 ten-day returns. Sort them. Read the 5th percentile. That's the 10-day VaR.

---

## Toy Example: 3 Paths of 3 Days

Let me make it concrete with a tiny example.

**Model:** $r_t = 0.3 \cdot r_{t-1} + \epsilon_t$, where $\epsilon_t \sim N(0, 1\%)$

**Terms:**
- $r_t$: return on day t
- $\epsilon_t$: random shock on day t, drawn from N(0, 1%)

**Path 1:**
```
Day 1: ε₁ = +0.8%, r₁ = 0 + 0.8% = +0.80%
Day 2: ε₂ = -0.3%, r₂ = 0.3 × 0.80% + (-0.3%) = -0.06%
Day 3: ε₃ = +1.1%, r₃ = 0.3 × (-0.06%) + 1.1% = +1.08%
→ R₁ = 0.80 + (-0.06) + 1.08 = +1.82%
```

**Path 2:**
```
Day 1: ε₁ = -1.5%, r₁ = -1.50%
Day 2: ε₂ = -0.8%, r₂ = 0.3 × (-1.50%) + (-0.8%) = -1.25%
Day 3: ε₃ = +0.4%, r₃ = 0.3 × (-1.25%) + 0.4% = +0.03%
→ R₂ = -1.50 + (-1.25) + 0.03 = -2.72%
```

**Path 3:**
```
Day 1: ε₁ = +0.2%, r₁ = +0.20%
Day 2: ε₂ = +0.7%, r₂ = 0.3 × 0.20% + 0.7% = +0.76%
Day 3: ε₃ = -0.1%, r₃ = 0.3 × 0.76% + (-0.1%) = +0.13%
→ R₃ = 0.20 + 0.76 + 0.13 = +1.09%
```

**Now sort the three 10-day returns (3-day in this toy):**
```
-2.72%, +1.09%, +1.82%
```

With only 3 paths, the 5th percentile isn't meaningful. But with 10,000 paths, you'd sort all 10,000 ten-day returns and read the 500th worst (5th percentile). That's your 10-day VaR.

---

## The Full Algorithm for Multi-Period VaR

```
For each path i = 1 to N:
    Initialize state (e.g., today's volatility)
    For each day t = 1 to H (horizon):
        Draw random shock ε_t
        Compute r_t from the process equation
        Update state for next day
    Compute cumulative return: R_i = r_1 + r_2 + ... + r_H

Sort R₁, R₂, ..., R_N
VaR = α-percentile of sorted R's
```

**Terms:**
- $N$: number of paths (e.g., 10,000)
- $H$: horizon in days (e.g., 10)
- $R_i$: cumulative return over H days for path i

---

## The Contrast With Parametric

Parametric 10-day VaR does this:

$$1\text{-day VaR} \times \sqrt{10}$$

It assumes each day's return is an independent draw from the same distribution. The √10 comes from:

$$\text{Var}(r_1 + ... + r_{10}) = 10 \cdot \sigma^2 \quad \text{(if independent)}$$

$$\sigma_{10\text{-day}} = \sqrt{10} \cdot \sigma_{1\text{-day}}$$

Monte Carlo with paths doesn't make that assumption. If the process has positive autocorrelation (momentum), the 10-day variance will be **more** than 10 × 1-day variance. If it has mean reversion, it will be **less**. The paths capture this automatically.

---

## Check-In

Does the aggregation step make sense? Each path collapses to one cumulative return. The VaR is the quantile of those cumulative returns across all paths.

And here's the follow-up: **what's the trade-off between N (number of paths) and H (horizon length)?** If you have a fixed computational budget — say you can afford 100,000 total daily simulations — how do you allocate between more paths (better percentile estimate) vs longer horizon?