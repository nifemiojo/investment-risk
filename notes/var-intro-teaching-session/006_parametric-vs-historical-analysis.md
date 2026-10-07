# Parametric vs. Historical Analysis

**Deep Comparison: When methods agree, when they diverge, why it matters**

---

## The Two Methods Side-by-Side

### Historical VaR
```
Steps:
  1. Get 252 days of returns
  2. Sort from worst to best
  3. Find 5th percentile
  4. Done

Assumption: Past is prologue. Whatever we saw in history defines the tail.
```

### Parametric VaR
```
Formula:
  VaR = Mean - (Z-score × Volatility)

Example with our 60/40:
  Mean = +0.0447%
  Vol = 0.8162%
  Z-score for 95% = -1.6449
  
  VaR = 0.0447% - (-1.6449 × 0.8162%)
      = 0.0447% - (-1.341%)
      = 0.0447% + 1.341%
      = -1.296%
  
Assumption: Returns follow a perfect bell curve (normal distribution).
```

---

## First Comparison on Our Data

Same portfolio (60/40 SPY/BND):

```
Historical VaR (95%):    -0.848%
Parametric VaR (95%):    -1.296%
Difference:              -0.448%
Relative difference:     52.8% (!!)
```

**What this means:** Parametric thinks the risk is roughly 50% *higher* than what we actually saw in history.

---

## Why Do They Diverge?

### Reason 1: Fat Tails

Real stock/bond returns don't follow a perfect bell curve. They have **fat tails**—extreme events happen more often than normal distribution predicts.

**Example:**
- Normal distribution says: "5% chance of losing more than 1.3%"
- Reality says: "We actually saw 0.85% as the 5th percentile, not 1.3%"
- The extreme tail is thinner than normal distribution predicts (for this sample)

### Reason 2: Skewness

Returns aren't perfectly symmetric.

- **Positive skew** (right tail fatter): More extreme ups than downs
- **Negative skew** (left tail fatter): More extreme downs than ups
- **Normal distribution** assumes skew = 0 (perfectly symmetric)

Our 60/40 portfolio data likely has slight negative skew (stocks have crash risk).

### Reason 3: Kurtosis

This measures how much probability is in the tails vs. the shoulders.

- **High kurtosis** = Fat tails + sharp peak (crashes are bigger but rare)
- **Low kurtosis** = Thin tails + flat peak (more even distribution)
- **Normal has kurtosis = 3**

If our data has high kurtosis, normal distribution badly underestimates tail risk.

---

## When Methods Agree

(They mostly don't, but here's when they would)

**Conditions for agreement:**
- Data is perfectly normal (symmetrical, no fat tails)
- Sample size is very large (>1000 observations)
- No regime changes (correlations stable)
- No structural breaks in the data

**In practice:** This almost never happens with real returns.

---

## When Methods Diverge Dangerously

### Scenario 1: Tail Events
```
Normal times:      ~85% agreement
Market stress:     ~40% agreement
Crisis:            ~10% agreement
```

During 2008 GFC:
- Historical VaR (from 2007 data) said: "Worst loss probably ~5%"
- Actually happened: ~60% drawdowns
- Parametric would have been even worse (assumed normal distribution crashed too)

### Scenario 2: Correlation Breakdown
```
Normal times:      60/40 portfolio = low correlation between SPY/BND
Crisis:            Both down 30%+ = high correlation
```

When correlation breaks:
- Historical VaR: Recalibrates immediately (includes the new regime)
- Parametric VaR: Still assumes old correlations (lags behind)

### Scenario 3: Regime Change
Example: 2022 (stocks + bonds both crashed together)
- Historical: VaR spikes immediately (we see the bad days)
- Parametric: Spikes if vol increases, but might miss the correlation shift

---

## The Real Lesson: Distribution Shape Matters

### Visual Comparison

**Normal Distribution (Parametric assumes this):**
```
          ___
        /     \
      /         \
    /             \
   ...(symmetric)...
```

**Real Returns (Fat tails, slight skew):**
```
         ___
      /      \
    /          \__
  /                \___
 ...more crashes here...(left tail fatter)
```

The red part shows where "real" defaults are more common than "normal" predicts.

---

## Diagnostic Tests (In Your Calculator)

When you run file 005, you'll see:

### Shapiro-Wilk Test
- Tests: "Are these returns normally distributed?"
- p-value > 0.05: "Yes, looks normal" ✓
- p-value < 0.05: "No, not normal" ⚠️

### Skewness
- 0 = perfectly symmetric
- Negative = left tail fatter (crash risk)
- Positive = right tail fatter (momentum risk)

### Excess Kurtosis
- 0 = normal distribution
- Positive = fat tails (more extreme events)
- Negative = thin tails (fewer extremes)

**When running file 005, look at these metrics. They tell you when parametric is lying.**

---

## Which Method Should You Trust?

**Historical VaR:**
- ✅ Use when: Data looks normal, stable regime, no stress expected
- ❌ Avoid when: Market stress, regime change, new environment
- 💡 Pro: Honest about what we've seen
- 💡 Con: Blind to unseen risks

**Parametric VaR:**
- ✅ Use when: You want to be conservative (assumes worst case)
- ❌ Avoid when: You trust parametric assumption (you shouldn't)
- 💡 Pro: Estimates tail risk beyond history
- 💡 Con: Often completely wrong in real crises

**Best practice:** Use both, watch them diverge.

If they're close → market is normal, pick whichever matches your use case.
If they diverge significantly → warning signal, dig deeper.

---

## At Spreadex

Your autohedge system probably uses:
- **Historical VaR** for routine decisions (fast, simple)
- **Stress scenarios** for edge cases (parametric might fail)
- **Manual override** for judgment calls (when both methods look wrong)

A good risk manager:
- Knows both methods perfectly
- Watches when they diverge
- Overrides the model when intuition says yes

That's dangerous-good level.

---

## Next Step

Run **File 005: Parametric Comparison**

It will:
1. Download the same market data
2. Calculate both methods
3. Show diagnostic tests (normality, skewness, kurtosis)
4. Print detailed comparison
5. Explain when/why they diverge

Your job: Understand every number in the output.
