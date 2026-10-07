# Component 4: The Model Assumption — The Foundation Under Everything

**Date:** 2026-07-03  
**Topic:** The stationarity assumption—why it's the bedrock of VaR, when it holds, when it shatters

---

## **The Model Assumption: One Sentence**

"The distribution of returns tomorrow will resemble the distribution from the past 252 days"

Technical term: Statistical stationarity

Formally:

$$F(R_t) = F(R_{t+1}) = F(R_{t+h})$$

**Terms:**
- $F(R_t)$ = probability distribution of returns at time $t$
- $F(R_{t+1})$ = probability distribution of returns at time $t+1$
- $F(R_{t+h})$ = probability distribution of returns at time $t+h$ (h periods ahead)
- Equality means: All distributions are identical
- This is **stationarity**: "The shape doesn't change over time"

Translation: "The probability distribution is constant over time"

This single assumption is **everything**. When it breaks, VaR breaks.

---

## **Why Do We Need This Assumption?**

### **The Logical Chain**

```
Step 1: We observe data
  "Past 252 days showed losses between -8.2% and +6.7%"
  
Step 2: We measure a percentile
  "The 5th percentile was -1.85%"
  
Step 3: We want to make a prediction
  "Tomorrow, 5% chance of exceeding -1.85% loss"

Step 4: Here's where we need the assumption
  "To say tomorrow resembles the past,
   we MUST assume the distribution is the same"

Without this assumption:
  Why would past percentiles predict the future?
  No logical reason.
  
With this assumption:
  "If tomorrow draws from the same distribution,
   then past percentiles are a guide to future percentiles"
```

### **The Gap It Bridges**

```
Sample statistic (what we have):
  "Past 252 days: 5% exceeded -1.85%"

Probabilistic prediction (what we want):
  "Tomorrow: 5% chance of exceeding -1.85%"

The assumption that bridges them:
  "The distribution is stationary"
  
If true: Sample stat predicts well
If false: Sample stat is useless
```

---

## **What the Assumption Covers (Stationarity Implies)**

### **Mean Return Constancy**

```
Past: Average daily return = +0.04% / day
Assumption: Tomorrow's expected return = +0.04% / day
Reality check: True in normal markets, false in bear markets
```

### **Volatility Constancy**

```
Past: Daily volatility = 1.2% (std dev of returns)
Assumption: Tomorrow's volatility = 1.2%
Reality check: False! Vol clustering means high vol days cluster

Example:
  Week 1: Vol = 10%
  Week 2: Vol = 18% (cluster of volatile days)
  Assumption says: Vol = constant
  Reality: Vol regimes shift constantly
```

### **Tail Shape Constancy**

```
Past: 5% tail shows losses -1.85% to -8.2%
Assumption: Future 5% tail will be same shape, same range
Reality check: False! Tails can be much fatter in crises

2020 COVID example:
  Past 252 days: Worst day = -3.2%
  Assumption: Can't see worse than -3.2%
  Reality: March 16, 2020 = -12.4% (4x worse)
```

### **Correlation Constancy**

```
Past: SPY-BND correlation = -0.15 (diversified)
Assumption: Tomorrow's correlation = -0.15
Reality check: False! Correlations break in crises

2008 example:
  Past: SPY-BND corr = -0.2 (safe diversification)
  Crisis: SPY-BND corr = +0.6 (everything falls together)
  Result: 60/40 portfolio much riskier than VaR predicted
```

### **Distribution Shape Constancy**

```
Past: Returns look roughly normal (bell curve)
Assumption: Future returns will be normal
Reality check: False! Real returns have fat tails

Evidence:
  Normal distribution: -5% day happens once per 4,000 years
  Reality: -5% days happen every few years
  
  Implication: Distribution is not normal (has fatter tails)
  VaR using normal assumption is wrong
```

---

## **When the Assumption Holds**

### **Scenario: Normal Market, Stable Regime**

```
Past 252 days:
  Vol: ~12%
  Mean: +0.04%/day
  Max loss: -3.2%
  Correlations: Stable
  Distribution: Roughly normal

Next 252 days (similar regime):
  Vol: ~13%  ✓ Similar
  Mean: +0.05%/day  ✓ Similar
  Max loss: -3.5%  ✓ Similar
  Correlations: Stable  ✓ Similar
  Distribution: Roughly normal  ✓ Similar

Result: Assumption holds!
VaR prediction works.
Historical percentile ≈ Future percentile
```

### **Real-World Example: 2016-2019**

```
2016-2019 were calm years
  Vol: 12-15%
  Correlations: Steady
  No crises, no shocks
  Distribution: Relatively stable

If you calculated VaR on 2016-2019 data,
it predicted 2019 well because regime didn't change.

Assumption held: ✓
```

---

## **When the Assumption Breaks**

### **Scenario 1: Volatility Regime Shift**

```
Past 252 days (before crisis):
  Vol: 12%
  5th percentile loss: -1.85%

Crisis hits:
  Vol: 35% (3x higher!)
  
  What SHOULD 5th percentile be if vol is 35%?
  Roughly: -1.85% × (35% / 12%) ≈ -5.4%

What did your VaR predict?
  -1.85% (based on 12% vol)

Reality:
  On bad days in crisis, losses hit -5.4%+
  Your VaR = -1.85%
  You're underestimating risk by 3x!
  
Assumption broken: Volatility changed
Result: VaR failed spectacularly
```

**Real example: 2020 COVID**

```
Feb 28: 1-day VaR = ~1.8%
Mar 16: Actual loss = -12.4%

Your VaR said: "Don't worry, maybe -1.8%"
Reality: -12.4%
Ratio: 6.9x worse!

What happened? Vol went from 14% to 42%
Assumption broken.
```

### **Scenario 2: Correlation Breakdown**

```
Past 252 days:
  60/40 stock/bond portfolio
  SPY: -1% day
  BND: +0.5% day (offsetting!)
  Net: -0.54% (diversified)
  
  Correlation: -0.15 (bonds hedge stocks)

Crisis day:
  SPY: -8%
  BND: -2% (bonds NOT hedging!)
  Net: -5.6% (no diversification!)
  
  Correlation: +0.7 (everything down!)

Your VaR predicted:
  "Diversification works, worst case -2%"
  
Reality:
  Correlation broke, actual loss: -5.6%
  You thought 60/40 was safe.
  It wasn't.

Assumption broken: Correlation changed
Result: Diversification myth exposed
```

**Real example: 2008 Financial Crisis**

```
Normal times: Stocks and bonds negatively correlated
             Diversification works

September 2008 (Lehman collapse): Stocks AND bonds fell together
                                   Correlation flipped positive
                                   60/40 wasn't safe
```

### **Scenario 3: Tail Structure Change (Fat Tails Emerge)**

```
Past 252 days:
  Worst day: -4%
  Distribution: Roughly normal
  5th percentile: -1.85%

What your VaR assumes:
  "Tails follow normal distribution
   Probability of -10% day = basically zero"

Tomorrow (crisis):
  -12% day happens
  -15% day happens next week
  Tails are FAT (much fatter than normal)

Your VaR said: "Can't happen"
Reality: Happened

Assumption broken: Tail shape changed
                  (or was always fat, normal assumption was wrong)
Result: VaR blindsided
```

**Real example: 1987 Black Monday**

```
October 19, 1987: S&P down -22% in 1 day

Historical VaR from pre-1987 data: ~-2% to -3%
Actual: -22%

The tail model broke completely.
Market showed a tail structure no one predicted.
```

### **Scenario 4: Regime Change (Bull → Bear)**

```
Past 252 days (bull market):
  Mean: +0.08%/day
  Vol: 12%
  Drawdowns: Shallow (-2-3% quarterly)
  Correlation: Negative (diversification works)
  Distribution: Right skew (more gains than losses)

New regime (bear market):
  Mean: -0.05%/day
  Vol: 18%
  Drawdowns: Steep (-10%+ annually)
  Correlation: Positive (no diversification)
  Distribution: Left skew (more losses than gains)

Your VaR predicted: Based on bull data
Reality: Bear behavior

Assumption broken: EVERYTHING changed
Result: All predictions useless
```

**Real example: 2000-2002 (NASDAQ bear) and 2008 (broad bear)**

```
If you calculated VaR using 1998-1999 data (super bull),
predictions for 2000-2002 would be catastrophically wrong.

Distribution fundamentally changed.
```

---

## **How to Detect When Assumption Is Breaking**

### **Signal 1: Rolling Volatility Spike**

```
Monitor daily:
  30-day rolling vol
  60-day rolling vol
  
If today's vol is 2x yesterday's rolling vol:
  Signal: "Regime changing"
  
Action: Recalculate VaR
        Watch for bigger moves
        Tighten hedges
```

### **Signal 2: Historical vs. Parametric Divergence**

```
Calculate both:
  Historical 95% VaR: (percentile from past data, no assumptions)
  Parametric 95% VaR: (assuming normal distribution + current vol)

Normal times:
  Both are similar (roughly within 5%)
  
Crisis emerging:
  Historical: -2%
  Parametric: -3.5%
  
  Divergence > 1.5pp = signal
  Parametric seeing fatter tails (normal assumption being violated)
```

### **Signal 3: Realized Loss Exceeds VaR**

```
VaR says: "5% of days, loss > $500k"

Monitor:
  Are bad days happening at 5% frequency? Or more?
  
If more than 5% of days exceed VaR:
  Signal: "Distribution shifted, VaR is stale"
  
Backtest result:
  Expected: 5% of days exceed (roughly 13/252)
  Actual: 8% of days exceed (20/252)
  
  This is statistically significant — distribution changed
```

### **Signal 4: Correlation Change**

```
Monitor correlation matrix daily:
  SPY-BND: Was -0.15, now -0.05? Weakening
  SPY-AGG: Was +0.2, now +0.6? Strengthening
  
  If any correlation changes >0.3:
  Signal: "Regime shifting, correlation breakdown risk"
```

### **Signal 5: Extreme Day (Tail Event Outside Historical Range)**

```
Your data: Worst day was -4%
Today: -8% day happens

Signal: IMMEDIATE ESCALATION
  Distribution clearly changed
  Historical data no longer representative
  Need emergency stress testing
  Override VaR with manual limits
```

### **Signal 6: Market Events / Exogenous Shocks**

```
Watch for:
  - Central bank policy change
  - Geopolitical crisis
  - Pandemic announcement
  - Major bankruptcy/default
  - Regulatory shock
  - Sanctions
  
When these happen:
  Distribution WILL change
  Don't wait for the data to show it
  Assume assumption is breaking
```

---

## **Different Models, Different Assumptions**

### **Historical VaR Model**

```
Assumption:
  "Tomorrow's distribution = distribution of past 252 days"
  
Specifically assumes:
  ✓ Mean is stable
  ✓ Volatility is stable  
  ✓ Tail structure is stable
  ✓ Correlations are stable
  
Fails when:
  ❌ Vol spikes
  ❌ Correlations break
  ❌ Regime changes
  ❌ New worst-case appears
```

### **Parametric (Normal) VaR Model**

```
Assumption 1: Distribution is normal (bell curve)
Assumption 2: Vol is current measured vol
Assumption 3: Vol stays constant

Specifically assumes:
  ✓ -1% and +1% days are equally likely
  ✓ Tails are symmetric
  ✓ -5% days are extremely rare
  ✓ All risk captured by mean + vol

Fails when:
  ❌ Returns have fat tails (real markets)
  ❌ Negative skew (losses more common than gains)
  ❌ Vol clustering (vol isn't constant)
  
Advantage: Can extrapolate beyond data range
          (Normal curve extends infinitely)
Disadvantage: Very wrong about tail
             Normal assumes -5% every 4,000 years
             Reality: happens every few years
```

### **Exponentially Weighted VaR (EWMA)**

```
Assumption:
  "Recent data matters more than old data"
  (Vol weight decays, older observations count less)
  
Specifically assumes:
  ✓ Recent vol is more predictive
  ✓ Regime changes are captured faster
  ✓ Old crisis data shouldn't dominate
  
Fails when:
  ❌ Regime is stable (averaging nearby and far past)
  ❌ Need historical crises (throws away old data)
  ❌ Smooth drift (weights can oscillate)
```

---

## **The Implication: VaR Is Only as Good as Its Assumption**

### **The Hierarchy of Assumption Robustness**

```
Weakest assumption:
  Historical VaR
  "Forever and always, whatever happened before will happen again"
  Fails instantly when regime changes

Stronger assumption:
  EWMA VaR
  "Recent behavior predicts near future"
  Better at adapting, still breaks in true crises

Strongest mathematical assumption:
  Parametric VaR (normal)
  "Returns are normal, all captured by mean and vol"
  Most extrapolative but most wrong about real tails

Reality check:
  None of them hold during shocks
  All assume some form of persistence
  All break when distribution changes
```

---

## **At Spreadex: What to Challenge**

When you see VaR:

```
Question 1: What model is used? (Historical? Parametric?)

Question 2: What assumptions does it embed?

Question 3: When was the last time you questioned the assumption?
           "Have you checked if vol is still 12%?
            Or did it change to 18%?"

Question 4: What's your monitoring process?
           "How do you detect assumption failure?
            What's the early warning?"

Question 5: What's the override procedure?
           "When the model fails (and it will),
            what replaces VaR?"
```

If they can't answer these clearly, they don't understand their own risk system.

---

## **Building Your Intuition: The Assumption Test**

### **Test 1: When Should You Trust VaR?**

```
Condition: Market is calm, vol has been 12% for 6 months
           No major news
           Correlations stable
           Returns look normal

Assumption check:
  Is tomorrow likely to be like the past 252 days?
  YES
  
VaR reliability: HIGH
Action: Use VaR for decisions

---

Condition: Fed just announced rate shock
           Vol spiked from 12% to 25% this week
           Correlations jumping around
           
Assumption check:
  Is tomorrow likely to be like the past 252 days?
  NO
  
VaR reliability: LOW
Action: Override VaR, use stress testing instead
```

### **Test 2: Which Signal Matters Most?**

```
Scenario A: Rolling vol rose from 12% to 13%
            Historical vs parametric diverge by 0.5%
            
Signal strength: Weak
Action: Monitor but don't panic

Scenario B: Rolling vol rose from 12% to 30%
            Historical vs parametric diverge by 3%
            Realized losses exceed VaR 10% of days
            
Signal strength: STRONG
Action: Escalate immediately, override limits

Scenario C: Market gaped down 10% at open
            Your worst day from historical data: -4%
            
Signal strength: IMMEDIATE/EXTREME
Action: EMERGENCY response, all bets off
```

---

## **Your VaR Definition: Adding the Assumption**

### **Complete Version**

> "VaR is a threshold loss at a specified confidence level (e.g., 95%) 
> over a specified time horizon (e.g., 1 day), calculated from historical 
> or parametric data.
>
> **THE CORE ASSUMPTION: The future distribution of returns will resemble 
> the past distribution (statistical stationarity).**
>
> This means: Volatility stays constant, correlations hold, tail structure 
> persists, mean return is stable.
>
> **When this assumption holds** (normal markets, stable regime):
> VaR is useful for estimating next period's risk.
>
> **When this assumption breaks** (vol spikes, correlations shift, regime change):
> VaR becomes stale and dangerous. Realized losses can exceed VaR by 10x.
>
> **Detection:** Monitor rolling volatility, historical vs parametric divergence, 
> realized loss frequency, correlations, exogenous shocks.
>
> **Action:** When assumption breaking, override VaR with stress tests 
> and manual limits."

---

## **The Meta-Level Insight**

```
VaR is not a scientific law.
VaR is an engineering tool.

It's useful when:
  ✓ Assumptions hold
  ✓ You monitor the assumptions
  ✓ You override when they break

It's dangerous when:
  ❌ You treat it as law ("VaR won't breach")
  ❌ You ignore assumption monitoring ("VaR is always right")
  ❌ You don't have override procedures ("Model rules everything")
  
The best risk managers know exactly when VaR will fail.
They prepare for it.
```

---

## **Your Component 4 Checklist**

- [ ] The core assumption is stationarity (distribution doesn't change)
- [ ] This assumption is what allows past percentiles to predict future
- [ ] It covers: mean, vol, tail shape, correlations, distribution shape
- [ ] It holds in stable regimes, breaks in crises
- [ ] You can detect breaking assumptions via: rolling vol, historical/parametric divergence, realized loss frequency, correlation changes, exogenous shocks
- [ ] Historical VaR weakest (breaks instantly on regime change)
- [ ] Parametric VaR strongest mathematical (but wrong about tails)
- [ ] EWMA VaR intermediate (faster to adapt)
- [ ] When assumption breaks, VaR can be 10x wrong
- [ ] Good practices: monitor, override, stress test, have backup procedures

---

## **Next: Confidence Level (Component 3)**

You've now mastered:
- ✅ Time horizon (rehedging period)
- ✅ Underlying data (data frequency + sample size)
- ✅ Model assumption (stationarity + when it breaks)

Missing:
- ⚠️ Confidence level (95% vs 99%? What does it mean given your data?)

Ready to explore why 95% and what happens at 99%?
