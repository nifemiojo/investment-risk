# Historical VaR: The Core Idea

**Date:** 2026-07-06
**Topic:** Historical VaR calculation — what it is, how it works, first concrete example

---

## Starting Point: What You Already Know

From your VaR foundations work, you understand that VaR at 95% confidence with a 1-day horizon answers:

> "What loss threshold will be exceeded on only 5% of days?"

You also know the four components:
1. **The Loss** — what exactly is being measured
2. **Time Horizon** — the rehedging period
3. **Underlying Data** — what sample, how big
4. **Model Assumption** — stationarity (the past distribution ≈ the future distribution)

---

## The Historical VaR Method in One Sentence

**Historical VaR answers the question by literally looking at what happened in the past, sorting those outcomes from worst to best, and reading off the threshold at the desired percentile.**

No formulas. No distribution assumptions. No parameters to estimate.

You take the last N days of returns, sort them, and the 5th percentile *is* your 95% VaR.

---

## Concrete Example — Before We Define Anything

Let me give you a toy example with real numbers. This is the entire method.

**Setup:** You hold a position in SPY. You have the last 10 daily returns (in %):

```
Day 1:  +1.2%
Day 2:  -0.8%
Day 3:  +0.3%
Day 4:  -2.1%
Day 5:  +0.5%
Day 6:  -1.5%
Day 7:  +2.0%
Day 8:  -0.3%
Day 9:  -3.2%   ← worst day
Day 10: +0.7%
```

**Step 1:** Sort from worst to best:
```
-3.2%, -2.1%, -1.5%, -0.8%, -0.3%, +0.3%, +0.5%, +0.7%, +1.2%, +2.0%
```

**Step 2:** Find the 5th percentile (for 95% VaR with 10 days):
$$5\% \times 10 = 0.5 \text{ — wait, that doesn't make sense}$$

---

## Pause — Here's Where the Haziness Usually Starts

There are actually two common ways to pick the percentile from a sorted list. Let me pause and ask:

**Before I show you both methods — when I said "sort the returns and take the 5th percentile," what did you picture in your head?** 

What exact calculation did you imagine doing to find that number from the sorted list above?
