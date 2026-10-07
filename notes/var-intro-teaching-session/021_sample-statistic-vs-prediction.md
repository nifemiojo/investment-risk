# The Tension: Sample Statistic vs. Probabilistic Prediction

**Date:** 2026-07-03  
**Topic:** Bridging the gap between what we measure and what we predict

---

## **The Core Tension You've Identified**

VaR is fundamentally both:

```
WHAT IT IS:  Sample statistic (derived from past data)
             "In 252 days, the 5th percentile loss was 1.85%"

WHAT WE USE IT FOR:  Probabilistic prediction (about the future)
                     "Tomorrow, there's a 5% chance of exceeding 1.85% loss"

Tension:  How do we go from "what happened" to "what will happen"?
          What connects the two?
```

This is the critical gap that breaks down when distributions change.

---

## **The Implicit Bridge: The Key Assumption**

### **What Connects Sample to Prediction**

```
Historical observation:
  "Last 252 days: 5% of outcomes exceeded 1.85% loss"

To make a prediction:
  "Tomorrow: 5% probability of exceeding 1.85% loss"

The bridge (implicit assumption):
  "The future will draw from the same distribution as the past"

In technical terms:
  Distribution(past) = Distribution(future)
  
Or:
  Tomorrow's return ~ Distribution_estimated_from_past_252_days
```

**This assumption is everything.**

When it holds → VaR is useful  
When it breaks → VaR is dangerous

---

## **Framing That Captures This Tension**

### **Option 1: The Two-Step Frame**

> "VaR is a sample statistic (5th percentile from 252 days of data) 
> used as a probabilistic prediction (5% risk tomorrow) 
> under the assumption that tomorrow draws from the same distribution as the past."

**Pros:**
- Explicitly names the assumption
- Shows both the measurement and the prediction
- Clear where it can break

**Cons:**
- Longer
- Sounds technical

---

### **Option 2: The Process Frame**

> "VaR translates what we observed into what we expect:
> 
> OBSERVE: In past 252 days, 5% of daily returns exceeded -1.85%
> 
> ASSUME: Tomorrow draws from the same distribution
> 
> PREDICT: Therefore, tomorrow has ~5% chance of exceeding -1.85%"

**Pros:**
- Shows the three-step process clearly
- Each step is separate and visible
- Makes the assumption testable ("does tomorrow look like past?")

**Cons:**
- More verbose

---

### **Option 3: The Conditional Frame**

> "VaR is a **conditional probability statement**:
> 
> P(Loss_tomorrow > VaR | Distribution_unchanged) = 5%
> 
> The prediction is only valid if the distribution assumption holds."

**Pros:**
- Precise statistical language
- Makes clear: prediction depends on condition
- Emphasizes where to monitor

**Cons:**
- Very technical
- Not for traders or clients

---

### **Option 4: The Honest Frame (Best for Production)**

> "VaR is a historical measurement with a forward-looking assumption:
> 
> We measured: On 95% of past days, losses ≤ 1.85%
> 
> We assume: Tomorrow is like the past
> 
> We predict: On 95% of tomorrow-like days, losses ≤ 1.85%
> 
> Key risk: If tomorrow is NOT like the past, this prediction is wrong.
> This is why we monitor for distribution changes."

**Pros:**
- Professional and honest
- Shows measurement, assumption, prediction separately
- Includes risk monitoring
- Works for risk committees, boards

**Cons:**
- Longer

---

## **Understanding the Bridge in Detail**

### **The Assumption Is Statistical Stationarity**

```
Technical term: "Statistical stationarity"

What it means: The distribution of returns is constant over time

Formally:
  Distribution_t = Distribution_t+1 = Distribution_t+n
  
  (The distribution today = distribution tomorrow = distribution next month)

Why this matters for VaR:
  If distribution is stationary:
    5th percentile from past 252 days ≈ 5th percentile tomorrow
    So VaR derived from past has predictive power
  
  If distribution shifts:
    5th percentile yesterday ≠ 5th percentile tomorrow
    VaR breaks
```

---

### **When This Assumption Holds**

```
Scenario: Normal market, stable regime

Past 252 days:
  Vol: 12%
  Mean return: +0.04%/day
  Worst day: -3.5%
  5th percentile: -1.85%

Next 252 days:
  Vol: 11.8%  ← Similar
  Mean return: +0.05%/day  ← Similar
  Worst day: -3.3%  ← Similar
  5th percentile: -1.82%  ← Similar

VaR prediction:
  "5% chance of exceeding 1.85% loss"
  
Reality:
  "In next 252 days, 5.1% of days exceeded 1.85% loss"
  
Result: VaR worked! Prediction matched reality.
```

---

### **When This Assumption Breaks**

```
Scenario: Regime change (bull → bear)

Past 252 days (bull market):
  Vol: 12%
  Mean: +0.08%/day
  5th percentile: -1.85%

Next 252 days (bear market):
  Vol: 22%  ← 2x higher!
  Mean: -0.05%/day  ← Flipped!
  5th percentile: -3.50%  ← Way worse!

VaR prediction:
  "5% chance of exceeding 1.85% loss"
  
Reality:
  "In next 252 days, 15% of days exceeded 1.85% loss!"
  (Distribution shifted, prediction was way off)
  
Result: VaR failed. The assumption broke.
```

---

## **Why This Tension Matters**

### **The Philosophical Problem**

```
Question: Can we ever predict the future from the past?

Answer: Only if the structure doesn't change.

VaR assumes: "Structure doesn't change"

But markets have structural breaks:
  - Regime changes (bull ↔ bear)
  - Correlation breakdowns (diversifiers correlate)
  - Volatility regimes (calm → crisis)
  - New policies (central bank action)
  - Black swans (pandemics, wars, crashes)

So VaR's assumption is optimistic.
```

---

## **Ways to Frame This Tension for Different Audiences**

### **For Yourself / In Notes**

```
"95% daily VaR = 1.85% loss

This is:
  Sample statistic: 5th percentile from 252 past days
  
Used as:
  Probabilistic prediction: 5% chance of exceeding 1.85% tomorrow
  
Under assumption:
  Distribution(past) = Distribution(future)
  
Works when: Normal, stable regime
Breaks when: Vol spikes, correlation shifts, regime changes
Monitor by: Historical vs parametric divergence, rolling vol changes"
```

---

### **For Your Boss / Risk Committee**

```
"Our value at risk is $500k (95% daily).

This measures our historical tail risk (based on past performance).
We use it to predict tomorrow's risk (assuming markets behave similarly).

This works well in normal times. 
But when markets shift—new regimes, vol spikes, correlation changes—
our historical VaR becomes stale.

That's why we:
  1. Recalculate VaR weekly (watch for changes)
  2. Compare historical vs parametric VaR (signal when distribution shifts)
  3. Monitor rolling volatility (flag regime breaks)
  4. Have backup hedges beyond VaR (for when prediction fails)
  5. Conduct quarterly stress tests (test outside historical range)"
```

---

### **For Traders**

```
"Your $500k VaR limit is based on recent market history.
On most days, you'll be well inside this.
On ~5% of days, you might hit it.

Important: This assumes markets behave like they did recently.
When vol spikes, correlations break, or market regimes shift,
your actual risk could be 2-3x this number in a day.

That's why I'm watching the market. When I see signs of a shift,
I'll tell you and we're tightening the hedge.
Don't assume $500k is a hard floor—it's a normal-market guideline."
```

---

### **For Interview / Demonstrating Deep Understanding**

```
"VaR is interesting because it bridges two worlds:

The statistical world:
  'Here's what I measured from history (sample statistic)'

The predictive world:
  'Here's what I expect tomorrow (probabilistic claim)'

The bridge is an assumption: stationarity (distribution stays the same).

This assumption:
  ✅ Works in stable regimes (most of the time)
  ❌ Fails in regime changes (the times we most need risk tools)

This is why good risk managers:
  1. Know what VaR measures (historical percentile)
  2. Understand what VaR predicts (future risk)
  3. Monitor when the assumption breaks (regime shifts)
  4. Have backup plans for when VaR fails (stress tests, overrides, hedges)

The firms that blew up in 2008 didn't understand this gap.
They assumed VaR was a hard floor.
When distribution shifted, they had no backup."
```

---

## **Detecting When the Bridge Breaks**

### **The Gap Widens When:**

```
1. Rolling volatility changes > 50%
   → Distribution is shifting
   → Assumption breaking
   → VaR is stale

2. Historical VaR diverges from Parametric VaR
   → Data showing non-normal tail behavior
   → Distribution shape changing
   → Assumption breaking

3. New worst-day happens (5+ sigma event)
   → Outside historical range
   → Assumption definitely broken
   → Recalibrate immediately

4. Correlation regime shift
   → Assets that were negative now positive
   → Distribution structure changed
   → Assumption broken

5. Realized loss exceeds VaR multiple times in short period
   → More than ~5% of days (statistically)
   → Assumption broken
   → Backtest is failing
```

---

## **The Math Behind the Bridge**

### **Technical Statement of the Assumption**

Null hypothesis (assumption we hope is true):

$$H_0: F(R_t) = F(R_{t+1})$$

**Terms:**
- $H_0$ = null hypothesis
- $F(R_t)$ = probability distribution of returns at time $t$
- $F(R_{t+1})$ = probability distribution of returns at time $t+1$
- Statement: "The distribution today equals the distribution tomorrow"

(The distribution of today's returns = tomorrow's returns)

If $H_0$ is true:

$$\text{Quantile}_{\text{past}} \approx \text{Quantile}_{\text{future}}$$

**Terms:**
- $\text{Quantile}_{\text{past}}$ = percentile threshold measured from historical data
- $\text{Quantile}_{\text{future}}$ = percentile threshold that will occur in the future

$$\text{VaR}_{\text{from past}} \approx \text{VaR}_{\text{going forward}}$$

**Terms:**
- $\text{VaR}_{\text{from past}}$ = VaR calculated from historical data
- $\text{VaR}_{\text{going forward}}$ = VaR that actually occurs in the next period

Prediction works ✓

Test the assumption:
  - Compare rolling 252-day VaR (past) vs 252-day forward VaR (actual)
  - Or: Backtest (do realized losses match VaR assumptions?)
  - Or: Monitor volatility changes (first sign of distribution shift)

---

## **Your Refined Definition: Capturing the Tension**

### **Comprehensive Version**

> "VaR bridges a measurement-to-prediction gap:
> 
> **Measurement:** The X-th percentile loss from historical data (sample statistic)
> 
> **Prediction:** The probability of exceeding this loss tomorrow (probabilistic claim)
> 
> **Assumption:** The future distribution of returns resembles the past 
> (statistical stationarity)
> 
> **Validity:** VaR is useful when this assumption holds (stable regimes); 
> it breaks when distributions shift (regime changes, vol spikes, correlations break).
> 
> **Practice:** Monitor for assumption breaks; pair VaR with stress tests and 
> overrides for when it fails."

---

### **Interview-Ready Version**

> "VaR is a sample statistic from historical data that we use as a 
> probabilistic prediction for the future. Implicitly, we're assuming 
> tomorrow's distribution resembles the past 252 days. This works well 
> in stable markets but breaks when regimes shift—which is exactly when 
> we most need risk tools. That's why good risk systems pair VaR with 
> monitoring for distribution changes and backup hedges for tail events."

---

### **Production-Ready Version**

> "Our value at risk is $X. 
> 
> This is the historical percentile loss, used as a forward prediction 
> assuming our market regime stays stable. 
> 
> We monitor for regime breaks via rolling vol and historical/parametric 
> divergence. If we detect shifts, we recalibrate VaR, tighten hedges, 
> and may override limits."

---

## **The Practical Implication**

```
Bad risk manager:
  Sees VaR = $500k
  Thinks: "We're safe up to $500k"
  Assumes: Distribution won't change
  Reality: Vol spikes, loses $1.5M
  Outcome: Blown up

Good risk manager:
  Sees VaR = $500k
  Thinks: "This is valid if markets act like last 252 days"
  Assumes: Actively monitor the assumption
  Reality: Vol spikes, caught it early, hedged
  Outcome: Manageable loss

The difference: Understanding that VaR is a conditional prediction, 
not a hard floor.
```

---

## **Your Checklist: Do You Have This?**

- [ ] VaR is a **sample statistic** (what happened in the past)
- [ ] But we **use it as a prediction** (what we expect to happen)
- [ ] The bridge is an **assumption** (future = past distribution)
- [ ] This assumption **holds in stable times** (so VaR usually works)
- [ ] This assumption **breaks in regime shifts** (so VaR fails when we need it most)
- [ ] We should **monitor for breaks** (vol changes, divergence signals)
- [ ] We need **backup plans** (stress tests, hedges, overrides)

If you can check all seven, you understand the core insight.

---

## **Next Level: When the Bridge Breaks**

Now that you understand:
- VaR is a historical measurement used as a prediction
- It assumes the future is like the past
- This assumption breaks in regime changes

Ready to explore:
- **How to detect when the assumption is breaking?** (Warning signals)
- **What happens when VaR fails?** (Case studies: 2008, 2020)
- **How to build backup hedges for the 5%?** (Beyond-VaR framework)
- **How to actually code this and test it?** (Notebooks + production)

Which matters most for you right now?
