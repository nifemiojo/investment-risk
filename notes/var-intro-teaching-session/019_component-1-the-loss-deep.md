# Component 1: The Loss — Building Clear Intuition

**Date:** 2026-07-03  
**Topic:** Exactly what VaR measures when it measures "losses"

---

## **What Is a Loss? Start Simple**

### **The Straightforward Example**

You have a portfolio worth $10M today.

Tomorrow, it's worth $9.85M.

```
Change in value: $9.85M - $10M = -$150k (a loss)
Return: -$150k / $10M = -0.015 = -1.5% (a loss of 1.5%)
Loss (as positive): +1.5% or +$150k
```

**Key insight:** Loss is just the negative of the return.

```
Return = (Value_tomorrow - Value_today) / Value_today
       = (9.85M - 10M) / 10M
       = -150k / 10M
       = -1.5%

Loss = -Return = 1.5%
```

So when VaR measures "losses," it's measuring the **downside tail of the return distribution**.

---

## **Why Measure Returns (%), Not Dollar Loss**

This is crucial for understanding what VaR is doing.

### **Problem: Dollar Loss Depends on Portfolio Size**

```
Portfolio A: $10M
Portfolio B: $100M

Both have the same risk (both SPY/BND 60/40).
Both could lose 1.5% on a bad day.

Dollar loss:
  Portfolio A: 1.5% × $10M = $150k
  Portfolio B: 1.5% × $100M = $1.5M

Same risk, different dollar losses!

If we measure VaR in dollars without accounting for size:
  A's VaR: $150k
  B's VaR: $1.5M

Does this mean B is 10x riskier? NO!
Both are equally risky (same return distribution)
Difference is just size.
```

### **Solution: Measure Returns (%), Not Dollars**

```
Both portfolios, same allocation:
  Return on bad day: -1.5%
  Return on good day: +1.2%

Same return distribution = same risk profile

VaR (as return): Both have 95% daily VaR of 1.85% loss
VaR (as dollars):
  Portfolio A: $185k
  Portfolio B: $1.85M

This tells us:
  "Same 1.85% loss, but B's position is 10x bigger"
  Which is exactly right.
```

**This is why VaR is measured as a percentage return, not an absolute dollar amount.**

---

## **What Are We Actually Measuring?**

### **We're Measuring the Distribution of Daily Returns**

Imagine you have 252 trading days of data:

```
Day 1 return:    -2.1%    ← Loss of 2.1%
Day 2 return:    +0.8%    ← Gain of 0.8%
Day 3 return:    -3.2%    ← Loss of 3.2%
Day 4 return:    +1.1%    ← Gain of 1.1%
...
Day 252 return:  -0.5%    ← Loss of 0.5%
```

**VaR extracts a single number from this distribution:**

```
Sort all 252 returns from worst to best:
Worst 5% = roughly 13 worst days

95% VaR = the loss threshold at day 13 (5th percentile)
```

So if the 13th worst day was -1.85%, then:
- **95% VaR = 1.85% loss** (or -1.85% return)

---

## **Building Intuition: What This Means in Practice**

### **Your Mental Model Should Be:**

```
"Every day, the portfolio moves randomly.
 I have data on 252 days of these random moves.
 Most days, the move is small (±0.5%).
 Some days, the move is larger (±2%).
 A few days, the move is really bad (±3% or worse).

 VaR picks out: The threshold where 95% of days are better, 5% are worse."
```

### **Concrete Picture**

Let's say you actually see:

```
252 trading days, daily returns sorted worst to best:

Day 1:   -8.2%   ← Worst day (maybe a crisis day in your data)
Day 2:   -4.1%
Day 3:   -3.5%
Day 4:   -3.2%
Day 5:   -2.8%
...
Day 13:  -1.85%  ← 5th percentile (this is your 95% VaR)
Day 14:  -1.75%
Day 15:  -1.60%
...
Day 126: +0.05%  ← Median (50% of days better, 50% worse)
...
Day 252: +6.7%   ← Best day
```

**What 95% VaR = 1.85% means:**
```
Days 1-13 (13 days): Losses worse than 1.85%
Days 14-252 (239 days): Losses better than 1.85%

239 / 252 ≈ 95%  ← This is your 95% confidence
13 / 252 ≈ 5%    ← This is your tail
```

---

## **Exactly What We're Measuring: A Thought Experiment**

### **Question: What determines if tomorrow is "good" or "bad"?**

```
Answer: The day's return.

If tomorrow's return is +1.2%, that's a "good" day → gain
If tomorrow's return is -2.5%, that's a "bad" day → loss

VaR says: "Based on 252 days of history, 
         5% of days I see returns worse than -1.85%
         So I expect tomorrow has ~5% chance of being a -1.85% or worse day"
```

### **What We're NOT Measuring**

```
❌ We're NOT measuring: "Will the market crash?"
   (We don't know if tomorrow is bad or good)

❌ We're NOT measuring: "What's the expected return?"
   (That's usually close to 0 daily, not what VaR measures)

❌ We're NOT measuring: "How often do big wins happen?"
   (VaR only looks at the downside)

✅ We ARE measuring: "In my past 252 days, 
                     where's the boundary between 
                     the best 95% and worst 5%?"
```

---

## **The Math Behind Loss Measurement**

### **Portfolio Value Changes**

$$V_0 = \text{portfolio value today}$$

$$V_1 = \text{portfolio value tomorrow}$$

$$\text{Return} = \frac{V_1 - V_0}{V_0}$$

**Terms:**
- $V_0$ = initial portfolio value (starting point)
- $V_1$ = ending portfolio value (after 1 period)
- $V_1 - V_0$ = absolute price change
- $(V_1 - V_0) / V_0$ = percentage return

$$\text{Loss (as positive)} = -\text{Return} = \frac{V_0 - V_1}{V_0}$$

**Terms:**
- Loss = negative return expressed as a positive number
- When return is -1.5%, loss = +1.5%
- Flips the sign for intuitive reading ("I lost 1.5%")

### **Why Daily Returns, Not Total Returns?**

```
If you measure annual returns:
  "My annual return was -15%"
  Where did those losses happen? Mostly in October? Spread out?
  Unclear.

If you measure daily returns:
  "Day 1: -2.1%, Day 2: +0.8%, Day 3: -3.2%, ..."
  You see the actual path of losses/gains
  Captures volatility and tail risk
  
VaR typically uses daily returns because:
  1. More data points (252 per year vs 1)
  2. Captures intra-year volatility
  3. More accurate tail estimates
  4. Better for position management (hedge daily)
```

---

## **Critical Insight: Loss Measurement Is About Distribution**

### **VaR Doesn't Predict Tomorrow**

```
❌ "VaR = 1.85% means tomorrow I lose 1.85%"
   WRONG. Tomorrow you might gain 1%, lose 2%, lose 0.5%, gain 3%, etc.

✅ "VaR = 1.85% means: Of 252 days, 95% had losses ≤ 1.85%,
                        5% had losses > 1.85%"
   
   So statistically, tomorrow has a ~5% chance of exceeding 1.85% loss.
```

### **This Is Crucial for Intuition**

VaR is a **sample statistic**, not a prediction.

```
Sample statistic: A number derived from past data
  "In the past 252 days, here's what I observed"

Prediction: A claim about the future
  "Tomorrow, I expect this will happen"

VaR is the former (sample statistic).
We hope it's useful for the latter (prediction).
But they're not the same.

This is why VaR breaks when the distribution changes:
  "In the past 252 days: losses were ±2% max
   Tomorrow: loses -8% (outside your sample)"
```

---

## **Measuring Portfolio Losses: Aggregation**

### **Simple Portfolio: Single Asset**

```
You own $10M of SPY

Daily return of SPY: -1.5%
Your portfolio loss: -1.5% × $10M = $150k loss

Or expressed as return: -1.5%
Or expressed as loss: +1.5%
```

### **Multi-Asset Portfolio: Multiple Components**

```
You own:
  $6M of SPY (60%)
  $4M of BND (40%)

Day 1:
  SPY return: -2%  → Loss: $6M × 2% = $120k
  BND return: +0.5% → Gain: $4M × 0.5% = $20k
  
  Net portfolio return: (-2% × 0.6) + (+0.5% × 0.4)
                      = -1.2% + 0.2%
                      = -1.0%
  
  Net portfolio loss: $10M × 1.0% = $100k

(Note: Portfolio loss is less than SPY loss alone because
 BND hedge helped.)
```

---

## **The Loss Distribution: What We Actually Sample**

### **Step-by-Step: What VaR Is Sampling**

```
Step 1: Collect 252 days of portfolio returns
  Daily returns = [r_1, r_2, r_3, ..., r_252]
  
Step 2: Convert to losses (negative of returns)
  Daily losses = [-r_1, -r_2, -r_3, ..., -r_252]
  
  (Or keep as returns and measure the left tail)

Step 3: Sort losses from worst to best
  Losses sorted = [L_worst, L_2nd_worst, ..., L_best]
  
Step 4: Find the 5th percentile loss
  Position = 5% × 252 ≈ 13
  VaR_95% = Loss at position 13

Step 5: Interpret
  "On 95% of days (239 days), losses ≤ VaR
   On 5% of days (13 days), losses > VaR"
```

---

## **Why This Matters for Production**

### **At Spreadex: Loss Measurement Affects Everything**

```
Question: "How much can this position lose in a day?"
Answer: "Based on recent historical returns, 1.85% loss (95% confidence)"

This affects:
  1. Position limits: "You can take up to $500k VaR"
  2. Hedging decisions: "When we hit $500k loss, hedge"
  3. Capital allocation: "Set aside capital for 1.85% swings"
  4. Margin management: "Watch for days when 5% loss happens"
```

---

## **Intuition Builders: Test Cases**

### **Test 1: If all past returns were between -2% and +2%, what's 95% VaR?**

```
If all 252 days: returns in [-2%, +2%]
Then: 5th percentile (95% VaR) ≈ -1.85% (or +1.85% loss)

Intuition: You're looking at the left tail of your data.
          The tail extends to -2% (the worst day)
          The 5th percentile is deep into that tail

Problem: What if tomorrow is -5%?
         Your historical data never saw it.
         VaR can't help you.
```

### **Test 2: Same data, but using Parametric (normal dist) instead**

```
If returns normally distributed with mean +0.04%, vol 1.2%:

Normal distribution extends infinitely in both tails.
5th percentile ≈ -1.93% (even though you never saw -1.93% in data)

Parametric VaR assumes: "The tail continues beyond my data
                        Following a normal curve"

Historical VaR assumes: "The tail stops at my data's edge"

Difference: Parametric is more pessimistic about unknowns.
```

### **Test 3: If you grow your portfolio from $10M to $100M**

```
Historical 95% VaR (return): -1.85% (unchanged!)
Historical 95% VaR (dollars): 
  At $10M: -$185k
  At $100M: -$1.85M

Intuition: Return-based VaR doesn't change with size.
          But dollar VaR does (naturally, because position is bigger).

This is why Spreadex probably uses dollar VaR for position limits:
  "You have $500k VaR limit"
  This adjusts automatically if you grow/shrink the desk.
```

---

## **The Deep Intuition: Loss as a Random Variable**

### **Mental Model**

Think of each trading day as a draw from an invisible distribution:

```
Distribution of daily returns
(unknown shape, we estimate from history)
         │
         │      ← Most returns here (typical days)
     ────┼────
    ╱    │    ╲
   ╱     │     ╲  ← Some days out here (volatile, but ok)
  ╱      │      ╲
 ╱       │       ╲╲  ← 5% of days out here (bad, really bad, catastrophic)
─────────┴──────────────
 -8%  -5% -2% 0% +2% +5%

VaR marks where the 5% threshold is:
"Days to the left of this line are the worst 5%"
```

### **What Loss Represents**

```
A loss is: The downside outcome
          You don't hope for it
          It's what you're trying to avoid
          But it happens anyway

VaR measures: Where in the distribution of losses 
              does the 95%/5% boundary sit?

Daily loss: The amount of money that went backward today
            Measured as % of portfolio (return) or $ amount

We collect 252 days of these observations
Find the pattern
VaR extracts the risk-relevant boundary
```

---

## **Connecting Back to the Definition**

```
"VaR is a threshold loss at confidence level c over horizon h"

The loss (Component 1) is:
  - The change in portfolio value (negative return)
  - Measured as percentage of portfolio (for comparability)
  - Over a defined time period (h = 1 day, 10 days, etc.)
  - At a percentile boundary (5% for 95% confidence)
  
Example:
  Daily loss (95% confidence) = 1.85%
  
  Meaning: On 95% of days in history,
           portfolios lost ≤ 1.85%
           On 5% of days, they lost > 1.85%
```

---

## **Your Intuition Checklist**

- [ ] Loss = negative return (or positive representation of the same thing)
- [ ] We measure percentage returns (not dollars) so different portfolios are comparable
- [ ] VaR extracts a single number from a distribution of 252 daily losses
- [ ] That number marks the boundary: 95% of days are better, 5% are worse
- [ ] This is a sample statistic (what happened), not a prediction (what will happen)
- [ ] Daily returns are used for VaR because there's more data and better tail estimates
- [ ] When portfolio grows, percentage VaR stays same, dollar VaR grows with it
- [ ] If a loss happens outside your historical data, VaR can't see it

---

## **The Core Insight on Loss Measurement**

```
VaR doesn't predict or forecast losses.

VaR observes a distribution of losses (from history).
VaR marks a threshold in that distribution (the percentile).
VaR says: "Here's where the boundary between 95% and 5% is."

Tomorrow:
  - You might not lose anything (gain 1%)
  - You might lose 0.5%
  - You might lose 1.85% (right at VaR)
  - You might lose 3% (exceed VaR, happens ~5% of the time)
  - You might lose 10% (if distribution changes)

VaR tells you: "In the past, here's where the 95/5 boundary was"
It does NOT tell you: "Tomorrow, you will or won't cross it"

But statistically, if history repeats, you'll cross it ~5% of the time.
This is the assumption (and where it breaks).
```

---

## **Next Layer of Intuition**

Now that you have this:
- Loss = change in portfolio value (downside)
- We measure as percentage returns for comparability
- Daily returns give us more data points
- VaR marks the percentile boundary in this distribution

Ready to explore:
- **How does time horizon affect loss?** (1-day vs 10-day VaR)
- **How do correlations between assets affect portfolio loss?** (Does diversification show up in VaR?)
- **How does the measurement change if distribution shifts?** (When does VaR break?)
- **Actually calculating VaR from real data** (Code + notebooks)

Which makes sense to go deeper on?
