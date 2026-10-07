# How VaR Measures Losses: Implications for Framing & Communication

**Date:** 2026-07-03  
**Topic:** Sign conventions, language choices, and how framing affects interpretation

---

## **The Sign Convention Problem**

This is where precision becomes critical and confusion spreads.

### **The Ambiguity**

When we say "VaR = 1.85%", what does that mean?

```
Interpretation 1: "Loss of 1.85%"
  The number is POSITIVE, representing a loss
  So if your portfolio is $10M, you could lose $185k
  Frame: "We expect a loss of 1.85%"

Interpretation 2: "Return of -1.85%"
  The number is NEGATIVE, representing a negative return
  So if your portfolio is $10M, you could see -$185k
  Frame: "We expect a return of -1.85%"

Same magnitude, different signs, DIFFERENT MENTAL MODELS
```

### **The Problem This Creates**

```
Risk manager says: "Our 95% VaR is 1.85%"
Trader hears: "We lose 1.85%"

Risk manager says: "Our 95% VaR is -1.85%"
Trader hears: "Our return will be -1.85%"

Are these the same? YES
But do they feel the same? NO

The sign changes how people react.
```

---

## **Three Common Sign Conventions (All Used in Production)**

### **Convention 1: Loss as Positive (Classic Risk Management)**

```
"Our 95% daily VaR is +1.85%"

Meaning: We expect a loss of 1.85% on 95% of days (or worse on 5%)
Frame: "We could lose 1.85%"
Audience: Risk managers, CFO, board
```

**Advantages:**
- Intuitive (bigger number = bigger risk)
- Easy to explain ("we could lose this")
- Aligns naturally with hedging ("we need to hedge 1.85%")

**Disadvantages:**
- Inconsistent with return notation (returns are typically negative for losses)
- Can confuse with profit/loss statements (where positive = profit)

### **Convention 2: Loss as Negative Return (Finance Theory)**

```
"Our 95% daily VaR is -1.85%"

Meaning: Our return could be -1.85% (which is a loss of 1.85%)
Frame: "Our return could be -1.85%"
Audience: Academic context, some quantitative teams
```

**Advantages:**
- Consistent with return notation
- Aligns with probability theory (lower tail of return distribution)
- Natural for comparing to other returns

**Disadvantages:**
- The negative sign is counterintuitive for a "risk" measure
- Confuses people: "Negative? That's bad, right?"

### **Convention 3: Dollar Loss (Practitioner)**

```
"Our 95% daily VaR is $185k"

Meaning: We expect a dollar loss of up to $185k on 95% of days
Frame: "We could lose $185k"
Audience: Traders, portfolio managers, clients
```

**Advantages:**
- Concrete and intuitive
- Easy to hedge against ("hedge $185k")
- Natural for position limits

**Disadvantages:**
- Depends on portfolio size (hard to compare across portfolios)
- Changes if portfolio size changes (VaR goes up just from growing the book)

---

## **How Sign Convention Affects Communication**

### **Scenario: Same Risk, Different Frames**

```
Reality: Portfolio has 95% daily VaR of 1.85% loss

FRAME 1 (Risk Manager to Board):
"Our value at risk is 1.85%. That means on 95% of days, 
we lose at most 1.85%. On 5% of days, we lose more."
→ Board reaction: Sounds manageable.

FRAME 2 (Quantitative Team Internal):
"Our 95% daily VaR is -1.85%. The loss distribution 
shows the 5th percentile at -1.85%."
→ Quant reaction: Yes, that matches theory.

FRAME 3 (Trader to Client):
"Your portfolio could lose $185k on 95% of days, 
but on about 5 days a year you might see bigger losses."
→ Client reaction: Concrete, I understand the risk.

Same risk. Different framing. Different reception.
```

### **Scenario: Where Framing Is Dangerous**

```
You present: "95% VaR is -3.5%"

Trader A (hears "negative"): "That's a return of negative 3.5%? 
That's a gain relative to a 0% baseline?"
→ Misinterprets as less risky

Trader B (hears "VaR"): "That's a loss of 3.5%"
→ Correctly interprets as risky

Same number. Due to sign, different risk perception.
This is how traders blow up: misinterpreting what the number means.
```

---

## **Why Framing Matters: The Decision-Making Chain**

### **How VaR Frame Affects Action**

```
"95% VaR is 1.85% loss"
↓
Risk manager: "We're within our 2% daily limit. No action needed."
↓
Trader: "I can take bigger positions; we have headroom."
↓
Trader increases position size
↓
Volatility spikes
↓
Portfolio drops 3.5% (outside VaR)
↓
Margin call
↓
Forced liquidation at worst prices

vs.

"95% VaR is 1.85%, but on 5% of days, losses could be 3-5%+. Here's how we handle the 5%:"
↓
Risk manager: "We hedge beyond VaR."
↓
Trader understands tail risk exists
↓
Trader takes appropriate hedge
↓
Volatility spikes
↓
Portfolio drops 3.5%
↓
Hedge gives back gains
↓
Overall impact: manageable

SAME VaR NUMBER. Different framing. Different outcome.
```

---

## **Sign Convention in Different Contexts**

### **Academic/Theoretical (Finance Theory)**

```
Returns: R (positive or negative)
Loss: L = -R (so a -1% return is a +1% loss, but written as -1% in VaR)

VaR expressed as: -1.85% (meaning the 5th percentile return)
Why? Keeps consistent with probability quantile notation.

Interpretation: "The return at the 5% tail is -1.85%"
```

### **Risk Management/Regulatory**

```
VaR expressed as: 1.85% loss (positive number for loss)
Why? Natural for discussing "how much capital do we need to hedge?"

Interpretation: "The capital-at-risk is 1.85%"
```

### **Dealer/Trading Floor**

```
VaR expressed as: $185k (dollar amount for this portfolio)
Why? Concrete for position limits and hedging sizes.

Interpretation: "If you get hit, maximum expected loss is $185k"
```

### **Client Communication**

```
"Your portfolio's worst expected 1-day loss (95% confidence) is $185k"
Why? Client cares about dollars, intuitive.

Or: "On 95% of days, your portfolio fluctuates $100k-$200k. 
     On 5% of days (roughly once a month), you might see $300k+ moves."

Why? Gives context for what "risk" means in practice.
```

---

## **The Practical Problem: Spreadex**

### **How Spreadex Likely Frames VaR**

```
Internal (risk system):
"95% daily VaR: -1.85%" 
(Negative return, academic convention)
or
"95% daily VaR: 1.85% loss"
(Positive for loss magnitude)

To traders (position limits):
"Daily VaR limit: $500k"
"Current VaR: $485k"
"Headroom: $15k"
(Dollar amount, actionable)

To clients:
"Your portfolio's estimated 1-day loss (95% confidence): $185k"
"Typical monthly fluctuation: ±$500k (95% of days)"
(Concrete, intuitive)

To regulators:
"Capital requirement based on VaR: $X"
(Tied to regulatory capital rules)
```

---

## **How Framing Affects Different Stakeholders**

### **Risk Manager**

```
Prefers: "VaR = 1.85% loss" (positive number = magnitude of risk)
Question: "Do we have enough capital/hedges for this?"
Action: Set limits, reserve capital
```

### **Trader**

```
Prefers: "$185k" (dollar amount I can actually hedge)
Question: "How much can I hedge at what cost?"
Action: Adjust position size, buy hedges
```

### **Client**

```
Prefers: "1.85% loss on portfolio"
Question: "Is this acceptable for my goals?"
Action: Accept/reject risk, adjust allocation
```

### **Regulator**

```
Prefers: Precise definition with standard methodology
Question: "Can you calculate VaR consistently and document it?"
Action: Enforce compliance, capital requirements
```

---

## **The Language Precision Issues**

### **Issue 1: "Maximum Loss"**

```
❌ "Our VaR is the maximum loss"
   This is WRONG. VaR is not the maximum.

✅ "Our VaR is the threshold beyond which we expect 5% of losses"
   But on that 5% of days, losses could be 10x worse.
```

### **Issue 2: "Expected Loss"**

```
❌ "Our expected loss is VaR"
   WRONG. VaR is a percentile, not an expectation.
   Average of the worst 5%? That's Expected Shortfall, not VaR.

✅ "Our VaR (95%) is the 5th percentile loss"
   Expected Shortfall (expected loss given you exceed VaR) is different.
```

### **Issue 3: "Risk of Loss"**

```
❌ "Risk of loss is 5%" (sound like bad thing)

Better: "On 5% of days, we could exceed this loss threshold"
        "On 95% of days, losses are contained"

Why? Emphasizes that 95% is normal, 5% is tail.
```

---

## **Sign Convention Decision for Spreadex**

### **When You Get into Production**

Ask:
```
1. "How do you express VaR internally? Positive loss or negative return?"
2. "How do you communicate VaR to traders? Dollars or percentage?"
3. "What's the convention when VaR is compared across desks?"
4. "How does the sign convention affect hedging decisions?"
```

### **What's Best Practice**

```
Internal system: Explicitly state both
  "95% daily VaR: -1.85% (negative return) = $185k loss"
  
To traders: Dollar amount or percentage loss (positive)
  "Desk Limit: $5M | Current VaR: $4.8M | Headroom: $200k"

To clients: Loss language
  "Expected 1-day loss (95% confidence): 1.85%"

To regulators: Follow their standard
  (Usually negative return in framework)
```

---

## **How This Affects Your Work**

### **When Building Models**

```
Be explicit about sign:
  - Store returns as typical (positive for gains, negative for losses)
  - Convert to loss representation when calculating VaR
  - Always specify: "VaR = 1.85% loss" or "VaR = -1.85% return"
  - Never assume the sign is obvious
```

### **When Communicating Results**

```
To engineers/other risk managers:
  "95% daily VaR is 1.85% (losses measured as positive)"
  
To traders:
  "Your desk has $300k VaR headroom"

To yourself/notes:
  "Historical 95% VaR (5th percentile, measured as loss %): 1.85%"
```

### **When You See VaR Numbers**

```
First question: "Is this positive (loss) or negative (return)?"
Second question: "What confidence level?"
Third question: "What time horizon?"

Example:
  You see: "-1.85%"
  You think: "That's the 5th percentile return (which is a loss).
            In dollars on $10M, that's $185k loss.
            Is this 95% confidence? 1-day? Historical method?"
```

---

## **Test: Do You Have This?**

When someone says "VaR is 2%", can you ask:

- [ ] "Is that 2% loss (positive) or -2% return (negative)?"
- [ ] "What confidence level—95% or 99%?"
- [ ] "What time horizon—1-day or 10-day?"
- [ ] "In dollars or percentage?"
- [ ] "What method—historical or parametric?"

If you can ask all five, you have the framing right.

---

## **The Big Picture on Convention**

```
Sign convention doesn't change the risk
It just changes how people perceive and react to it

"1.85% loss" → people think "manageable"
"-1.85% return" → people think "negative, bad"
"$185k loss" → people think "concrete, can hedge"

Same risk, three different frames, three different decisions

This is why precision in framing is not trivial.
It's how you align the entire organization around the same risk.
```

---

## **Your Takeaway**

**VaR measures losses, but how you express it (positive/negative, % or $, confidence level, horizon) completely changes how people understand and respond to the risk.**

When you see or report VaR in production:
1. **Always specify the sign convention**
2. **Always include confidence level and horizon**
3. **Choose framing for your audience** (traders want $, clients want %, risk needs documented)
4. **Never assume the sign is obvious**

The difference between a 1.85% loss and a -1.85% return is the same number, but different mental models, different decisions.

---

## **Next Question**

Now that you understand:
- VaR is a threshold loss at a percentile
- Different confidence levels = different percentiles
- Sign/framing affects how people respond

Ready to go deeper on:
- **How to actually calculate VaR** (with code, using the notebooks)?
- **How to interpret VaR results in production**?
- **How VaR fails** (and what to watch for)?
- **Expected Shortfall** (what happens beyond VaR)?

Which matters most for you right now?
