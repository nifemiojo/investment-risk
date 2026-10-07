# Same Distribution: What It Means & When It Breaks

**Date:** 2026-07-03  
**Topic:** Understanding what "same distribution" means, visually and numerically

---

## **What Is a Distribution?**

A distribution is **the shape of all possible outcomes**.

Not just one number. The whole pattern.

### Key Properties

1. **Mean:** Average return (e.g., +0.05% per day)
2. **Volatility (std dev):** Spread around the mean (e.g., ±1.2%)
3. **Skew:** Is it lopsided? (Left tail worse? Or right tail?)
4. **Kurtosis:** How fat are the tails? (How many extreme days?)

---

## **When Distributions Are the Same (Assumption Holds)**

### Visual Picture

```
Past Year (252 days)                Future Year (252 days)
────────────────────────            ──────────────────────

        │                                    │
        │  ← 68% of days                    │  ← 68% of days
    ────┼────                           ────┼────
       ╱ │ ╲                           ╱ │ ╲
      ╱  │  ╲                         ╱  │  ╲
     ╱   │   ╲    shape is          ╱   │   ╲    SAME shape
    ╱    │    ╲   basically the    ╱    │    ╲   (slightly
   ╱     │     ╲  same             ╱     │     ╲  random variation)
  ╱      │      ╲               ╱       │      ╲
─────────┴─────────────        ──────────┴──────────
   -3% 0% +3%                    -3% 0% +3%
```

### What "Same" Means Numerically

| Property | Past 252 Days | Next 252 Days | Status |
|----------|---------------|---------------|--------|
| Mean daily return | +0.04% | +0.05% | ✅ Same (both ~0%) |
| Volatility | 1.20% | 1.18% | ✅ Same (both ~1.2%) |
| 5% worst day | -1.85% | -1.90% | ✅ Same (both ~-1.9%) |
| Skew | -0.15 | -0.12 | ✅ Same (both slightly left-skewed) |
| Kurtosis | 0.8 | 0.9 | ✅ Same (similar tail thickness) |

**Translation:** "If I draw 252 days from next year's distribution, it looks a lot like the 252 days I just lived through."

---

## **When the Distribution Breaks (Assumption Fails)**

### Scenario 1: Volatility Spike (Most Common)

```
Past Year (Calm)                Future Year (Crisis)
────────────────────            ──────────────────

        │                                │
        │  ← Most days                  │  ← Fewer days
    ────┼────                       ────┼────
   ╱ │ ╲                         ╱╱╱ │ ╲╲╲
  ╱  │  ╲                       ╱╱  │  ╲╲
 ╱   │   ╲     SPREADS OUT     ╱   │   ╲╲╲
╱    │    ╲    → FATTER TAILS ╱    │    ╲╲╲╲
──────┴──────             ────────┴────────
 -2% 0% +2%               -8% 0% +8%

Mean: +0.04%              Mean: -0.15%
Vol: 1.2%                 Vol: 3.1% ← 2.5x higher!
5% worst: -1.85%          5% worst: -5.2% ← Much worse!
```

**What changed:** Volatility spiked. Distribution got wider.

**Example:** 
- 2019: Normal year, vol ~12%, daily moves ±1-2%
- 2020 COVID crash (Feb-Mar): Vol ~40%, daily moves ±5-10%

### Scenario 2: Correlation Breakdown

```
Past: Stocks and Bonds move opposite (diversification works)
───────────────────────────────────────

When stocks down -2%  → Bonds up +0.8%
Net portfolio move:     -1.2% (hedged)

Wait, bad news hits bonds too...

Future: Stocks and Bonds move together (no diversification)
─────────────────────────────────────────────

When stocks down -2%  → Bonds down -0.5% (now correlated!)
Net portfolio move:     -2.5% (worse!)

Distribution of portfolio is now WIDER
```

**Example:**
- Normal days: Stocks down → Bonds up (60/40 portfolio barely moves)
- Crisis (2008, 2020): Flight to safety reverses. Stocks AND bonds sell off together
- Your 60/40 diversification disappears

### Scenario 3: Regime Change (Structural)

```
Past: Bull Market (2017-2019)        Future: Bear Market (2022)
─────────────────────────────       ────────────────────────

Mean: +0.08% per day                 Mean: -0.06% per day
Biggest down day: -3.5%              Biggest down day: -6.2%
Most days positive                   More days negative

Distribution SHIFTED left
(mean got worse)
and SKEWED left
(tail risks are on the downside)
```

**What changed:** 
- Not just volatility
- The center of the distribution moved
- The whole character changed

---

## **Concrete Example: VaR Fails When Distribution Breaks**

### Historical VaR Before Crisis

Using past 252 days (normal times):
- 95% VaR = -1.85% daily loss
- Translation: "95% of days, lose no more than 1.85%"

### What Happens During Crisis

Distribution changes → volatility spikes 2-3x

Now:
- 95% VaR should be -4% to -5% daily loss
- But your model still says -1.85%
- Your hedge triggers when it's already too late
- You're underestimating risk by 2-3x

**This is what happened:**
- 2008: Models said worst case -5%, reality was -20%
- 2020 COVID: Models said -3% worst day, saw -12% in a week

---

## **How to Detect Distribution Breakdown**

### Flag 1: Volatility Changes
```python
# Rolling volatility (30-day windows)
Past 6 months:  12%, 11%, 13%, 12%, 11%  ← Stable
Now:            12%, 15%, 22%, 31%, 28%  ← SPIKING
```

**Action:** VaR estimates are stale. Recalculate.

### Flag 2: Historical vs. Parametric Diverge
```
Historical 95% VaR:   -1.85%  (based on actual past)
Parametric 95% VaR:   -1.92%  (based on normal assumption)
Difference: 0.07%     ← Close, OK

Two weeks later:
Historical 95% VaR:   -2.40%  (realized tail losses worse)
Parametric 95% VaR:   -1.65%  (still assumes normal)
Difference: 0.75%     ← HUGE DIVERGENCE

Translation: "Real tail losses are way worse than normal distribution predicts."
This is your signal: "The market is showing fat tails. Regime changing."
```

### Flag 3: Correlation Breakdown
```
Portfolio: 60% SPY, 40% BND (normally -0.2 correlation)

Normal days:
  SPY down -1% → BND up +0.3% → Net: -0.54% (hedged)
  
Crisis (correlation jumps to +0.5):
  SPY down -1% → BND down -0.5% → Net: -0.9% (NOT hedged!)
```

**Action:** Diversification disappeared. Risk profile changed.

### Flag 4: Outlier Days vs. Historical Pattern
```
Past 252 days: Worst day was -3.5%
  VaR(95%): -1.85% (so ~13 days worse than -1.85%, best of them is -3.5%)
  
This week: -6.2% down day
  That's 12 standard deviations worse than yesterday
  In a "normal" year with 252 trading days, you'd expect a -6.2% day:
    - Never (it's 12 sigma)
    - Or once every 10,000+ years
  
You just saw it on Tuesday.

Translation: "The distribution changed. Past is no longer a guide."
```

---

## **Spreadex Context**

When VaR triggers a hedge at Spreadex:

```
VaR = -$500k (95% confidence, based on normal distribution assumption)
Actual loss approaches $500k
→ System: "Hedge now"

But if distribution just shifted:
- Volatility jumped 2x
- Correlation broke down
- True 95% VaR is now -$1M

Your hedge at -$500k is not enough.
Your assumption of "same distribution" failed.
```

This is why good systems have:
1. **Primary hedge:** Triggered by VaR (based on assumed distribution)
2. **Backup hedge:** Triggered by extreme moves or divergence signals (for when assumption breaks)
3. **Circuit breaker:** Kill trade if losses exceed 2-3x VaR (assumption definitely broke)

---

## **Visual Summary**

### Same Distribution (Assumption Holds)
```
Day 1-252:    Bell curves          Day 253-504:    Bell curves
              roughly same                         roughly same shape
              ───────────                         ───────────
            ╱   │   ╲                          ╱   │   ╲
           ╱    │    ╲        ≈              ╱    │    ╲
          ╱     │     ╲                     ╱     │     ╲
         ╱      │      ╲                   ╱      │      ╲
────────────────┴──────────────   ────────────────┴──────────────
   -2% 0% +2%                          -2% 0% +2%

✅ VaR calculated from past = Good estimate for future
```

### Different Distribution (Assumption Breaks)
```
Day 1-252:    Calm               Day 253-504:    Crisis
              ───────                          ─────────
            ╱   │   ╲                        ╱╱╱ │ ╲╲╲
           ╱    │    ╲        ≠            ╱╱  │  ╲╲╲
          ╱     │     ╲                   ╱   │   ╲╲╲╲
         ╱      │      ╲               ╱     │     ╲╲╲╲
──────────────┴──────────    ────────────────┴──────────────────
  -2% 0% +2%                   -6% -3% 0% +3% +6%

❌ VaR from past WRONG for future
   Distribution changed. Volatility 2-3x higher. Tails fatter.
   Model assumptions broken.
```

---

## **Your Checklist: When Is "Same Distribution" Valid?**

✅ **Same distribution assumption holds if:**
- Volatility stable (rolling vol changes < 20%)
- Historical and parametric VaR agree (difference < 5%)
- Correlations stable (correlation matrix changes < 10%)
- No regime shift apparent (mean stable, no structural changes)
- Market conditions unchanged (no new macro shock, policy change)

❌ **Same distribution assumption BREAKS if:**
- Volatility spike (rolling vol changes 50%+)
- Historical and parametric diverge (difference > 10%)
- Correlations break (suddenly positive when normally negative)
- Regime shift (bull → bear, risk-on → risk-off)
- Macro shock (pandemic, war, financial crisis, policy shock)
- Extreme day happens (move 5+ standard deviations)

---

## **For You: The Production Question**

At Spreadex, **how does the system detect distribution breakage?**

Does it:
1. Monitor rolling volatility?
2. Compare historical vs. parametric VaR?
3. Watch correlation matrices?
4. Have manual overrides for regime breaks?
5. Use some combination?

This is where you dig. When you see VaR underestimate risk in production, trace back: Was it a volatility spike? Correlation breakdown? Regime shift?

That's dangerous-good risk thinking.

---

## **Questions to Test Understanding**

1. If historical volatility is 12% but market just spiked to 20%, what happens to your 95% VaR estimate? Is it still valid?

2. Stocks and bonds normally correlate -0.2. During a crisis, they correlate +0.4. Does your 60/40 portfolio VaR still hold?

3. You calculate 95% VaR = -1.85% from past 252 days. A historical 2 sigma event (-3.7% loss) just happened. Should you recalculate VaR?

4. At Spreadex, when would you override a VaR hedge? When would you add extra hedging even though VaR doesn't trigger?

Pick one, and we dig into it.
