# Core Definition of Value at Risk: Building Precision

**Date:** 2026-07-03  
**Topic:** Constructing a precise, unambiguous definition of VaR

---

## **The Starting Problem: Vague Definitions Fail**

Most definitions you'll see:

> "VaR is the maximum loss you could lose under normal conditions."

Problems:
- What's "maximum"? Biggest possible? Or some threshold?
- What's "normal"? Who defines it?
- Over what time period?
- How confident are you in this number?

This is too sloppy for production. We need precision.

---

## **Building Toward Precision: Step by Step**

### **Component 1: The Loss**

**What are we measuring?**

Not just any number. A **loss**.

```
Let's say your portfolio is worth $10M today.
Tomorrow it's worth $9.9M.

Gain/loss: -$100k (a loss of $100k)
Return: -1% (the loss as a percentage)

In VaR, we typically use: Daily return = -1%
(Not the dollar amount, the return percentage)

Why? Because a 1% loss on $1M portfolio ≠ 1% loss on $100M portfolio
Percentage makes them comparable
```

**Precise language:**

VaR measures **negative returns** (losses as a percentage or dollar amount of your position).

**Notation:**
```
R = return on portfolio (daily, weekly, monthly, or other horizon)
L = loss = -R  (so a -1% return = +1% loss)

We measure the distribution of L
```

---

### **Component 2: The Time Horizon**

**Over what period is this loss measured?**

This matters hugely.

```
1-day horizon:
  "Tomorrow's loss could be..."
  Used for: Daily hedging, intraday trading

10-day horizon:
  "Over the next 10 trading days, loss could be..."
  Used for: Position limits, regulatory capital

1-month horizon:
  "Over the next month, loss could be..."
  Used for: Portfolio management, longer-term risk
```

**They give different answers:**

1-day 95% VaR:  $$-1.85\%$$

**Terms:**
- 1-day = time horizon (market close to market close)
- 95% = confidence level (5th percentile)
- $-1.85\%$ = the loss threshold

10-day 95% VaR: $$-5.2\%$$ (roughly $$\sqrt{10} \times \text{1-day}$$ for i.i.d. returns)

**Terms:**
- 10-day = time horizon (10 trading days)
- $\sqrt{10}$ = time scaling factor
- $-5.2\%$ = scaled loss threshold

1-month 95% VaR: $$-8.1\%$$

**Terms:**
- 1-month ≈ 21 trading days
- Scales by $$\sqrt{21}$$
- $-8.1\%$ = the monthly loss threshold

Why? Volatility compounds over time (in rough square-root time). More time = more opportunity for bad things to happen.

**Precise language:**

VaR is always specified with a **time horizon** (1-day, 10-day, etc.).

**Notation:**

$$\text{VaR}_h = \text{Value at Risk over horizon } h$$

**Terms:**
- $\text{VaR}_h$ = Value-at-Risk as a function of horizon
- $h$ = time horizon

where $$h = 1 \text{ day}, 10 \text{ days}, 1 \text{ month}, \ldots$$

---

### **Component 3: The Confidence Level (The Critical Piece)**

**What does "95% confidence" actually mean?**

This is where precision breaks down most often.

#### **Definition: Confidence Level = Probability Interpretation**

```
95% VaR over 1 day = $1.85M loss

Precise interpretation:
"Under my model's assumptions, there is a 95% probability 
that tomorrow's loss will be LESS than $1.85M.

Equivalently: 
There is a 5% probability that tomorrow's loss will be 
GREATER than $1.85M."

NOT: "I'm 95% confident this won't happen"
NOT: "There's a 5% chance of losing more than this"
     (This is actually wrong - it's exactly backward!)

RIGHT: "5% of the days (roughly), losses exceed this threshold"
```

#### **The Mathematical Notation**

```
Let L = loss (as a percentage or dollar amount)
Let c = confidence level (e.g., 0.95 for 95%)

VaR_c = the value such that:
  P(L ≤ VaR_c) = c
  
  (Probability that loss is at most VaR_c equals c)

Or equivalently:
  P(L > VaR_c) = 1 - c
  
  (Probability that loss exceeds VaR_c equals 1 - c)

For 95% confidence:
  P(L ≤ VaR_0.95) = 0.95
  P(L > VaR_0.95) = 0.05
```

#### **Why This Is Confusing**

The **confidence level** and the **percentile** are complements:

```
95% confidence level = 5th percentile
  (You're confident about the best 95%, so you're looking at the worst 5%)

99% confidence level = 1st percentile
  (You're confident about the best 99%, so you're looking at the worst 1%)

90% confidence level = 10th percentile
  (You're confident about the best 90%, so you're looking at the worst 10%)
```

They add to 100%: `confidence + (100% - confidence) = 100%`

---

### **Component 4: The Model Assumption (The Hidden One)**

**This is what everyone glosses over.**

```
"95% VaR = -1.85% means 95% probability of not losing more than 1.85%"

But: Probability under WHAT?

Answer: Under my model's assumptions about the distribution.
```

#### **Historical VaR Assumption**

```
Assumption: "The future will draw from the same distribution 
            as the past 252 days"

Translation: "If it didn't happen in the past 252 days,
             it's not part of the distribution"

Problem: What about tail events outside this window?
         A -12% day?
         A correlation breakdown?
         Market closed?
```

#### **Parametric VaR Assumption**

```
Assumption: "Returns follow a normal distribution"

Translation: "The shape of outcomes is a bell curve
             with mean μ and volatility σ"

Problem: Real markets have fat tails (way more extreme events 
         than normal distribution predicts)
```

#### **Precise Language**

```
Historical VaR is:
  P(L ≤ VaR_c | past 252 days) = c
  (Probability under the assumption that future = past)

Parametric VaR is:
  P(L ≤ VaR_c | R ~ Normal(μ, σ)) = c
  (Probability under the assumption returns are normal)

These are CONDITIONAL on the assumption being true.
If the assumption breaks → the probability claim is wrong.
```

---

## **The Complete Precise Definition**

### **English Version**

```
Value at Risk (VaR) at confidence level c over horizon h is:

"The threshold loss L* such that, under the specified model's 
assumptions about the return distribution, there is a 
probability c that tomorrow's loss will be at most L*, 
and probability (1-c) that the loss will exceed L*."

Example (95%, 1-day):
"There is a 95% probability we lose no more than $1.85M 
over the next day (assuming the past is representative of 
the future and returns are iid from the same distribution 
we've observed)."
```

### **Mathematical Version**

```
Given:
  - Confidence level c (typically 0.95 or 0.99)
  - Time horizon h (typically 1 day)
  - Portfolio return R_h over horizon h
  - Loss L_h = -R_h (negative return = loss)
  - Assumed distribution F(L) from historical data or parametric model

VaR is defined as:

VaR_c,h = inf{x : P(L_h ≤ x) ≥ c}

Or more intuitively, the (1-c) quantile of the loss distribution:

VaR_c,h = F^{-1}(1-c)

Which means:
  P(L_h > VaR_c,h) = 1 - c
  P(L_h ≤ VaR_c,h) = c
```

### **What This Says**

Breaking it down:
- **VaR** = a specific loss threshold (a number, in $ or %)
- **c** = confidence level (0.95 = 95%)
- **h** = time horizon (1 day, 10 days, etc.)
- **Assumption** = embedded in how we calculate F (historical or parametric)

All three components are required. You cannot say "VaR is $1M" without specifying:
- Is it 95% or 99% confidence?
- Is it 1-day or 10-day?
- Did you use historical or parametric method?

---

## **What VaR Does NOT Measure**

This is critical precision point:

### **What VaR Doesn't Tell You**

```
95% VaR = -1.85% loss means:

❌ It does NOT tell you: "The worst possible loss"
   (Could be -20% on a bad day outside your model)

❌ It does NOT tell you: "The average loss on bad days"
   (That's Expected Shortfall/CVaR)

❌ It does NOT tell you: "I'm safe if I stay within VaR"
   (5% of days you lose MORE than this)

❌ It does NOT tell you: "This is the limit of what could happen"
   (Tail risk exists beyond VaR)

✅ It DOES tell you: "On 95% of days, losses are less than this"
   (That's the percentile interpretation)

✅ It DOES tell you: "On ~5% of days (roughly), I exceed this"
   (This is the risk you're taking)
```

### **Why This Matters**

Imagine you hedge at VaR:
```
"My 95% daily VaR is -$500k, so I'll hedge when we hit -$500k"

Problem: On 5% of days, you exceed -$500k
         You get hit with bigger losses than hedged
         Your hedge catches only the normal 95%, not the bad 5%

What you really need:
         Primary hedge at VaR (normal days)
         + Backup hedge beyond VaR (tail days)
```

---

## **Variations in Definition (Same Concept, Different Names)**

These all measure the same thing:

```
VaR at 95% confidence, 1-day horizon

= 95th percentile of returns (if returns are increasing)
= 5th percentile of losses (if losses are measured as positive)
= The threshold such that 95% of days are better than this
= The threshold such that 5% of days are worse than this
= The (1 - 0.95) = 0.05 quantile measured from the downside
= The conditional quantile of the loss distribution at level (1-c)
```

All these statements describe the same number.

---

## **Testing the Definition Against Edge Cases**

### **Test Case 1: What if all past 252 days had returns between -2% and +2%?**

Historical 95% VaR:
```
5th percentile = position 13 out of 252
If data goes from -2% to +2%, position 13 ≈ -1.85%

So: 95% VaR = -1.85%

Interpretation: "In my 252 days of data, losses never exceeded 1.85%,
                so I expect 95% confidence of not exceeding 1.85%"

Question: What if a -5% day happens tomorrow (outside your data)?

Answer: Your model is wrong.
        You assumed "future = past"
        That assumption broke.
        VaR predicted 95% confidence.
        Now losses are at 5% percentile OR WORSE
        You've moved outside the "95% confidence zone"
```

### **Test Case 2: Same data, but you use Parametric VaR instead**

```
Data: All returns between -2% to +2%
Mean return: +0.04%
Volatility: 1.2%

Assuming normal distribution:
95th percentile of Normal(0.04%, 1.2%) ≈ -1.93%

So: Parametric 95% VaR = -1.93%

Compare:
Historical:   -1.85%
Parametric:   -1.93%

They're close (differ by 0.08%). Why?

Because the data IS roughly normal in that range.
If they diverge a lot → data is NOT normal → parametric assumption breaks
```

### **Test Case 3: Confidence level misinterpretation**

```
❌ Wrong interpretation:
   "95% VaR = -1.85% means I have a 95% chance of not losing more"
   (This sounds right but is actually backward in subtle way)

✅ Right interpretation:
   "95% VaR = -1.85% means: in 95% of days, losses ≤ 1.85%
    In 5% of days, losses > 1.85%"

The difference:
   Wrong: "95% chance I'm OK"
   Right: "95% of the time I'm in this range, 5% I'm not"

These sound similar but have different implications:
   - Wrong leads to complacency
   - Right means you actively plan for the 5%
```

---

## **At Spreadex: Precise Definition in Production**

When you ask about VaR in the system, ask exactly:

```
1. "What confidence level? 95%? 99%?"
2. "What time horizon? 1-day? 10-day?"
3. "What method? Historical (how many days?) or Parametric?"
4. "What do you measure? Daily returns in % or dollar loss?"
5. "What's your assumption about the future?"
6. "When does this break? (When do you override it?)"
```

The answer to each changes what VaR means.

---

## **Your Checklist: Do You Have the Definition?**

- [ ] VaR is a **threshold loss** (not an average, not a max)
- [ ] Specified by **confidence level** (95%, 99%, etc.)
- [ ] Over a **time horizon** (1-day, 10-day, etc.)
- [ ] Under **model assumptions** about the distribution
- [ ] It tells you: "X% of days, losses are less than this"
- [ ] It does NOT tell you: "The worst that could happen"
- [ ] It does NOT tell you: "Average loss on bad days"
- [ ] Different methods (historical, parametric) give different VaR numbers
- [ ] The method assumption matters for whether VaR is accurate

---

## **The Core Insight**

VaR is a **probabilistic statement about a percentile**, not a "maximum loss."

The precision matters because:
- If you think it's the max → you get complacent on the 5% tail
- If you know it's the 95th percentile → you plan hedges for the 5%

**This difference kills firms in crises.**

---

## **Questions to Test Your Understanding**

1. **If your 95% daily VaR is -$500k, does that mean:**
   - A) You won't lose more than $500k? 
   - B) On 95% of days, you lose less than $500k?
   - C) Both?
   
   (Answer: B is correct. A is wrong — 5% of days you do lose more.)

2. **If you change confidence from 95% to 99%, does your VaR:**
   - A) Get smaller (less extreme)?
   - B) Get bigger (more extreme)?
   - C) Stay the same?
   
   (Answer: B. 99% confidence means you're looking further into the tail.)

3. **If historical and parametric VaR diverge, what does that mean:**
   - A) One of them is definitely wrong?
   - B) The data isn't normally distributed?
   - C) The future might break your assumptions?
   
   (Answer: B is the immediate signal; C is the implication.)

Which of these is unclear?
