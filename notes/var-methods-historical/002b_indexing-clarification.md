# Indexing Clarification: Two Coordinate Systems

**Date:** 2026-07-06
**Topic:** Why nearest rank and interpolation give different answers from the same sorted list

---

## Your Observation

You spotted:

> Nearest rank maps the first observation to cover everything from 0 to $1/n$, so the 1st, 5th, and 10th percentiles all land on the same value. Interpolation maps the first observation to exactly the 0th percentile, so the 5th percentile lands between the first and second observations.

That's exactly right. Here it is visually.

---

## Same Sorted List, Two Different Coordinate Systems

```
Sorted returns (worst → best):
  -3.2%    -2.1%    -1.5%    -0.8%    -0.3%    +0.3%    +0.5%    +0.7%    +1.2%    +2.0%

Nearest rank index:   1        2        3        4        5        6        7        8        9       10
                       ↑
                   r = ceil(0.05 × 10) = 1  →  -3.2%

Interpolation index:  0        1        2        3        4        5        6        7        8        9
                       ↑
                   i = 0.05 × 9 = 0.45  →  between 0 and 1  →  -2.71%
```

---

## What's Happening

**Nearest rank:** The first observation "absorbs" everything up to the $1/n$ threshold. With 10 observations, the first rank covers percentiles 0 through 10%. So the 1st, 5th, and 10th percentiles all return −3.2%. The value doesn't change until you cross the 10% boundary, at which point it jumps to the second-worst observation.

**Interpolation:** The first observation represents exactly the 0th percentile. The 5th percentile falls 45% of the way between observations 0 and 1, giving −2.71%. There are no "jumps" — the VaR moves continuously as you vary the confidence level.

---

## The Deeper Point

Neither is "wrong." They're different answers to the same question: **What percentile does the worst observation in the sample represent?**

- Nearest rank answer: "It represents everything from 0 to $1/n$."
- Interpolation answer: "It represents exactly the 0th percentile."

With 252 observations, $1/252 \approx 0.4\%$, so the difference between the two conventions shrinks to a rounding error. The indexing choice only matters for small samples, toy examples, or very extreme percentiles (99.9% VaR from 252 days).

---

## Why This Matters for Implementation

When you code this up, you don't need to implement either formula by hand. Both conventions are built into standard libraries:

```python
import numpy as np

# Nearest rank
var_nearest = np.percentile(returns, 5, method='lower')  # or method='higher'

# Linear interpolation (default)
var_interp = np.percentile(returns, 5)  # default is method='linear'
```

The key is knowing **which one you're using and why** — not which formula to type.
