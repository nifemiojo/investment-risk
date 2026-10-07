# The Underlying Data: How Time Horizon Determines What Data You Use

**Date:** 2026-07-03  
**Topic:** The data-horizon connection—what rolls into your VaR calculation depends crucially on your horizon choice

---

## **The Critical Link You Need to See**

Your time horizon determines **what data you feed into VaR**.

```
Choice of horizon:        → Determines data frequency:      → Affects calculation:

1-day VaR               → Daily returns (252/year)         → 252 observations
10-day VaR (direct)     → 10-day returns (not daily!)      → Fewer observations
1-month VaR (direct)    → Monthly returns (60/year)        → 60 observations

OR:

1-day VaR               → Daily returns (252/year)         → 252 observations
10-day VaR (scaled)     → [Scale 1-day by √10]            → Derived, not measured
1-month VaR (scaled)    → [Scale 1-day by √21]            → Derived, not measured
```

This difference is where confusion lives.

---

## **Approach 1: Historical Data Matching Horizon**

### **1-Day VaR from Daily Data**

```
Collect: 252 days of daily returns
  Day 1: +0.5%
  Day 2: -0.2%
  Day 3: +0.1%
  ...
  Day 252: -0.8%

Calculate percentile:
  Sort all 252 returns
  Find 5th percentile (worst ~13 days)
  That's your 1-day 95% VaR
  
Result: VaR based on actual 1-day price changes
Data: 252 observations
Quality: Good (lots of data)
```

### **10-Day VaR from 10-Day Data (Direct Measurement)**

```
Collect: 10-day rolling returns
  (Every 10 trading days, measure cumulative change)
  
  10-day 1: (Close_day10 - Close_day0) / Close_day0
  10-day 2: (Close_day20 - Close_day10) / Close_day10
  10-day 3: (Close_day30 - Close_day20) / Close_day20
  ...
  
From 252 daily returns:
  (252 ÷ 10) ≈ 25 ten-day periods
  
So you get: ~25 observations of 10-day returns

Calculate percentile:
  Sort 25 observations
  Find 5th percentile (worst ~1.25 observations)
  That's your 10-day 95% VaR
  
Result: VaR based on actual 10-day price changes
Data: 25 observations
Quality: Poor (very few data points, unstable estimate)
```

### **1-Month VaR from Monthly Data (Direct Measurement)**

```
Collect: Monthly returns
  (Every month-end, measure change from previous month-end)
  
  Month 1: (Close_end_month1 - Close_end_month0) / Close_end_month0
  Month 2: (Close_end_month2 - Close_end_month1) / Close_end_month1
  ...
  
From 5 years of data:
  60 monthly returns
  
Calculate percentile:
  Sort 60 observations
  Find 5th percentile (3rd worst month)
  That's your 1-month 95% VaR
  
Result: VaR based on actual monthly price changes
Data: 60 observations
Quality: Moderate (better than 10-day but still limited)
```

---

## **Approach 2: Scaled Data (The √T Method)**

### **1-Day VaR from Daily Data**

```
Same as above:
  Collect 252 daily returns
  Calculate 1-day VaR = 1.85%
```

### **10-Day VaR from Daily Data (Scaled)**

```
Start with: 1-day 95% VaR = 1.85%

Math assumption: Daily returns are i.i.d. (independent, identical)

Formula: VaR_10day = VaR_1day × √10

Calculation: 1.85% × √10 = 1.85% × 3.162 = 5.85%

Result: You DERIVED 10-day VaR from daily data
Data used: All 252 daily returns (indirectly)
Quality: Depends on assumption validity
```

### **1-Month VaR from Daily Data (Scaled)**

```
Start with: 1-day 95% VaR = 1.85%

Math assumption: Daily returns are i.i.d.

Formula: VaR_1month = VaR_1day × √21

Calculation: 1.85% × √21 = 1.85% × 4.583 = 8.48%

Result: You DERIVED 1-month VaR from daily data
Data used: All 252 daily returns
Quality: Depends on assumption validity (worse than 1-day)
```

---

## **The Fundamental Tradeoff: Data Frequency vs. Sample Size**

### **Table: What You Get With Each Choice**

| Horizon | Data Frequency | Sample Size | Calculation Type | Data Quality | Assumption Risk |
|---------|---|---|---|---|---|
| 1-day | Daily (252/yr) | 252 obs | Direct | Excellent | Low |
| 10-day | 10-day periods | ~25 obs | Direct | Poor | Low* |
| 10-day | Daily (scaled) | 252 obs | Derived | Good | High |
| 1-month | Monthly | 60 obs | Direct | Good | Low* |
| 1-month | Daily (scaled) | 252 obs | Derived | Good | High |

*Low statistical risk (can measure), but high model risk (measurement might be wrong)

---

## **What This Means in Practice**

### **Example: You're Choosing How to Calculate 10-Day VaR**

**Option A: Use 10-day data directly**

```
Pros:
  ✅ Direct measurement (no scaling assumptions)
  ✅ Captures real 10-day behavior
  ✅ Shows correlation/vol changes over 10 days
  ✅ If data shows tail clustering, you see it
  
Cons:
  ❌ Only 25 10-day observations (one per ~10 trading days)
  ❌ 5th percentile = "3rd worst 10-day period"
     Calculation unstable (one extreme month changes it)
  ❌ Old data mixed with new (5 years = multiple regimes)
  ❌ Fewer recent observations (data from 5 years ago is stale)
  
Example failure:
  If you had only 20 ten-day periods (4 years of data):
    5th percentile = "worst ~1 observation"
    Your estimate is basically: 1 number
    Not really a percentile anymore, just a worst case
```

**Option B: Scale daily VaR by √10**

```
Pros:
  ✅ Use all 252 daily observations
  ✅ Stable percentile estimate (13th out of 252)
  ✅ Recent data (just last year)
  ✅ Standard industry practice
  
Cons:
  ❌ Assumes daily returns are independent
  ❌ Assumes daily vol constant over 10 days
  ❌ Misses tail clustering (things that happen together)
  ❌ Wrong if correlations strengthen over 10 days
  
Example failure:
  2008 crisis: First 5 daily moves were normal magnitude
             6th day (Lehman): Everything correlates, massive move
             Can't scale daily to capture that cascade
 ```

---

## **The Sample Size Problem: Why It Matters**

### **The Precision Issue**

```
1-day VaR from 252 daily returns:
  5th percentile = position 13 (252 × 5% = 12.6)
  
  Interpretation: Strong.
                  "Position 13 is 13th out of 252
                   That's a solid percentile"

10-day VaR from 25 ten-day returns:
  5th percentile = position 1.25 (25 × 5% = 1.25)
  
  Interpretation: Shaky.
                  "Position 1.25 = roughly the worst observation"
                  This is not a percentile, it's basically the max
                  
  Problem: One new 10-day period with -9% return
           Your 5th percentile changes from -8% to -9%
           Your estimate is unstable
```

### **Illustration: How Sample Size Affects Stability**

```
Year 1: VaR estimates from 10-day data
  Observations: 25 ten-day periods
  5th percentile (worst 1.25): -7.2%

Add Year 2:
  Observations: 50 ten-day periods
  5th percentile (worst 2.5): -7.9%  ← Changed!
  
  Did the market change? Or was it just randomness?
  Hard to tell with N=50, especially at the tail

Compare to 1-day:
  
Year 1: VaR estimates from daily
  Observations: 252 daily returns
  5th percentile (worst 13): -1.85%

Add Year 2:
  Observations: 504 daily returns
  5th percentile (worst 25.2): -1.83%  ← Stable
  
  Much more stable, easier to tell if real change
```

---

## **Data Frequency Match: The Hidden Assumption**

### **The Principle**

```
Best practice: Data frequency should match horizon

1-day VaR    → Use daily data
10-day VaR   → Use 10-day data (or scale with caution)
1-month VaR  → Use monthly data

Why? Because that's where the actual risk lives.

Breaking this rule creates a gap between:
  What you're measuring (1-day daily swings)
  What you care about (10-day compounding)
```

### **What Happens If You Don't Match**

```
Scenario: You calculate 10-day VaR by scaling daily

Daily risk:    Many small swings, mean reversion, diversification
10-day risk:   Compounding + correlation breakdown + vol clustering

Daily VaR × √10 might:
  ✅ Be right if markets are normal
  ❌ Miss tail clustering (worse in crisis)
  ❌ Assume independence (breaks when correlations spike)
  
So daily-scaled 10-day VaR might be:
  - Too optimistic in crisis
  - Too pessimistic in normal times
  - Unstable at predicting actual 10-day behavior
```

---

## **Statistical Concept: The Data Frequency-Assumption Tradeoff**

### **More Data Points → Less Assumption Risk**

```
Using 252 daily observations:
  ✅ Can estimate 5th percentile reliably (13th position)
  ✅ Less subject to outliers (1 bad day doesn't dominate)
  ✅ Can detect recent changes (recalculate weekly)
  
  ❌ Have to assume: Daily compound to monthly correctly
  ❌ Have to assume: Independence holds
  ❌ Have to assume: Vol is constant
```

### **Fewer Data Points → More Model Risk**

```
Using 25 ten-day observations:
  ✅ Direct measurement (no scaling assumptions)
  ✅ See real 10-day tail behavior (correlation effects)
  ✅ Can't scale away the hard truth
  
  ❌ 5th percentile = "roughly the worst observation"
  ❌ One new data point changes everything
  ❌ Hard to detect regime changes (need 5+ years to see pattern)
```

---

## **Real Example: SPY Over 5 Years**

### **Daily VaR Calculation**

```
Collect: SPY daily returns, 2019-2024 (252 days × 5 = 1260 returns)

Worst days (sorted):
  1. -14.2% (March 2020 COVID crash)
  2. -9.5% (March 2020)
  3. -8.7% (March 2020)
  ...
  Position 63: -1.85%  (5th percentile)

1-day 95% VaR: -1.85%
```

### **10-Day VaR: Option A (Direct From 10-Day Data)**

```
Collect: SPY 10-day returns (every 10 days)

10-day periods: 1260 ÷ 10 = 126 periods

Worst periods (sorted):
  1. -42.1% (March 2020, 10-day cascade)
  2. -28.3% (March 2020)
  3. -19.5% (March 2020)
  ...
  Period 6: -7.5%  (5th percentile of 126)

10-day 95% VaR (direct): -7.5%
```

### **10-Day VaR: Option B (Scaled From Daily)**

Start: 1-day 95% VaR = -1.85%

$$\text{Scale: } -1.85\% \times \sqrt{10} = -1.85\% \times 3.162 = -5.85\%$$

**Terms:**
- $-1.85\%$ = 1-day VaR threshold
- $\sqrt{10}$ = square root of time scaling factor for 10 days
- $-5.85\%$ = resulting 10-day VaR (scaled)

$$\text{10-day 95\% VaR (scaled): } -5.85\%$$

### **Comparison**

Direct from 10-day data:  $$-7.5\%$$

**Terms:**
- Calculated directly from historical 10-day returns
- Captures actual market behavior over 10-day periods

Scaled from daily:        $$-5.85\%$$

**Terms:**
- Derived from daily VaR using $$\sqrt{10}$$ rule
- Assumes independence of daily returns

Difference: 1.65 percentage points!

Why?
  Direct captures: Correlation breakdown in March 2020
                   Cascade days where everything fell together
                   Real 10-day tail behavior
                   
  Scaled assumes: Daily independence
                  Daily compounding predictably
                  No special clusters
                  
In this case: Direct is worse (more conservative)
              Shows tail risk scaling up super-linearly
              √10 underestimates because correlations strengthen
```

---

## **How to Choose: Data vs. Scaling**

### **Use Direct Measurement When:**

```
✅ You have enough data
   (At least 50+ observations for that horizon)
   
✅ You care about real tail behavior
   (Not just theory, but what actually happens)
   
✅ You want to detect regime changes
   (See if tail structure evolving)
   
✅ You suspect correlations or vol non-constant
   (Direct measurement captures these)
   
Example: 1-month VaR from 5 years of monthly data (60 obs)
         Good enough to use direct
```

### **Use Scaled Approach When:**

```
✅ You don't have enough data at that horizon
   (E.g., 10-day: only 25 obs = too few)
   
✅ You trust the independence assumption
   (Normal market, not crisis)
   
✅ You need stability
   (Daily has 252 obs, scaled is stable)
   
✅ You want recent focus
   (Scaling from daily captures recent regime)
   
Example: 10-day VaR from daily, in normal market
         Scaling is practical
```

---

## **The Hidden Risk: Mixing Data Frequencies**

### **What NOT to Do**

```
❌ Calculate daily VaR from monthly data
   "Use monthly returns to get daily VaR"
   
   Problem: Monthly data includes 21 trading days
            Can't back out what happens daily
            Loss of information
            
   Example: Monthly return: -2%
            Daily breakdown: Maybe -0.1%, -0.1%, -0.05%, ...
            Or maybe: -1.9%, +0.1%, -0.1%, ...
            Can't tell from the monthly number

❌ Calculate 10-day VaR from daily data without scaling
   "Just take worst 10 consecutive days"
   
   Problem: Not a percentile
            Just the worst case
            (What if next 10 days are worse?)
            
   Better: Scale daily VaR, or collect actual 10-day data

❌ Calculate 1-month VaR from quarterly data
   "Divide quarterly return by 3"
   
   Problem: Loses intra-month structure
            Compounding not linear
            Correlations vary within quarter
```

---

## **At Spreadex: Data-Horizon Alignment Questions**

When you see VaR:

```
1. What time horizon is this? (1-day? 10-day? 1-month?)

2. What underlying data is used?
   Daily returns? Monthly? 10-day?
   
3. How much data?
   252 daily observations? 60 monthly? 25 ten-day?
   
4. If scaled: What's the scaling assumption?
   √T rule? Assumes independence?
   Have they validated it?
   
5. Do they calculate both scaled and direct?
   Or just one approach?
   If they diverge, investigate why.
   
6. Is the data current?
   Last year? Last 5 years?
   Does recent regime look like historical?
```

---

## **Building Your Understanding: Data-Horizon Connection**

### **The Map**

```
Your horizon choice
    ↓
Determines data frequency
    ↓
Affects sample size
    ↓
Determines calculation stability
    ↓
Determines assumption risk
    ↓
Affects how reliable your VaR is
```

### **Examples**

```
You want: 1-day VaR
Data: 252 daily returns
Sample: Excellent (252 obs)
Calc: Direct percentile
Stability: Excellent
Assumptions: Minimal

You want: 10-day VaR (direct approach)
Data: 10-day returns (rolling)
Sample: Poor (25 obs)
Calc: Direct percentile
Stability: Poor (unstable)
Assumptions: Direct (good)

You want: 10-day VaR (scaled approach)
Data: 252 daily returns
Sample: Excellent (252 obs)
Calc: Derived (×√10)
Stability: Good
Assumptions: Heavy (independence, constant vol)

You want: 1-month VaR
Data: 60 monthly returns (5 years)
Sample: Adequate (60 obs)
Calc: Direct percentile
Stability: Moderate
Assumptions: Minimal
```

---

## **Your Data-Horizon Checklist**

- [ ] Time horizon determines data frequency
- [ ] More data points = more stable percentile but stronger assumptions
- [ ] Fewer data points = direct measurement but unstable estimates
- [ ] Daily data + scaled = hundreds of observations, good for 1-day, risky for 10-day+
- [ ] Monthly data = limited observations (60/decade), direct but slow to detect changes
- [ ] Direct measurement (from actual 10-day/monthly data) shows real tail behavior
- [ ] Scaling assumes independence and constant vol (often breaks in crises)
- [ ] When direct and scaled diverge, it's a signal assumptions are breaking
- [ ] Sample size at 5th percentile with 25 obs = basically the worst observation (unstable)
- [ ] Sample size at 5th percentile with 252 obs = 13th worst (stable)

---

## **Next: Connecting Data, Horizon, and Confidence**

Now you understand:
- ✅ Time horizon = rehedging period
- ✅ Horizon determines data frequency
- ✅ Data frequency affects sample size and stability
- ✅ Sample size affects calculation reliability
- ✅ Assumptions differ (direct vs. scaled)

Next: How confidence level interacts with all of this

```
Why 95% confidence? Why not 99%?
What does confidence mean given your data size?

With 252 observations:
  5th percentile = position 13 (reliable)
  1st percentile = position ~2.5 (shaky)
  
With 60 observations:
  5th percentile = position 3 (shaky)
  1st percentile = position 0.6??? (impossible)
  
This matters. Ready?
```
