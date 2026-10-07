# Percentiles Refresher for Historical VaR

**Date:** 2026-07-03  
**Topic:** What percentiles are and how they work for historical VaR

---

## **Percentiles: The Simple Definition**

A percentile is **a position in a sorted list** that tells you what percentage of items are below that point.

**Example with heights in a classroom:**

```
100 students, ranked shortest to tallest:

Position 1:   5'0"   ← 1st percentile (1% of people shorter, 99% taller)
Position 5:   5'2"   ← 5th percentile
Position 25:  5'6"   ← 25th percentile
Position 50:  5'10"  ← 50th percentile (MEDIAN - half above, half below)
Position 75:  6'0"   ← 75th percentile
Position 95:  6'3"   ← 95th percentile (95% of people shorter, 5% taller)
Position 100: 6'8"   ← 100th percentile (tallest)
```

**Key insight:** The percentile itself is just your position. The value at that position is what matters.

---

## **Connecting to Returns (This Is Where VaR Lives)**

Instead of heights, we have **daily returns** sorted worst to best.

### Example: 252 Trading Days of Returns

```
Day 1 return:    -8.2%   ← Worst day (1st percentile)
Day 2 return:    -4.1%
Day 3 return:    -3.5%
...
Day 13 return:   -1.85%  ← 5th percentile (5 days out of 100 worse than this)
Day 14 return:   -1.60%
...
Day 126 return:  +0.05%  ← 50th percentile (MEDIAN)
...
Day 252 return:  +6.7%   ← 100th percentile (best day)
```

---

## **How to Calculate a Percentile**

### The Formula (Conceptually)

```
Percentile position = (percentile / 100) × number_of_observations

Example: 5th percentile with 252 observations
Position = (5 / 100) × 252 = 0.05 × 252 = 12.6 ≈ 13th position
```

So the 5th percentile is approximately the **13th worst day** (out of 252).

### What This Means for VaR

```
95% confidence = we want the 5th percentile (worst 5% of days)
Calculation: 5% × 252 days = 12.6 ≈ 13 days

Sort 252 days worst to best.
Look at position 13 (the 13th worst day).
That's your VaR.

On 95% of days, returns are BETTER than this.
On 5% of days, returns are WORSE than this.
```

---

## **Concrete Example: Historical VaR Step-by-Step**

### Step 1: Collect 252 Days of Returns

```
Day 1:   -2.1%
Day 2:   +0.8%
Day 3:   -3.2%
Day 4:   +1.1%
... (248 more days)
Day 252: -0.5%
```

### Step 2: Sort From Worst to Best

```
Sorted (worst first):
Day X:   -8.2%    ← Position 1 (worst)
Day Y:   -4.1%    ← Position 2
Day Z:   -3.5%    ← Position 3
...
Day A:   -1.85%   ← Position 13 (5th percentile)
Day B:   -1.60%   ← Position 14
...
Day M:   +6.7%    ← Position 252 (best)
```

### Step 3: Find the 5th Percentile

```
95% confidence → Look at worst 5%
Worst 5% = 5% of 252 = 12.6 ≈ position 12-13

Pick position 13: -1.85%

This is your 95% VaR: -1.85%
```

### Step 4: Interpret

```
95% of 252 days (≈240 days) had returns BETTER than -1.85%
5% of 252 days (≈12 days) had returns WORSE than -1.85%
```

---

## **Key Percentiles for VaR**

### Common Confidence Levels

```
Confidence  Percentile    # Days Out of 252    Meaning
─────────   ──────────    ──────────────────    ─────────
90%         10th          ~25 days             Worst 10% of days
95%         5th           ~13 days             Worst 5% of days
99%         1st           ~2-3 days            Worst 1% of days
99.9%       0.1st         ~0.2 days (rare!)    Worst 0.1% of days
```

### What This Looks Like in Practice

```
If your 90% VaR = -1.2%, then:
  - 25 days out of 252, you lose more than 1.2%
  - 227 days, you lose less than 1.2%

If your 99% VaR = -3.5%, then:
  - 2-3 days out of 252, you lose more than 3.5%
  - 249-250 days, you lose less than 3.5%
```

---

## **The Percentile Calculation in Code**

### Numpy Example

```python
import numpy as np

returns = [-8.2, -4.1, -3.5, -2.1, -1.9, -1.85, -1.6, ...]  # 252 values

# 95% confidence = 5th percentile
var_95 = np.percentile(returns, 5)
# Result: -1.85%

# 99% confidence = 1st percentile
var_99 = np.percentile(returns, 1)
# Result: -3.50%

# 90% confidence = 10th percentile
var_90 = np.percentile(returns, 10)
# Result: -1.20%
```

### What numpy.percentile Does

```python
np.percentile(data, q)
  ├─ Takes your data
  ├─ Sorts it
  ├─ Finds the position: q% from the bottom
  └─ Returns the value at that position
```

---

## **Why Percentiles Work for Historical VaR**

Historical VaR is **empirical**, not theoretical.

It doesn't assume anything about the shape of the distribution. It just says:

```
"In my 252 days of data, the 5th percentile (5% worst days) 
had a return of -1.85%.

So if tomorrow draws from the same distribution, 
I expect 95% chance of not losing more than 1.85%."
```

---

## **Common Mistakes with Percentiles**

### Mistake 1: Confusing Percentile Position with Percentile Value

```
❌ Wrong: "The 5th percentile is position 5"
✅ Right: "The 5th percentile is the value at position 13 
          (which is 5% of 252 observations)"
```

### Mistake 2: Using the Wrong Direction

```
❌ Wrong: "95% VaR = 95th percentile" 
         (That's the best 95%, not worst)
✅ Right: "95% VaR = 5th percentile" 
         (That's the worst 5%, which is the boundary for 95% confidence)
```

### Mistake 3: Mixing Up Confidence vs. Percentile

```
95% confidence = 5th percentile
  (confidence counts UP from good)
  (percentile counts DOWN from bad)

99% confidence = 1st percentile
  (these are complements: 100% - 99% = 1%)
```

---

## **Visual: From Data to VaR**

```
Step 1: Your 252 daily returns
┌──────────────────────────────────┐
│ +0.5%, -2.1%, +1.2%, -3.2%, ... │ (unsorted)
└──────────────────────────────────┘

            ↓ SORT

Step 2: Same returns, sorted worst to best
┌──────────────────────────────────┐
│ -8.2%, -4.1%, -3.5%, -2.1%, ... │ (sorted)
└──────────────────────────────────┘
  ↑
  Position 1 (1st percentile)

            ↓ FIND 5TH PERCENTILE

Step 3: Position 13 (5% of 252)
┌──────────────────────────────────┐
│ -8.2%, -4.1%, -3.5%, ..., -1.85% │
│  1     2     3    ...      13    │ (positions)
└──────────────────────────────────┘
                            ↑
                   5th percentile = -1.85%

            ↓ THIS IS YOUR 95% VaR

Step 4: Interpretation
"95% of the time, returns are better than -1.85%
 5% of the time, returns are worse than -1.85%"
```

---

## **Quiz: Test Your Understanding**

### Q1: 252 trading days, you want 99% confidence VaR.
What percentile do you use?

```
Answer: 1st percentile
Because: 100% - 99% = 1%
So you look at the worst 1% of days
```

### Q2: Your 90% VaR (10th percentile) = -1.2%
How many days out of 252 had returns worse than -1.2%?

```
Answer: ~25 days
Because: 10% × 252 = 25.2
```

### Q3: Which is more conservative? 95% VaR or 99% VaR?

```
Answer: 99% VaR
Because: 99% confidence means you're looking deeper into the tail
99% VaR looks at only the worst 1% of days (further out)
vs 95% VaR looks at worst 5% of days
So 99% VaR is a bigger loss number (more conservative)
```

---

## **At Spreadex: Why This Matters**

When you see "95% daily VaR = $500k":

It means:
```
Out of 252 trading days in the data,
  - 240 days: losses ≤ $500k (95%)
  - 13 days: losses > $500k (5%)

So the system expects:
  - Most days, hedge triggers around $500k
  - Some days (roughly every 20 days), you might see worse
```

If you're only hedging at 95%, you're OK with 5% of days being rough.

If you want to be more conservative:
```
Switch to 99% VaR = $800k (roughly)
Now: 249 days ≤ $800k, only 3 days worse
Tighter hedge, less tail risk
```

---

## **Your Checklist: Percentiles**

- [ ] Percentile = position in a sorted list (as a %)
- [ ] 5th percentile = worst 5% (position 13 out of 252)
- [ ] 95% confidence = 5th percentile (they're complementary)
- [ ] np.percentile(data, 5) gives you the value at that position
- [ ] Historical VaR = just the percentile, no assumptions about shape

Ready to run notebook 003 and see this in action?
