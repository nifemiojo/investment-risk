# Deep Dive: Limitations of Historical VaR

**Date:** 2026-07-03  
**Topic:** Why historical VaR fails, when it fails, and what it misses

---

## **Core Problem: Historical VaR Is Backward-Looking**

Historical VaR says: *"Based on the past 252 days, here's the worst 5% of outcomes."*

**But the future is not in the past.**

It's not that historical VaR is wrong. It's that it answers the wrong question.

It answers: **"What happened?"**

You need: **"What could happen?"**

---

## **Limitation 1: Events Outside Your Window (Black Swans)**

### The Problem

You only look at past 252 days. Anything worse than that? Invisible.

### Real Example: 2008 Financial Crisis

```
Historical VaR (based on 2004-2007 data):
  95% daily VaR: -2.5%
  "95% of days, losses ≤ 2.5%"

Reality in 2008:
  October 10, 2008: S&P 500 down -9.03%  ← 3.6x worse!
  This was never in the "past 252 days" to learn from
  VaR model said: Don't worry, stay calm
  Reality: Massive blowup

Why? The 2004-2007 period was a BULL MARKET
  - Low volatility (~13%)
  - Rising correlations (everything up together)
  - No tail events
  
The model learned: "This is what returns look like"
Then: Financial system nearly collapsed
Distribution completely changed
```

### Why This Happens

```
Your 252-day window:
┌────────────────────────────────────┐
│ 2006-2007: Bull market, calm       │
│ Worst day: -2.5%                   │
│ Volatility: 13%                    │
└────────────────────────────────────┘

Hidden outside your window:
┌────────────────────────────────────┐
│ 1998 Russia/LTCM crisis            │ ← Not in window
│ 2000-2002 dot-com crash            │ ← Not in window
│ 1987 Black Monday: -22% in one day │ ← Definitely not
└────────────────────────────────────┘

Then 2008 happens: -9% day you've never seen
Your model has NO experience with this
```

### Spreadex Impact

```
Your 252-day window fits neatly after a spike in vol:
  Vol was 35%, now 15%, trending down
  
Historical VaR shows: "Biggest loss was -4%"
System hedges accordingly

Then: Geopolitical shock, war risk spikes
Vol jumps back to 35% in 2 days
-8% loss realized

Your hedge at -4% VaR wasn't enough
You were overconfident in a calm period
```

---

## **Limitation 2: Regime Change (The Distribution Changed, You Didn't Know)**

### The Problem

Historical VaR assumes the past 252 days are representative.

When the market regime changes, this assumption dies.

### Real Example: 2020 COVID Crash

```
Pre-COVID (Jan 2020):
  Volatility: 14%
  Daily moves: ±1%
  252-day worst: -3.6%
  Historical 95% VaR: -1.8%

COVID arrives (Feb-Mar):
  Volatility: 42% (3x higher!)
  Daily moves: ±5%
  New 252-day worst: -12%
  Historical 95% VaR should be: -4.5% (not -1.8%)

But you didn't update your model...
So you're still hedging at -1.8% while reality is -4.5%
Your hedge is 2.5x too small
```

### Numerical Example: When Regime Breaks

```
Day 1-252:
  Worst 5% of days: -2.0%, -1.9%, -1.8%, -1.7%, -1.6%, ... -1.2%
  Historical 95% VaR = -1.85%

Day 253-264 (regime breaks):
  New data arrives: -5.2%, -4.8%, -4.1%, -3.9%
  
Your old model still says: VaR = -1.85%
But you're now seeing -4.1% days

One week in, model is badly wrong
You're 2x underestimating risk
```

### Why Regime Breaks Happen

```
Bull Market → Bear Market:
  Mean changes, volatility spikes, correlations shift

Risk-On → Risk-Off:
  Correlations rise, diversification fails

Stable Vol → Crisis Vol:
  Hidden leverage gets revealed, forced liquidations cascade

New policies:
  Central bank action changes market structure

Geopolitics:
  War, sanctions, supply shocks
```

---

## **Limitation 3: Correlation Breakdown (Your Hedge Disappears)**

### The Problem

Historical correlations assume assets will behave similarly in the future.

They won't.

### Real Example: 60/40 Portfolio in 2008

```
Pre-2008 (2004-2007):
  SPY-BND correlation: -0.15 (negative!)
  Stocks down → Bonds up (diversification works)
  60/40 portfolio VaR: -1.2%
  (Lower because diversification hedges!)

2008 Crisis (Sep-Oct):
  SPY-BND correlation: +0.6 (positive!)
  Stocks down → Bonds also down (both selling off)
  60/40 portfolio VaR should be: -3.5%
  (Higher because diversification failed!)

What happened?
  - Pre-crisis: Stocks down 1% → Bonds up 0.2% → Net -0.58%
  - Crisis: Stocks down 1% → Bonds down 0.3% → Net -0.74%
  
Plus, on bad days, losses compound:
  - Stocks down -8% → Bonds down -2% → Net -5.6%
  - But corr rose, so it's actually worse
  - Pre-2008 model said: Don't worry, diversified
  - 2008 reality: Not diversified anymore
```

### Why Correlations Break

```
Normal times:
  Different markets responding to different information
  Negative correlation is stable (negative feedback)
  
Crisis times:
  All markets responding to same systemic risk
  "Flight to safety" flows break correlations
  Leverage causes forced liquidations across all asset classes
  Margin calls force selling anything liquid (including hedges!)
```

### Spreadex Context

```
Your risk model says:
  Equities VaR: -$800k
  FX VaR: -$200k
  Combined (with correlation):  -$900k

Assumption: Equities and FX correlate ~0.3 (diversify)

Crisis hits:
  Both selloff hard
  Correlation jumps to +0.7
  Real combined VaR: -$1.2M

Your hedge at -$900k is undersized by 33%
```

---

## **Limitation 4: Fat Tails (The Tail Event You Haven't Seen)**

### The Problem

Historical VaR captures tail events you've experienced.

Not tail events you haven't.

### Visual: Fat Tails

```
Normal Distribution (Parametric assumes this):
              │
              │  ← Most days clustered here
          ───┼───
        ╱   │   ╲
       ╱    │    ╲
      ╱     │     ╲    ← Thin tails (rarely extreme)
     ╱      │      ╲
────────────┴──────────

Historical data (252 days):
Worst day in history: -4%
Tail doesn't extend beyond that

Reality (future):
              │
              │
          ───┼───
        ╱   │   ╲
       ╱    │    ╲      ← FAT TAIL (extreme days more likely)
      ╱     │     ╲╲╲
     ╱      │      ╲╲╲╲
────────────┴──────────────
           -4% -8% -12%

A -12% day happens (not in historical data)
Your model never saw it
VaR doesn't account for it
```

### Real Example: Distribution Evolution

```
Bull Market (2014-2018):
  252-day worst: -3.2%
  Your 95% VaR: -1.6%
  
Then volatility picks up (2018 Q4):
  Worst day: -5.1%
  New 95% VaR (recalculated): -2.2%
  
Then 2020 COVID:
  Worst day: -12.3%
  New 95% VaR: -4.8%
  
Each time, the distribution got fatter in the tails
Each time, historical VaR underestimated until it caught up
But by then, you've already suffered losses
```

### Why Fat Tails Exist (The Mechanism)

```
Normal days:
  Rational actors, prices move smoothly
  Distribution looks ~normal
  
Stress days:
  Leverage gets called
  Stop-losses trigger
  Liquidity evaporates
  Price cascades down
  
More extreme than rational model predicts
Distribution has fat tails in crises
```

---

## **Limitation 5: Liquidity Risk (Can You Actually Exit?)**

### The Problem

Historical VaR assumes you can execute at recent historical prices.

In a crisis, you can't.

### Example: Liquidity Gets Sucked Out

```
Normal day:
  Bid-ask spread on SPY: 1 penny ($0.01)
  You sell $10M: executes instantly at $450
  
Crisis day (March 2020):
  Bid-ask spread: 50 cents ($0.50)!
  You sell $10M: stuck in queue, executes at $449.20
  Cost: $80k for the same position
  
VaR model said: "You can exit at yesterday's price"
Reality: Prices moved against you because everyone is selling
        
Worse case:
  Market closed (circuit breaker)
  Or trading halted
  You're stuck with the position
```

### Spreadex Impact

```
Your model: "Daily VaR = $500k, we can hedge at this level"
Assumes: You can buy hedges at recent prices

Reality in crisis:
  Volatility spike → Option prices jump 30%
  You try to hedge → costs 2x what you expected
  You can't get the hedge you need
  
Or:
  You need to sell a position to raise cash
  Bid-ask spreads blow out
  You lose another $200k just getting out
```

---

## **Limitation 6: Survivorship Bias (You're Only Looking at What Survived)**

### The Problem

Your 252 days of data only include assets/regimes that survived.

If an asset blew up, you don't have data from that.

### Real Example: Portfolio of Bonds

```
Your 252-day bond data:
  10 bonds included
  Worst day: -4.5%

Hidden: 3 bonds defaulted in 2001 (not in your data)
  Those bonds went from $100 to $20 in 2 weeks
  Loss: -80%

Your historical VaR: "Worst case -4.5%"
Reality: One of your holdings could lose -80%

But you never saw it because it happened outside your window
```

### Spreadex Example: Counterparty Risk

```
Your historical data: 2018-2020
  All major counterparties survived
  No defaults in your data
  
But: 2008 Lehman defaulted
     Swiss National Bank unpegged currency
     Russian debt defaulted 1998
     
Your model: "Based on recent history, unlikely"
Reality: Outside your window, it happened
```

---

## **Limitation 7: Window Size Tradeoff**

### The Problem

You have to choose: How many days of history to use?

```
252 days (1 year):
  ✅ Recent, reflects current regime
  ✅ More relevant
  ❌ Might miss rare events
  ❌ Misses tail risks outside this period

1000 days (4 years):
  ✅ Captures more rare events
  ✅ Bigger tail sample
  ❌ Includes old regimes (less relevant)
  ❌ Your 2014 normal market mixes with 2016 volatility spike
```

### The Dilemma

```
Use 252 days:
  Model says: VaR = -1.8%
  Reality in crisis: -4.5% (underestimated)
  
Use 1000 days:
  Model captures an old crisis from 3 years ago
  Says: VaR = -3.2%
  Reality today: -2.1% (overestimated)
  You're over-hedging, losing money
```

There's no perfect window. You have to choose a tradeoff.

---

## **Limitation 8: Path Dependence (How You Get There Matters)**

### The Problem

Historical VaR only looks at daily returns in isolation.

It doesn't account for how fast you get there.

### Example: Same Loss, Different Risk

```
Portfolio value: $10M

Scenario A (you're fine):
  Day 1: down -1%  ($9.9M)
  Day 2: down -1%  ($9.8M)
  Day 3: down -1%  ($9.7M)
  Total: -3%, spread over 3 days
  You have time to hedge, adjust, respond

Scenario B (you're blown up):
  Flash crash: down -3% in 1 minute  ($9.7M)
  Margin call hits immediately
  Forced to liquidate
  You're already out of hedges
  
Historical VaR sees both as: "Down -3%"
Same return = same risk?
NO. Path matters.

Flash crash is way more dangerous because:
  No time to respond
  Forced liquidations cascade
  Margin evaporates
  You can't execute hedges
```

---

## **Limitation 9: Hidden Leverage and Shadow Risk**

### The Problem

Historical data shows realized returns, not underlying leverage.

### Example: Hidden Leverage

```
Your portfolio shows:
  60% stocks, 40% bonds
  Reported volatility: 9%

But hidden underneath:
  You're using 2x leverage on the bonds (borrowed money)
  You're short vol via options
  You have counterparty exposure to a hedge fund
  
Historical VaR calculated on the 60/40 shows: -1.8%
But the actual leveraged portfolio could lose: -5.4% (3x worse)

Why? Because your historical window didn't capture a vol spike
If vol spikes, your short vol losses cascade
But it didn't happen in past 252 days
So VaR is blind to it
```

---

## **Limitation 10: Model Risk (What If Your Calculation Is Wrong?)**

### The Problem

Even if historical VaR is calculated correctly, there's margin for error.

### Example: Percentile Calculation Edge Cases

```
252 observations, 95% VaR:
  Position: 5% × 252 = 12.6
  
Do you use position 12 or 13?
Different calculators choose differently

Position 12: -1.90%
Position 13: -1.85%

Difference: $50k on a $10M portfolio

Which is right? Depends on your interpolation method.
```

---

## **Summary: When Historical VaR Fails**

### Red Flags That Historical VaR Is Unreliable

```
❌ Volatility spiking (rolling vol up 50%+)
❌ Rare event outside historical window happening
❌ Correlation regime breaking
❌ New market structure (policy, geopolitics)
❌ Unusual spread widths (liquidity drying up)
❌ Hidden leverage becoming visible
❌ Historical and parametric VaR diverging wildly
❌ Tail of distribution shifting (new worst day)
```

### When Historical VaR Is OK

```
✅ Normal, stable market conditions
✅ No obvious regime change
✅ Historical and parametric VaR close
✅ Volatility stable
✅ Correlations behaving
✅ Recent history good proxy for near future
```

---

## **At Spreadex: Mitigating Historical VaR Limitations**

### Layer 1: Primary Hedge (Historical VaR)
```
Trigger: VaR reaches threshold
Action: Hedge 50% of exposure
Assumption: Normal market, nothing breaks
```

### Layer 2: Backup Hedge (Tail Risk)
```
Trigger: Divergence detected (historical vs parametric)
        OR volatility spike 50%+
        OR historical worst-day exceeded
Action: Hedge additional 30% of exposure
Purpose: Protect against regime break, fat tail event
```

### Layer 3: Circuit Breaker (Emergency)
```
Trigger: Loss reaches 2-3x VaR
        OR margin utilization > 80%
        OR counterparty stress detected
Action: Force close position
Purpose: Prevent cascade failure
```

### Layer 4: Quarterly Review
```
Check: Is 252-day window still representative?
      Do we need to include older crisis data?
      What new tail risks appeared?
      
Adjust: VaR parameters, hedge ratios, correlation assumptions
```

---

## **Your Task: Audit Spreadex**

When you get into production:

1. **Understand:** How is historical VaR calculated? What window? What percentile?
2. **Check:** Does it compare against parametric? Does it diverge in stress?
3. **Find:** What's the breakdown procedure when historical VaR fails?
4. **Question:** What tail events could happen outside recent 252 days?
5. **Propose:** How would you improve the model?

That's dangerous-good risk work.

---

## **Key Insight**

Historical VaR is **honest but backward-looking.**

It says: "This is what happened."

It does NOT say: "This is what could happen."

The gap between those two statements? That's where blowups happen.

Good risk managers know this gap and plan for it.

Bad risk managers assume "happened" = "could happen" and get surprised.
