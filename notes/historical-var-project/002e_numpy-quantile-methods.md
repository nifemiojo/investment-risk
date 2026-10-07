# NumPy quantile methods — what they mean for VaR

**Date:** 2026-07-12
**Topic:** Understanding the interpolation methods behind `np.quantile` and which matter for VaR
**Turn:** 002e

## User request

Let's go over the numpy quantile methods.

## Work and response

`np.quantile(data, q, method=...)` has 13 interpolation strategies. For VaR, only two matter. But let's understand what's actually happening under all of them.

### The core idea

When you ask for the 5th percentile of 10 observations, the fractional index is rarely an integer:

$$i = q \times (n - 1) = 0.05 \times 9 = 0.45$$

Index 0.45 lies between the worst observation (index 0) and the second-worst (index 1). Every method answers the same question differently: **what value do you assign to index 0.45?**

### The ones that exist (abridged)

Using the sample `[-5%, -3%, -2%, -1%, 0%, 1%, 2%, 3%, 4%, 5%]` at the 5th percentile (i = 0.45, between -5% at index 0 and -3% at index 1):

| Method | What it does | Result | Intuition |
|--------|-------------|--------|-----------|
| `"linear"` | Linear interpolation between adjacent values | -4.1% | Smooth, uses all information. Production standard. |
| `"lower"` | Take the lower of the two | -5.0% | Discrete. Conservative — always the worse outcome. |
| `"higher"` | Take the higher of the two | -3.0% | Discrete. Optimistic — always the better outcome. |
| `"nearest"` | Take whichever is closer | -5.0% | Discrete. i=0.45 is closer to index 0 than index 1. |
| `"midpoint"` | Average of the two | -4.0% | Discrete. Halfway regardless of fractional position. |

The other eight methods (`"inverted_cdf"`, `"averaged_inverted_cdf"`, `"closest_observation"`, `"interpolated_inverted_cdf"`, `"hazen"`, `"weibull"`, `"median_unbiased"`, `"normal_unbiased"`) differ in how they compute the fractional index `i` itself — they use different formulas for $i = f(q, n)$. For VaR with 252+ observations, the difference between index formulas is negligible (fractions of one day's return). The interpolation strategy (linear vs discrete) matters far more.

### Which actually matter for VaR?

| Method | VaR name | When you'd use it |
|--------|----------|-------------------|
| `"linear"` | interpolation | Production. Smooth, stable, standard in every risk system. |
| `"lower"` | nearest-rank | Communication. "The 13th worst day out of 252" is explainable to non-technical stakeholders. |

Everything else is noise. `"higher"` understates risk. `"nearest"` and `"midpoint"` have no conceptual justification for VaR. The index-formula variants change `i` by tiny amounts that don't matter at n ≥ 252.

### Why our mapping is correct

```python
_PERCENTILE_METHOD = {
    "interpolation": "linear",
    "nearest-rank": "lower",
}
```

- `"linear"` is the right numpy method for interpolation — it uses the fractional distance between the two bracketing points.
- `"lower"` is the right numpy method for nearest-rank — it rounds down, taking the conservative side of the bracket.

Note: `"lower"` is not exactly the textbook nearest-rank formula ($\lceil P \times n \rceil$, ceiling). It uses the lower of the two bracketing values at numpy's interpolated index position. At n = 252, the difference is at most one observation — one day out of 252. For a learning project, this is fine. Production systems that care about this distinction would compute nearest-rank manually.

### The key insight (repeated because it's worth it)

At 252 observations, the difference between `"linear"` and `"lower"` is interpolating a fraction of one day's return. The window size choice (60 vs 252 vs 504) moves VaR by percentage points. The interpolation method moves it by basis points. **Window choice dominates convention choice.**