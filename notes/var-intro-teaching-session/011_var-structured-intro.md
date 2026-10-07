# Value at Risk (VaR) — Structured Intro

**Date:** 2026-07-03  
**Purpose:** Foundations + mental models before diving into code

---

## 1. **The Core Definition (60 seconds)**

VaR is a **percentile of losses**. That's it.

**Formally:** "The maximum loss you can expect to see with X% confidence over Y days."

**Example:** 
- 95% VaR (daily) = -1.85% means:
  - On 95% of trading days, you lose **at most** 1.85%
  - On 5% of trading days (bad days), you lose **more** than 1.85%

That's literally what VaR answers: *"What's the worst-case loss at the confidence level I care about?"*

---

## 2. **Why It Matters in Practice**

### At Spreadex: VaR triggers autohedging
- "My daily VaR is $500k"
- Market moves badly → actual loss approaches $500k
- System: "Hedge now, reduce exposure"
- Prevents blowups

### For clients: "Show me my risk in one number"
- Portfolio VaR = $185k (95%, daily)
- Client understands: *"On bad days, I could lose $185k"*
- Easier to explain than volatility or correlation matrices

### For you: Foundation for multi-asset risk
- VaR on equities, FX, futures, commodities separately → aggregate to portfolio VaR
- Learn to build it → understand where it breaks → know when to override it

---

## 3. **The Intuition (Not the Math Yet)**

Imagine 252 trading days of returns for your portfolio:

```
Worst day:        -8.2%
Bad day:          -4.1%
Bad day:          -3.5%
...
Bad day:          -1.9%    ← This is your 95% VaR
Mediocre day:     -0.8%
Good day:         +1.2%
...
Best day:         +6.7%
```

VaR is just: **"Sort all days worst to best, then pick the one at the 5% mark"** (for 95% confidence).

That's the entire concept. Everything else is just flavor.

---

## 4. **Two Ways to Calculate It**

### **Method 1: Historical (The Obvious Way)**

**Steps:**
1. Take past 252 days of returns
2. Sort them worst to best
3. Look at where the worst 5% ends
4. That's your VaR

**Assumption:** Past is prologue. History repeats.

**Pro:** No assumptions about distribution shape  
**Con:** You're blind to tail events you haven't seen yet

---

### **Method 2: Parametric (The Math Way)**

**Steps:**
1. Assume returns follow a normal distribution (bell curve)
2. Calculate mean + volatility
3. Use Z-score to find the percentile
4. Done

**Formula:** 
```
VaR = Mean - (Z-score × Volatility)
```

**Example:**
- Mean return: 0.05%
- Volatility: 1.0%
- 95% confidence Z-score: -1.6449
- VaR = 0.05% - (-1.6449 × 1.0%) = 0.05% + 1.6449% = -1.5949%

**Assumption:** Returns are normally distributed (they're not, but close enough often)

**Pro:** Uses only 2 numbers (mean, vol), smooth curve  
**Con:** Fat tails break this (crisis days have bigger losses than normal distribution predicts)

---

## 5. **When Both Methods Agree vs. Diverge**

### Agree (< 5% difference):
- Normal markets ✓
- You can use either method

### Diverge (> 10% difference):
- Something's broken ⚠️
- Historical says: "Actually, tail losses are bigger than normal distribution predicts"
- Reality check needed: Is this really a normal market? Or are we missing something?

---

## 6. **The Critical Limitations**

### VaR tells you:
- ✅ The threshold below which 95% of returns fall
- ❌ **NOT** how bad things get on the 5% of bad days

### Example:
- VaR (95%) = -2% loss
- On a bad day, you might lose -15% (way worse)
- VaR doesn't tell you that

### Other blindspots:
- Assumes portfolio weights stay constant (they don't in crisis)
- Assumes correlations hold (they don't during correlation breakdowns)
- Flash crashes, gap risk, liquidity evaporation: invisible to VaR
- Black swan events outside historical window: invisible

---

## 7. **Quick Mental Model**

Think of VaR like a **speed limit on a highway:**

- **Speed limit = 65 mph** (like VaR = -2% loss)
- **95% of drivers** stay at or below this speed ✓
- **5% of drivers** go faster (sometimes 90 mph, sometimes 120 mph)
- The speed limit doesn't tell you that 5% go 120 mph—it just tells you where the line is

**VaR is the line. What happens beyond it? That's Expected Shortfall (next level).**

---

## 8. **Your Path Forward**

### Now: Conceptual
- ✅ You understand what VaR is (a percentile)
- ✅ You know why it matters (risk summary, autohedging trigger, client communication)
- ✅ You know its blindspots (tail risk, model risk, regime change)

### Next: Run the code
- See it work on real data (notebook 003)
- See parametric vs. historical diverge (notebook 005)
- Build intuition from numbers

### Then: Production context
- Go to Spreadex
- Find one position
- Calculate VaR by hand
- Compare to system
- Debug if different
- Understand how it affects position sizing, hedge triggers, spread pricing

---

## **Framework Anchor**

**Remember:** VaR is not a forecast. It's a historical summary.

It says: "In the past 252 days, the worst 5% of days lost this much."

It does NOT say: "Tomorrow will be normal" or "Worse can't happen."

When you see divergence between methods, or see VaR underestimate losses in prod → that's your signal to dig deeper. That's where the real learning happens.

---

## **Where's the Fuzz?**

What's unclear here? 

- The definition itself?
- Why you'd use one method over another?
- How to interpret the results?
- How it connects to autohedging at Spreadex?
- Something else?

**Tell me where understanding breaks, and we go deep there.**

Next step: Run notebook 003 (historical VaR calculator). See the numbers. Come back with questions.
