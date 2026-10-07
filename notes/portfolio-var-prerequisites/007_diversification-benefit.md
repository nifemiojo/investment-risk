# 007 — The Diversification Benefit: From Intuition to Number

**Date:** 2026-07-22
**Topic:** Quantifying how much risk reduction you actually get from holding multiple assets

---

## The naive benchmark

Imagine you hold SPY and BND. You compute VaR for each individually:

| Asset | Weight | Individual VaR (95%, 1-day) |
|-------|--------|---------------------------|
| SPY | 60% | 2.0% |
| BND | 40% | 1.0% |

The **naive sum** — what you'd get if you treated them as perfectly correlated:

$$\text{Naive sum} = 0.60 \times 2.0\% + 0.40 \times 1.0\% = 1.60\%$$

This is the worst case. If SPY and BND always crashed together, your portfolio VaR would be 1.60%.

But they don't. The actual portfolio VaR — computed by feeding the portfolio return series into `historical_var()` — might be, say, 1.15%.

## The diversification benefit formula

$$\text{Diversification benefit} = \frac{\text{Naive sum} - \text{Portfolio VaR}}{\text{Naive sum}}$$

For our example:

$$\text{Diversification benefit} = \frac{1.60\% - 1.15\%}{1.60\%} = \frac{0.45\%}{1.60\%} = 28.1\%$$

**Interpretation:** 28.1% of the risk you'd have if assets moved in lockstep is eliminated by diversification.

## What drives the magnitude?

The diversification benefit depends on three things:

1. **Correlation** — lower ρ → larger benefit. At ρ = 0.3, maybe 15% reduction. At ρ = −0.3, maybe 30%.
2. **Weight distribution** — the benefit is largest when weights are roughly balanced. One asset at 99% and the other at 1% → almost no benefit regardless of correlation, because the portfolio is essentially a single asset.
3. **Relative volatilities** — if one asset is dramatically more volatile than the other, it dominates the portfolio return distribution even at moderate weights, reducing the effective benefit.

## Why this formula uses the naive sum as the denominator

The naive sum is the natural baseline because it answers: "What would my risk be if I got zero diversification?" Everything below that baseline is the benefit of not holding a single asset.

You could also define it relative to the most volatile asset, or relative to an equal-volatility benchmark. But the naive sum — the weighted sum of individual VaRs — is the standard because it directly isolates the effect of imperfect correlation.

## Connecting to the distribution insight

Remember from file 002: diversification shows up as a narrower portfolio return distribution. The 5th percentile of that distribution is less extreme than the weighted average of the 5th percentiles of the individual distributions.

The diversification benefit formula quantifies exactly that gap. It answers: "How much less extreme?"

## As a monitoring signal

The plan mentions this, and it's worth previewing now: the diversification benefit isn't constant. You can compute it as a rolling metric:

- January 2020: benefit = 32% (SPY/BND correlation ≈ −0.4)
- March 2020: benefit = 18% (correlation spiked during COVID crash)
- October 2022: benefit = 5% (stocks and bonds crashed together)

When the benefit shrinks, your portfolio is more fragile than it looks. This is the monitoring signal we'll build in Notebook 12.

---

## Check-in

1. Does the naive sum as baseline make sense — that "sum of individual VaRs" represents the ρ = +1 worst case?
2. Why does a balanced weight distribution give the largest benefit? Can you reason through a 99/1 portfolio mentally?
3. Does the link from "narrower distribution" (file 002) to "quantified benefit" (this file) connect cleanly?
