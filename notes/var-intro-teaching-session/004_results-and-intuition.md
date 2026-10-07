# Results & Intuition

**What we learned from running the 60/40 historical VaR calculator**

---

## The Numbers

Using 252 days of historical data (SPY + BND, 60/40 weights):

```
Portfolio Value:        $10,000,000
Confidence Level:       95%
Historical VaR (daily): -0.848%
Dollar VaR:             -$84,800
```

---

## What This Means

**Short version:**
"On 95% of trading days, this portfolio loses at most 0.848% ($84,800). On 1-in-20 bad days, it loses more."

**Slightly longer:**
- We looked at 252 days of historical returns
- We calculated the daily P&L for a $10M 60/40 portfolio
- We sorted all 252 returns from worst to best
- We found the 5th percentile (worst 5%)
- That percentile is our VaR

---

## Visual Intuition

Imagine all 252 daily returns sorted:

```
[worst day] ... [12 really bad days] ... [middle] ... [12 really good days] ... [best day]
                    ↑
                These 12-13 bad days are the "worst 5%"
                The worst of these is the VaR
                                    = -0.848%
```

**On a normal bell curve:**
- Most returns cluster around +0.04% (daily mean)
- Tails extend down to about -2% (bad days) and up to +2% (good days)
- The 5th percentile loss = our VaR

---

## Individual Assets vs. Portfolio

From the same calculation:

```
SPY (stocks):    -1.35% VaR
BND (bonds):     -0.42% VaR
Portfolio:       -0.848% VaR
```

**Why is the portfolio less risky than both individual assets?**

Diversification. On bad stock days, bonds often do OK (negative correlation). On bad bond days, stocks often do OK. When you mix them with 60/40 weights, the worst days don't align, so portfolio risk is lower than a weighted average of individual risks.

This is the core insight of modern portfolio theory: diversification works.

---

## Key Statistics from the Run

```
Mean daily return:     +0.0447%    (stocks + bonds together)
Volatility (daily):    +0.8162%    (standard deviation)
Worst day (252 days):  -2.68%      (actual worst we saw)
Best day (252 days):   +2.15%      (actual best we saw)
```

---

## The Confidence Level Trade-off

Same portfolio, different confidence levels:

```
90% confidence: VaR = -0.65%  ($65,000)   ← riskier day (1 in 10)
95% confidence: VaR = -0.85%  ($84,800)   ← medium (1 in 20)
99% confidence: VaR = -1.42%  ($141,600)  ← very bad (1 in 100)
```

**Interpretation:**
- 90% confidence = "On bad days (worst 10%), we lose at least 0.65%"
- 95% confidence = "On very bad days (worst 5%), we lose at least 0.85%"
- 99% confidence = "On catastrophic days (worst 1%), we lose at least 1.42%"

**Higher confidence = larger loss estimate** (because we're looking deeper into the tail)

---

## Limitations of Historical VaR

1. **Assumes past is prologue**
   - If markets have a regime change, historical data becomes stale
   - 2008 GFC: worst days were much worse than history predicted

2. **Can't predict worse than history**
   - We only saw -2.68% worst day in 252 days
   - But portfolio *could* have -5% day in a crisis
   - We'd never know from historical data alone

3. **Concentration of data**
   - Only 252 data points
   - The 95th percentile is based on ~13 observations
   - Small changes in data = big changes in VaR

4. **Doesn't capture regime shifts**
   - Correlations during normal times ≠ correlations during stress
   - 60/40 portfolio often fails when you need it most (stocks and bonds crash together in crisis)

---

## Why This Matters for Spreadex

At your dealer risk system:

- **Autohedging trigger:** "When portfolio VaR exceeds $X, auto-hedge"
- **Margin requirement:** "Customer's portfolio VaR = required margin"
- **Spread pricing:** "Wider spreads = higher risk = higher VaR in quotes"

If your VaR is wrong, all downstream decisions are wrong.

Example:
- Wrong calculation → underestimates risk
- Underestimate leads to insufficient hedging
- Unhedged risk → blowup
- This is why dealers obsess over VaR accuracy

---

## Key Insight

Historical VaR is:
- ✅ **Simple** — Just a percentile, anyone can understand it
- ✅ **Honest** — No distributional assumptions
- ✅ **Empirical** — Based on real data
- ❌ **Limited** — Can't predict worse than we've seen
- ❌ **Backward-looking** — Assumes past patterns continue

**Next:** We'll try a *forward-looking* method (parametric) that assumes returns follow a normal distribution. We'll see when it does better and when it does worse.
