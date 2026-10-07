# 013 — Worked Example: Naive Sum vs Actual Portfolio VaR

**Date:** 2026-07-22
**Topic:** Concrete 10-day walkthrough showing why the naive sum overstates risk when assets aren't perfectly correlated

---

## Setup

60/40 portfolio of two assets. 10 days of returns.

| Day | Asset A ($r_A$) | Asset B ($r_B$) | 60/40 Portfolio ($r_p$) |
|-----|----------------|----------------|------------------------|
| 1 | −1.8% | +0.3% | $0.60(-1.8) + 0.40(0.3) = -0.96\%$ |
| 2 | +1.2% | −0.1% | $0.60(1.2) + 0.40(-0.1) = +0.68\%$ |
| 3 | −0.5% | −0.2% | $0.60(-0.5) + 0.40(-0.2) = -0.38\%$ |
| 4 | +0.8% | +0.4% | $0.60(0.8) + 0.40(0.4) = +0.64\%$ |
| 5 | **−2.0%** | **+0.5%** | $0.60(-2.0) + 0.40(0.5) = \mathbf{-1.00\%}$ |
| 6 | +1.5% | +0.1% | $0.60(1.5) + 0.40(0.1) = +0.94\%$ |
| 7 | −0.3% | +0.2% | $0.60(-0.3) + 0.40(0.2) = -0.10\%$ |
| 8 | **−1.5%** | **−0.4%** | $0.60(-1.5) + 0.40(-0.4) = \mathbf{-1.06\%}$ |
| 9 | +2.0% | −0.2% | $0.60(2.0) + 0.40(-0.2) = +1.12\%$ |
| 10 | −0.8% | +0.1% | $0.60(-0.8) + 0.40(0.1) = -0.44\%$ |

---

## Step 1: Individual asset VaRs

Sort each asset's returns worst to best:

**Asset A:** −2.0, −1.8, −1.5, −0.8, −0.5, −0.3, +0.8, +1.2, +1.5, +2.0

**Asset B:** −0.4, −0.2, −0.2, −0.1, +0.1, +0.1, +0.2, +0.3, +0.4, +0.5

95% VaR (interpolation) — 0.05 quantile on 10 obs falls between index 0 and 1:

$$\text{VaR}_A \approx 1.91\% \quad\quad \text{VaR}_B \approx 0.38\%$$

---

## Step 2: Naive sum

$$\text{Naive} = 0.60 \times 1.91\% + 0.40 \times 0.38\% = 1.146\% + 0.152\% = 1.30\%$$

Interpretation: "If every bad day for A was also a bad day for B, my portfolio VaR would be 1.30%."

---

## Step 3: Actual portfolio VaR

Sort the $r_p$ column worst to best:

$$-1.06\%, -1.00\%, -0.96\%, -0.44\%, -0.38\%, -0.10\%, +0.64\%, +0.68\%, +0.94\%, +1.12\%$$

95% VaR (interpolation, 0.05 quantile):

$$\text{VaR}_p \approx 1.03\%$$

---

## Step 4: The gap

| Method | VaR |
|--------|-----|
| Naive sum (implicit ρ = +1) | 1.30% |
| Actual portfolio VaR | 1.03% |
| **Diversification benefit** | $\frac{1.30 - 1.03}{1.30} = \mathbf{20.8\%}$ |

---

## Why the gap exists: look at the pairings

The naive approach uses Asset A's worst return (−2.0%, Day 5) and blends it with Asset B's VaR threshold (−0.38%). It doesn't care what B *actually* did on Day 5.

But on Day 5, B actually did +0.5% — its best day in the sample. The portfolio return was −1.00%, not −1.30%. B cushioned the blow.

The actual worst portfolio day was Day 8 (−1.06%) — when both assets fell together (−1.5% and −0.4%). That day made the bottom of the portfolio distribution, not Day 5.

**The naive sum assumes the worst days align. Reality says they often don't.** The gap between the assumption and reality is the diversification benefit.

---

## Visualising the distribution shift

If we plot the three distributions (A, B, and the portfolio):

```
Asset A:   |---•----•---•----•---•----•---•-|   wide spread
Asset B:   |--•---•---•---•---•---•---•---•-|   narrow spread
Portfolio: |----•---•---•----•---•---•---•--|   narrower than A,
                                                  wider than B,
                                                  extremes pulled in
```

The portfolio distribution is somewhere between the two individual distributions — not as wide as the volatile asset, not as narrow as the stable one. The left tail (where VaR lives) is less extreme than Asset A's left tail, because on A's worst days, B often went the other way.

---

## Check-in

1. Day 5 vs Day 8 — can you see why Day 8 produced the worst portfolio return even though neither asset had its worst day?
2. The naive sum as an implicit assumption that "sort order is preserved" — does that mental model hold?
