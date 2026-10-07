# 012 — Naive Sum in Historical VaR: Percentile of Weighted Sum ≠ Weighted Sum of Percentiles

**Date:** 2026-07-22
**Topic:** Why the naive sum is the ρ = +1 benchmark in historical (non-parametric) VaR

---

**Question:** In the historical VaR context (not parametric), where does the naive sum come from?

**Answer:** It comes from a simpler intuition than the variance formula — no normality needed.

### Two approaches

**Naive:** Take each asset's individual VaR (the 5th percentile threshold from its own history), blend with weights:

$$\text{Naive} = w_1 \times \text{VaR}_1 + w_2 \times \text{VaR}_2$$

"SPY's worst-5% threshold is −2.0%. BND's is −1.0%. At 60/40, my threshold is 0.60 × 2.0% + 0.40 × 1.0% = 1.6%."

**Actual:** Compute $r_p = w_1r_1 + w_2r_2$ for every day, then find the 5th percentile of that series.

### Why they differ

The **percentile of a weighted sum ≠ weighted sum of percentiles** — unless the returns are perfectly ordered day by day.

Concrete example: on SPY's 13th-worst day, BND happened to have a *good* day (assets moved opposite). That day's portfolio return gets pulled up — it might not even make the bottom 5% of the portfolio distribution. But the naive approach treats SPY's 13th-worst return as a building block regardless of what BND did that day.

The naive approach implicitly assumes both assets' worst days line up — that the day-ordering is preserved. That only happens when ρ = +1.

### The benchmark interpretation

The naive sum is the ρ = +1 worst case NOT because of any parametric formula, but because it's what portfolio VaR would equal if every bad-SPY day were also a bad-BND day — if the historical pairings had always been in lockstep. The actual portfolio VaR is lower because in reality, the bad days don't perfectly align.
