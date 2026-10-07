# VaR at Spreadex — Production Context & Scenarios

**How VaR integrates into your dealer risk system. Real scenarios you'll face.**

---

## Spreadex Risk Architecture (Simplified)

```
Client Order → Position Book → Risk Calculation → Hedge Trigger → Pricing
                                     ↑
                            VaR is here
                     (and everywhere else)
```

---

## Key Integration Points

### 1. **Autohedging Threshold**

```
System checks every minute:
  IF Client_VaR > Threshold:
    AUTO_HEDGE()
  ELSE:
    Keep as-is
```

**Your VaR accuracy impacts:**
- How often hedging triggers
- How much capital you need
- Portfolio drift
- Profitability

**What happens if wrong:**
- Underestimate VaR → Don't hedge → Lose money on bad days
- Overestimate VaR → Over-hedge → Leave money on table, lose client to competitor

---

### 2. **Margin Management**

Client A asks: "How much leverage can I get?"

Your system:
```
Credit_Limit = $50M
Margin_Requirement = Portfolio_VaR(95%)
Available_Leverage = Credit_Limit / Margin_Requirement
```

**If VaR is wrong:**
- Underestimate → Loan too much → Client blows up → You eat the loss
- Overestimate → Loan too little → Client leaves, takes business to competitor

---

### 3. **Spread Pricing**

Client B asks: "What's your price on 1,000 shares of SPY?"

Your system:
```
Base_Spread = $0.02
Risk_Adjustment = VaR_of_new_position * Risk_Factor
Total_Spread = Base_Spread + Risk_Adjustment
Price_Supplied = Market_Price ± Total_Spread
```

**If VaR is wrong:**
- Underestimate risk → Too-tight spread → Get filled with risk we can't manage → Expected loss
- Overestimate risk → Too-wide spread → Not competitive → Client uses another dealer

---

### 4. **Stress Testing & Limits**

```
Daily_Risk_Limit[] = {
  VaR_95%: $500K,
  VaR_99%: $1.5M,
  Stress_2008: $5M,
  Manual_Override: $2M
}

Current_Risk = Calculate_VaR()

For each limit:
  IF Current_Risk > Limit:
    Alert(severity=HIGH)
    IF urgent: Liquidate partial position
```

**VaR is the baseline.** When it spikes, you investigate. Is market changing? Did we get a big order? New client? New correlation pattern?

---

## Scenario 1: Normal Tuesday

**Time:** 2:30 PM  
**Event:** Large equity fund (Customer A) adds $50M to their SPY position  
**Your system calculates new VaR** (considering their whole portfolio + the new SPY)

```
Old VaR (95%):     $200K
New VaR (95%):     $280K
Increase:          $80K
```

**What happens:**
- System compares to daily limit ($500K)
- Still under limit, so no action needed
- BUT: The spread you quote them on the SPY order gets slightly wider (more risk = wider spread)
- If they do the $50M trade, you update their margin requirement accordingly

---

## Scenario 2: The Regime Shift (COVID Scenario)

**Time:** March 16, 2020  
**Event:** Stocks crater, VIX spikes 80%+  
**Your system recalculates VaR**

```
Monday VaR (95%):   $300K (normal)
Tuesday VaR (95%):  $2.2M (10x spike!!)
```

**What happens:**
- System alerts: "RISK SPIKE — VaR increased 6x"
- Your risk team investigates:
  - Did returns distribution change? (Yes—fat tails)
  - Did correlations break? (Yes—bonds no longer hedge stocks)
  - What confidence level for hedge decision? (Probably 99%, not 95%)

- **Autohedge triggers** (if enabled)
  - System hedges all customer positions above threshold
  - Protects Spreadex balance sheet
  - Costs $ to hedge, but prevents much bigger loss

- **VaR model recalibrates**
  - Maybe switch from 252-day lookback to 90-day (faster to adapt)
  - Maybe increase confidence to 99% (more conservative in stress)

**Key insight:** VaR accuracy is CRITICAL in regime shifts. If your VaR didn't spike fast enough, you'd be unhedged when you need to be hedged. That's how dealers blow up.

---

## Scenario 3: The Correlation Breakdown (2022 Energy Crisis)

**Time:** September 2022  
**Event:** Stagflation sentiment → Stocks down, Bonds down, Credit widening  
**Normal 60/40 assumption:** Bonds should hedge stocks. They don't.  
**Your system calculates VaR**

```
Historical (using 2021 data): Assumes correlation(SPY, BND) = -0.20
              VaR = -0.85%

Parametric (using same data): Assumes normal distribution
              VaR = -1.30%

Current regime (Sept 2022): correlation = +0.15 (positive! bonds crashing too)
   Actual VaR = -2.85% (WAY worse than either model predicted)
```

**What happens:**
- Risk system flags: "Divergence detected"
- Historical and parametric disagree significantly
- Correlation has shifted
- **Manual override:** Risk manager looks at portfolio, sees the regime shift, increases internal limits or hedges more aggressively

**Why this matters:** If you'd set leverage based on historical assumptions, you'd be overleveraged. In 2022, many hedge funds got hurt this way (assumed 60/40 diversification, got whipsawed when bonds crashed).

---

## Scenario 4: The Feedback Loop (Cascading Hedges)

**Time:** Oct 19, 1987 (Black Monday, but happens every few years)  
**Event:** Market down 10% in one session  
**Your system calculates VaR**

```
Morning VaR:   $500K
Mid-day VaR:   $1.2M (market sold off)
Autohedge triggers → System sells futures to hedge
Market sells off more
Your system recalculates VaR
It's now $2M
Autohedge triggers again
System sells more futures
...cascade continues...
```

**The danger:** Everyone's autohedge triggers at same time → Everyone hedges → Massive selling pressure → Prices crash faster → More VaR spikes → More hedging.

This is why dealers need **circuit breakers**:
- Pause autohedging if VaR changes >50% in 5 minutes
- Manual review
- Smoothing algorithms
- Clear limits on hedge size per time period

**VaR isn't the problem (it's doing its job).** But mechanical application of VaR-based rules can amplify crashes. You need judgment.

---

## Your Job When You Revisit VaR at Spreadex

### Week 1
1. Find where VaR is calculated (which system? which code?)
2. Understand the configuration (252-day? 95% confidence? historical or parametric?)
3. Trace one live customer position through the system
4. Recreate VaR calculation by hand / Python script
5. Verify it matches the system's number

### Week 2
1. Find an interesting scenario (maybe correlation is weird, maybe vol is spiking)
2. Stress-test VaR with different assumptions
3. Propose one improvement (e.g., "detect regime change faster", "add stress percentile", "improve correlation estimation")
4. Document it

### Artifact for Interview
- "Here's what I learned about risk systems at Spreadex"
- "Here's how VaR works there and where I found a gap"
- "Here's my proposed fix"

That's dangerous-good. That's what gets you hired at AQR.

---

## Key Principles for Production VaR

1. **Accurate > Sophisticated**
   - A simple, correct VaR > complex, wrong VaR
   - 252-day historical beats fancy parametric if parametric is wrong

2. **Fast adaptation**
   - VaR must react to regime changes (shortening lookback, increasing confidence during stress)
   - Stale VaR is worse than no VaR

3. **Multiple perspectives**
   - Don't trust one number
   - Historical + Parametric + Stress scenarios + Manual override
   - When they diverge, investigate

4. **Feedback loops matter**
   - VaR triggers hedging → hedging moves markets → VaR spikes → more hedging
   - Build in circuit breakers and smoothing

5. **Know your limitations**
   - VaR won't predict the next crisis
   - It will tell you how bad things got historically
   - Use that as a baseline, not a prediction

---

## Next Step

Go back and run **File 003** and **File 005** with Spreadex in mind.

You're not just calculating VaR. You're starting to see how that number flows through a real dealer system and impacts thousands of decisions per day.

That's the context. That's why VaR matters. That's why getting it right is critical.
