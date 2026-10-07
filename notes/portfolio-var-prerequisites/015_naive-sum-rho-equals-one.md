# 015 — What ρ = +1 Actually Means for the Naive Sum

**Date:** 2026-07-22
**Topic:** Why the naive sum assumes the worst days align, and ρ = +1 is the condition that makes that true

---

**Question:** "The naive sum ignores the fact that the 5th percentile returns for both assets may not have occurred on the same day? Assumes that they do? What does the correlation = +1 assumption mean?"

**Answer:** Exactly right on both counts.

### What the naive sum assumes

$w_1\text{VaR}_1 + w_2\text{VaR}_2$ implicitly says: "the day SPY hit its 5th percentile return was also the day BND hit its 5th percentile return." It takes two thresholds from potentially different days and blends them as if they happened together.

### Why ρ = +1 makes that assumption true

When ρ = +1, the returns are perfectly linearly related — the rank ordering is identical across assets:

- SPY's worst day IS BND's worst day
- SPY's 12th percentile day IS BND's 12th percentile day
- The sort order is preserved

Under ρ = +1, the percentile of the weighted sum equals the weighted sum of percentiles. The naive sum equals the portfolio VaR. There's no gap — no diversification benefit.

### Why ρ < +1 breaks it

Under any ρ < +1, the rank ordering breaks. SPY's 5th percentile day might be BND's 80th percentile day. The weighted sum on that day gets pulled toward BND's mild outcome, and the 5th percentile of the portfolio distribution lands somewhere less extreme than the naive sum.

**That gap IS the diversification benefit.**
