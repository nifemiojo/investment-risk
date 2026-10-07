# Percentile Conventions: Nearest Rank vs Interpolation

**Date:** 2026-07-06
**Topic:** Two ways to pick the nth percentile from a sorted list

---

## Your Intuition Was Right

You said: "round up to 1 and use the lowest value." That's a legitimate method — it's called the **nearest rank** approach. And you correctly spotted the limitation: small samples make it coarse.

Here are the two conventions, side by side.

---

## Convention 1: Nearest Rank (What You Described)

**Rule:** Find the rank $$r = \lceil P \times n \rceil$$ (ceiling function — round up). Take the value at that rank.

For our 10 returns at the 5th percentile:
$$r = \lceil 0.05 \times 10 \rceil = \lceil 0.5 \rceil = 1$$

**Terms:**
- $P$ — percentile as a decimal (0.05 for 5th percentile)
- $n$ — number of observations in the sorted list
- $\lceil \cdot \rceil$ — ceiling function (round up to next integer)
- $r$ — rank/index in the sorted list (1-indexed)

**Result:** The 5th percentile = the worst return in the sample = −3.2%

**The problem you spotted:** With n = 10, the 5th and 10th percentiles would both be the worst observation. The 11th percentile would jump to the second-worst. It's coarse. This is purely a small-sample artifact.

---

## Convention 2: Linear Interpolation (What Most Production Systems Use)

**Rule:** Calculate the position $$i = P \times (n - 1)$$ (0-indexed). If $i$ isn't an integer, linearly interpolate between the two surrounding values.

For our 10 returns at the 5th percentile:
$$i = 0.05 \times (10 - 1) = 0.05 \times 9 = 0.45$$

**Terms:**
- $P$ — percentile as a decimal (0.05)
- $n$ — number of observations
- $i$ — fractional index (0-indexed, so 0 = worst, 9 = best)

Index 0.45 means: 45% of the way from the worst return (−3.2%) to the second-worst (−2.1%):

$$\text{VaR}_{95\%} = -3.2\% + 0.45 \times (-2.1\% - (-3.2\%))$$
$$= -3.2\% + 0.45 \times 1.1\%$$
$$= -3.2\% + 0.495\%$$
$$= -2.705\%$$

So the 95% VaR ≈ −2.71% under interpolation, vs −3.2% under nearest rank.

---

## Which One Matters?

| Convention | 10 days | 252 days | 1000 days |
|---|---|---|---|
| Nearest rank | −3.2% (coarse) | Still jumps between discrete days | Still discrete |
| Interpolation | −2.71% (smoother) | Smooth, between adjacent days | Nearly continuous |

**In practice:** With 252 trading days (1 year) or 504 days (2 years), the difference between the two conventions is tiny — you're interpolating a fraction of one day's return. Production systems (numpy, pandas, risk engines) use interpolation. But nearest rank is easier to explain to non-technical stakeholders: "the 13th worst day out of 252."

---

## The Real Insight (Don't Miss This)

The percentile convention is a footnote. **The assumption that the past 252 days represent the future is the real bet.**

Whether you interpolate or round up, both methods assume:
> The distribution of tomorrow's return will look like the distribution of the last N days.

When that assumption breaks, it doesn't matter which convention you used — your VaR is wrong. The 2008 crisis wasn't in the 2004-2007 sample. COVID wasn't in the 2018-2019 sample.

**The convention choice is precision. The sample choice is accuracy. Accuracy dominates.**

---

## Question For You

Given what you now know about both conventions:

**When you implement historical VaR, which convention would you use and why?** 

And more importantly: **What sample size (how many days) would you use, and what's the reasoning behind that choice?**
