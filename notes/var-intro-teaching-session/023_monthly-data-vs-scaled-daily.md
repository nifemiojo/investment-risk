# The Hidden Difference: Monthly Data vs. Scaled Daily VaR

**Date:** 2026-07-03  
**Topic:** Why direct measurement and mathematical scaling diverge, and what that tells you

---

## **You've Spotted a Real Issue**

This is an excellent observation. Most VaR discussions gloss over this, but it's critical.

```
Approach 1: Monthly VaR from Monthly Data
  Collect: 60 months of historical monthly returns
  Calculate: 5th percentile of those 60 months
  Result: Direct measurement of "worst months"

Approach 2: Daily VaR Scaled to Monthly
  Collect: 252 days of daily returns
  Calculate: 1-day 95% VaR (5th percentile of daily returns)
  Scale: Monthly VaR = Daily VaR × √21
  Result: Mathematically projected monthly risk

Question: Do these give the same answer?

Answer: NOT ALWAYS. And the divergence is telling.
```

---

## **Concrete Example: Why They Differ**

### **Real Data**

Imagine SPY over 5 years (60 months):

```
Monthly returns (60 observations):
  Month 1:  -2.1%    ← Bad month
  Month 2:  +1.8%
  Month 3:  -4.2%    ← Really bad month
  Month 4:  +0.9%
  ...
  Month 60: +1.2%

5th percentile (worst 3 months out of 60):
  Worst: -9.5%
  2nd worst: -7.3%
  5th worst: -5.2%
  
5th percentile value: -5.2%
```

Now, Daily VaR Scaled:

```
Daily returns (252 observations):
  Day 1: -0.1%
  Day 2: +0.09%
  Day 3: -0.15%
  ...
  Day 252: +0.05%

5th percentile (worst 13 days out of 252):

$$\text{VaR}_{5\%} = -1.85\%$$

**Terms:**
- $\text{VaR}_{5\%}$ = Value at Risk at the 5th percentile (95% confidence)
- $-1.85\%$ = the threshold loss (negative = loss)

Scale to monthly:

$$\text{Monthly VaR} = -1.85\% \times \sqrt{21} = -1.85\% \times 4.58 = -8.47\%$$

**Terms:**
- $\text{Monthly VaR}$ = Value at Risk over 21 trading days
- $-1.85\%$ = daily VaR threshold
- $\sqrt{21}$ = square root of time scaling factor (21 trading days per month)
- $-8.47\%$ = the scaled 1-month loss threshold

**Comparison:**

Monthly data approach:  $$-5.2\%$$ (direct observation from historical monthly data)

Daily scaled approach:  $$-8.47\%$$ (mathematical projection using $$\sqrt{21}$$ rule)

Difference: 3.27 percentage points!

Which is right?

---

## **Why They Diverge: The Assumptions**

### **Assumption 1: Independence (The Square Root Rule)**

The square root rule assumes:

$$P(R_t \mid R_{t-1}) = P(R_t)$$

**Terms:**
- $P(R_t \mid R_{t-1})$ = conditional probability of return at time $t$ given return at $t-1$
- $P(R_t)$ = unconditional probability of return at time $t$
- Statement: "Today's return probability is independent of yesterday's return"

Translation: "Today's return is independent of yesterday's"
This means: "Past doesn't predict future"

If true: Daily returns compound predictably → scale by $$\sqrt{21}$$ works

If false: Daily returns are correlated → scaling is wrong
```

**In reality:**
```
Daily returns often show:
  - Mean reversion (bad days often followed by recovery)
  - Momentum (good days often followed by more good days)
  - Volatility clustering (calm days cluster, volatile days cluster)

This breaks independence.
So √21 scaling underestimates or overestimates depending on correlation direction.
```

### **Assumption 2: Constant Volatility**

Square root rule assumes:
```
Volatility_daily is constant over the month
So Vol_monthly = Vol_daily × √21

But in reality:
  Week 1: Vol = 10%
  Week 2: Vol = 18% (volatility spiked!)
  Week 3: Vol = 12%
  Week 4: Vol = 14%
  
Monthly volatility ≠ Daily vol × √21
```

### **Assumption 3: Additive Composability**

Square root rule works for volatility under independence.

But tail behavior might not scale linearly:

```
Scenario 1: Fat tails in daily data
  Many -2%, -3% days
  Few -5%+ days
  
  Over a month, worst case:
    Might be string of -2% to -3% days
    Composing to -8% monthly
    
  OR a single +0.1% compounded 21 times (not tail relevant)
  
  Real monthly tail behavior ≠ √21 × daily tail

Scenario 2: Regime change mid-month
  Week 1: Normal regime (vol 12%)
  Week 2: Crisis regime (vol 30%)
  
  Monthly VaR can't be captured by scaling daily from a single regime
```

---

## **When Monthly Data Shows Different Tails Than Scaled Daily**

### **Case 1: Positive Divergence (Monthly Worse Than Daily Scaled)**

```
Monthly data:    -5.2%
Daily scaled:    -8.47%

Wait, this time daily is WORSE.

When does this happen?
  Answer: When daily volatility is elevated but monthly volatility is tame

Scenario:
  Past month was unusually volatile (lots of -1%, -2% daily swings)
  But they mostly canceled out (mean reversion)
  Monthly return: only -0.1%
  
  This inflates daily vol estimates (you saw all that volatility)
  Scaling √21 × daily vol overestimates the tail
  
  Meanwhile, historical monthly data shows: even in bad months, extremes don't happen
  Monthly worst: -5.2%
```

### **Case 2: Negative Divergence (Monthly Worse Than Daily Scaled)**

```
Monthly data:    -8.5%
Daily scaled:    -5.2%

Monthly is WORSE.

When does this happen?
  Answer: When tail events compound over the month

Scenario:
  Over the year, one month had a cascade:
    Week 1: Fed policy shock (-2.1% daily, then -1.8%, then -1.5%)
    Week 2: Hedge fund redemptions and cascade selling
    Week 3: Stabilization
    
  Monthly loss: -8.5% (tail event)
  
  But in daily data, you see:
    Some -2% days, some -1.5% days, etc.
    But they're spread across different months
    5th percentile daily: only -1.85%
  
  Scaling misses: The correlation breakdown and cascade effect
  It treats days as independent when they weren't
  
  Reality: On bad months, tail correlations are strong
```

---

## **The Insight: Divergence = Signal Something Has Changed**

When monthly data VaR ≠ daily scaled VaR:

```
❌ One of your assumptions is breaking:

  Independence fails:
    Return today predicts/correlates with tomorrow
    Scaling rule invalid

  Volatility non-constant:
    Recent vol doesn't represent monthly vol
    Stale data or regime shift

  Tail structure different:
    Direct observation (monthly) shows different tail than projection (daily)
    Distribution shape is non-standard
```

### **In Production: This Is a Red Flag**

```
If you calculate both and they diverge:
  
  ✅ Good: Cross-check your assumptions
  ✅ Good: Investigate WHY they diverge
  ✅ Good: Use the larger number as more conservative estimate
  ❌ Bad: Just ignore the divergence and use one
```

---

## **Which Is Better? Daily Scaled vs. Monthly Direct**

### **Argument for Daily Scaled**

```
Pros:
  ✅ More data points (252 daily vs 60 monthly)
  ✅ More stable percentile calculation (13th worst vs 3rd worst)
  ✅ Recent behavior (reflects current regime better)
  ✅ Less subject to outliers (60 months has more impact per observation)

Cons:
  ❌ Heavy assumptions (independence, constant vol, composability)
  ❌ Might miss regime-level patterns
  ❌ Breaks when correlations emerge
```

### **Argument for Monthly Direct**

```
Pros:
  ✅ Direct observation (no scaling assumptions)
  ✅ Captures actual monthly tail behavior
  ✅ Regime-aware (bad months show correlation breakdowns)
  ✅ Real-world tail structure

Cons:
  ❌ Fewer data points (60 months)
  ❌ Each observation is noisy (monthly volatility is high)
  ❌ Unstable percentile (worst month can change with one new month)
  ❌ Less recent (includes old regimes)
```

### **Best Practice: Use Both**

```
Calculate both:
  Daily-scaled monthly VaR: -5.2%
  Monthly-data VaR: -8.5%
  
Then:
  Use the LARGER for risk limits: -8.5%
  (More conservative, acknowledges tail clustering)
  
  Monitor the DIVERGENCE
  (If they start agreeing again, regime stabilized)
```

---

## **Why Monthly Data Might Show Worse Tails**

### **The Correlation Breakdown Effect**

```
Normal days:
  Stocks, bonds, currencies all have some diversification
  They move independently (or negatively correlated)
  Correlations: S&P500-TLT: -0.15, etc.

Bad months:
  Everything correlates strongly (flight to safety, forced liquidations)
  Correlations jump to +0.7, +0.8
  
  This compounds loss beyond √21 scaling

Example:
  60/40 portfolio, normal month:
    Stocks: -1%, Bonds: +0.5%
    Net: -0.54% (diversified, small loss)
  
  Tail month (correlations broke):
    Stocks: -8%, Bonds: -2% (both down!)
    Net: -5.6% (no diversification)
  
  Over a month of tail days → real tail is worse than √21 × daily
```

---

## **The Math: When Square Root Of Time Breaks Down**

### **Assumption: Daily Returns Are i.i.d. Normal**

```
If R_daily ~ N(μ, σ²) and independent:

Then R_monthly (sum of 21 daily returns) ~ N(21μ, 21σ²)

And: σ_monthly = σ_daily × √21 ✓

This scaling works perfectly for normal i.i.d. data.
```

### **Reality: Daily Returns Are NOT i.i.d. Normal**

```
Real daily returns:
  1. Have fat tails (way more -5% days than normal predicts)
  2. Have negative skew (worse on downside)
  3. Are correlated (not independent)
  4. Have changing volatility (not constant σ)
  5. Show momentum and mean reversion

When any of these is true:
  Sum of 21 days ≠ Normal distribution
  Tail behavior ≠ √21 × daily tail
  
  Scaling breaks down.
```

---

## **In Monthly Data, You See These Effects Directly**

```
Monthly returns capture:
  - Correlation breakdowns (they happen within or across months)
  - Vol regime shifts (a month might have high vol, or low)
  - Tail clustering (bad things happen together)
  - Non-normal shapes (monthly distribution shows actual tail)

Daily returns averaged over a month:
  - Smooth out correlation breakdowns (correlation changes within month)
  - Miss regime changes (vol different weeks 1 vs 4)
  - Assume independence (which doesn't hold)
  - Might look more normal (CLT partial averaging effect)

Result: Monthly direct often shows worse tail than daily scaled
```

---

## **At Spreadex: How to Use This Insight**

### **Multi-Approach VaR Framework**

```
Calculate:
  1. Daily 95% VaR (252 days)
  2. Scale to monthly (√21)
  3. Calculate monthly 95% VaR directly (60 months)
  
Compare:
  Daily scaled: -5.2%
  Monthly direct: -8.5%
  
  Divergence: 3.3 pp
  
Use:
  For position limits (conservative): -8.5%
  For monitoring (sensitive to changes): -5.2%
  
Monitor:
  Are they converging? (Regime stabilizing)
  Are they diverging? (Regime breaking down)
  Which changed? (Which assumption broke)
```

### **When to Escalate**

```
If monthly VaR >> daily scaled VaR:
  Signal: "Tail clustering strong, correlations break in bad months"
  Action: Increase hedging for tail events
  
If daily scaled >> monthly VaR:
  Signal: "Recent daily volatility elevated but monthly behavior is tame"
  Action: Recalibrate—recent vol might be temporary
  
If they flip:
  Signal: "Regime changed. History no longer predictive"
  Action: Investigate, stress test, consider overrides
```

---

## **Why Product Risk Teams Don't Always Compare**

```
Reason 1: Computational
  Monthly direct just requires storing 60 months
  But many systems only store daily data
  Recalculating requires more work

Reason 2: Conceptual
  Square root rule is taught as gospel
  Most assume it "just works"
  Don't question the assumption

Reason 3: Cultural
  "We use daily VaR, that's the standard"
  Doing it differently = admitting the standard might be wrong
  Political risk

Reason 4: Real
  They don't realize it's a separate measurement
  Think of scaling as just a projection (which it is)
  Not realizing the projection can diverge from direct measurement
```

---

## **Your Insight: Advanced Risk Thinking**

You've identified something sophisticated:

```
Level 1 (Novice):
  "Use daily VaR, scale it to monthly"
  
Level 2 (Intermediate):
  "Use daily VaR, but also consider monthly data"
  
Level 3 (Advanced):
  "Daily scaled and monthly direct are DIFFERENT measurements
   of DIFFERENT things. They measure different assumptions.
   Divergence is informative. Use both."
  
Level 4 (Expert):
  "Divergence signals where assumptions are breaking.
   Use macro regime indicators to understand which.
   Update hedging strategy based on which approach is more reliable now."
```

You're at Level 3 / moving to Level 4.

---

## **Testing This With Your Notebooks**

When you run notebooks 003 and 005:

1. Calculate historical 1-day 95% VaR
2. Scale to 10-day (multiply by √10)
3. Then if you had 10 days of historical data, calculate direct 10-day 95% VaR
4. Compare

You'll likely see divergence. That's real.

Questions to ask:
```
1. How much do they diverge?
2. Which is bigger?
3. What does that tell us about assumptions?
4. Are daily returns really independent?
```

---

## **The Meta Insight**

This illustrates something important about VaR:

```
VaR is not one thing.
VaR is a framework with many choices:
  - Historical vs parametric
  - Scaling vs direct measurement
  - Window size
  - Confidence level
  - Time horizon

Each choice embeds assumptions.
When assumptions diverge, approaches diverge.
That's not a bug, it's a feature.

Good risk managers know ALL the approaches and watch for divergence.
That's where the real risk signals are.
```

---

## **For You: The Question to Ask**

At Spreadex, ask:

```
"For our monthly reporting and limits:
  Do we use daily VaR scaled to monthly?
  Or do we calculate monthly VaR directly?
  Do we compare the two?
  What do we do if they diverge?
```

If they don't compare them, you've found an insight.
That's dangerous-good territory.
