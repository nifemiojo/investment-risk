# Component 2: Time Horizon — Why It Changes Everything

**Date:** 2026-07-03  
**Topic:** Understanding how time horizon affects VaR and what it really means

---

## **The Fundamental Question: Over What Period?**

VaR always requires specifying a time horizon.

```
VaR is not just "1.85% loss"
It's "1.85% loss over 1 day" or "over 10 days" or "over 1 month"

Same portfolio, different horizons → wildly different VaR numbers

1-day 95% VaR:   1.85% loss
10-day 95% VaR:  5.2% loss  (roughly √10 × 1-day)
1-month 95% VaR: 8.1% loss  (roughly √21 × 1-day)

Why? Because more time = more opportunity for bad things to compound.
```

---

## **Intuition: Why Time Horizon Matters**

### **The Compounding Problem**

```
1-day scenario:
  Portfolio: $10M
  1-day loss: -1.85%
  Value after: $9.815M
  
  You can rebalance tomorrow if needed.

10-day scenario:
  Portfolio: $10M
  Worst days happen spread over 10 days
  Maybe: -1%, -0.5%, -2%, -0.3%, -1.2%, ...
  
  These compound:
    (1 - 0.01) × (1 - 0.005) × (1 - 0.02) × ...
    ≠ Simple sum
    Much worse because each day's loss is applied to the remaining balance
    
  Value after 10 days: maybe $9.48M (5.2% total loss)
  
  And you COULDN'T rehedge for all 10 days.
  You're locked in.
```

### **The Key Insight: Rehedging Frequency**

```
The time horizon is implicitly asking:
  "How long until I can rebalance/hedge/adjust my position?"

1-day VaR: "I can rehedge every day"
           "Even if today is bad, I fix tomorrow"
           
10-day VaR: "I can't rehedge for 10 days"
            "Bad days compound without opportunity to adjust"
            "Risk accumulates"
            
1-month VaR: "I'm locked in for a month"
             "Worst-case drift is scary"
             "Multi-day compounding is significant"
```

---

## **The Virtual Timeline: What Each Horizon Captures**

### **1-Day VaR**

```
Today (close of business)
    ↓
Tomorrow (open to close)
    ↓
Here's the loss threshold you might see

Used for:
  - Daily position limits
  - Intraday monitoring
  - Dealer autohedging
  - Overnight risk
```

### **10-Day VaR**

```
Today (close)
    ↓
10-day period (open to close, 10 trading days)
    ↓
Here's the cumulative loss you might see

Used for:
  - Regulatory capital (Basel requires 10-day horizon!)
  - Risk appetite (strategic, how much can we tolerate)
  - Larger position adjustments
  - "If I can't rehedge for 10 days, what's my risk?"
```

### **1-Month VaR**

```
Today
    ↓
Next 21 trading days
    ↓
Here's the cumulative loss over the month

Used for:
  - Client risk statements
  - Portfolio management
  - Strategic decisions
  - "Given my rebalancing frequency, what's my risk?"
```

---

## **How Time Horizon Affects the Number: The Math**

### **Simple Case: Independent Daily Returns**

Assume daily returns are i.i.d. (independent, identically distributed):

$$\sigma_1 = 1.2\%$$

**Terms:**
- $\sigma_1$ = 1-day volatility (standard deviation of daily returns)

Then:

$$\sigma_{10\text{-day}} = \sigma_1 \times \sqrt{10} = 1.2\% \times 3.16 = 3.79\%$$

**Terms:**
- $\sigma_{10\text{-day}}$ = 10-day volatility
- $\sqrt{10}$ = square root of time (scales volatility over 10 days)

$$\sigma_{1\text{-month}} = \sigma_1 \times \sqrt{21} = 1.2\% \times 4.58 = 5.50\%$$

**Terms:**
- $\sigma_{1\text{-month}}$ = 1-month (21 trading day) volatility
- $\sqrt{21}$ = square root of time (scales volatility over 21 days)

This is the "square root of time" rule.

VaR scales with volatility, so:

$$\text{VaR}_{1\text{-day}, 95\%} = 1.85\%$$

**Terms:**
- $\text{VaR}_{1\text{-day}, 95\%}$ = 1-day Value at Risk at 95% confidence
- $1.85\%$ = the threshold loss (5th percentile of returns)

$$\text{VaR}_{10\text{-day}, 95\%} = 1.85\% \times \sqrt{10} \approx 5.85\%$$

**Terms:**
- $\text{VaR}_{10\text{-day}, 95\%}$ = 10-day Value at Risk at 95% confidence
- $1.85\%$ = 1-day VaR base threshold
- $\sqrt{10}$ = time scaling factor

$$\text{VaR}_{1\text{-month}, 95\%} = 1.85\% \times \sqrt{21} \approx 8.48\%$$

**Terms:**
- $\text{VaR}_{1\text{-month}, 95\%}$ = 1-month Value at Risk at 95% confidence
- $1.85\%$ = 1-day VaR base threshold
- $\sqrt{21}$ = time scaling factor (21 trading days in a month)

### **Why the Square Root?**

```
Intuition: Volatility compounds over time, but not linearly.

Think of it like taking steps:
  1 step: 1 unit forward
  10 steps: ~√10 units forward (not 10!)
  
  Why? Because the steps are random. Sometimes you backtrack.
  The net distance depends on how many steps (√n for N steps)
  
Same with returns:
  Each day adds random noise
  Over 10 days, the noise compounds as √10, not 10
  This is the statistical reality of random walk behavior
```

### **But This Assumes a Lot**

```
The square root rule works IF:
  ✅ Daily returns are independent (today doesn't predict tomorrow)
  ✅ Daily returns are identically distributed (same distribution every day)
  ✅ Returns are stationary (mean and vol constant)

It breaks IF:
  ❌ Correlation exists (momentum or mean reversion)
  ❌ Volatility is changing (vol clustering)
  ❌ Distribution is non-normal (fat tails, skew)
```

---

## **Why Time Horizon Is a Choice**

### **Different Users Choose Different Horizons Based on Needs**

```
Dealer (Spreadex):
  Chooses: 1-day VaR
  Why: Rebalances daily, positions shift, can hedge overnight
  Question: "If tomorrow is bad, what's my loss?"

Portfolio Manager (manages $500M fund):
  Chooses: 10-day VaR
  Why: Can't rehedge instantly, positions take days to adjust
  Question: "If markets move bad for 2 weeks, what's my max drawdown?"

Regulator (Basel Committee):
  Mandates: 10-day VaR
  Why: Sets capital requirements globally, standard horizon
  Question: "Does bank have enough capital to absorb 10-day loss?"

Big pension fund (30-year horizon):
  Chooses: 1-month VaR
  Why: Rebalances monthly, quarterly, or annually
  Question: "What's my risk between rebalancing?"
```

---

## **The Horizon-Rehedging Mismatch Problem**

### **When Horizon ≠ Your Ability to Rehedge**

```
Example 1: Correct alignment
  Your rehedging frequency: Daily (you can trade every day)
  Your VaR horizon: 1-day
  Match: ✅ Good
  Interpretation: "If tomorrow is bad, I can rehedge tomorrow"

Example 2: Mismatch → Underestimating risk
  Your rehedging frequency: Daily
  Your VaR horizon: 1-day
  Reality: Market closes at 4pm Friday, opens Monday 9:30am
  Gap: 65 hours without ability to rehedge!
  
  Your 1-day VaR assumes you can rehedge in <24 hours
  Over the weekend, it's longer
  Risk: Underestimated
  
  Better: Use 3-day VaR on Friday (captures Sat/Sun/Mon risk)

Example 3: Mismatch → Being too conservative
  Your rehedging frequency: Weekly (rebalance every Monday)
  Your VaR horizon: 1-day
  
  VaR tells you: "1-day risk is $500k"
  Reality: You can't rehedge for 5 days (Wed-Sun off, then new week)
  
  Your actual risk is: 5-day risk, which is √5 × 1-day ≈ 2.2x worse
  Real 5-day risk: $1.1M
  
  But you're setting limits based on 1-day ($500k)
  Result: Being too conservative, leaving money on table

Example 4: Mismatch → Blowup risk
  Your rehedging frequency: Daily
  Your VaR horizon: 1-day  ← Good so far
  Crisis: Market gaps down 10% at open
  Your position moves: -8% (because it's correlated)
  
  Loss: -$800k on your $10M position
  VaR predicted: Maybe $185k worst case
  
  What happened? Market gapped, you couldn't rehedge at open.
  Your 1-day horizon assumed you COULD rebalance.
  
  Reality: Gap risk (market closed when you wanted to trade)
  This is the hidden mismatch.
```

---

## **Different Horizons for Different Purposes**

### **Risk Monitoring & Position Limits (Dealer)**

```
Use: 1-day VaR
Why: Daily rehedging possible, overnight risk is main concern
Example: "Your desk has $500k 1-day VaR limit"

If exceeded:
  - Hedge triggered immediately
  - Position reduced
  - End of day, back to limit
```

### **Regulatory Capital Requirements (Supervisor)**

```
Use: 10-day VaR
Why: Banks might not be able to hedge in crisis
      Capital needs to absorb 10 days of potential losses
      Industry standard (Basel)

Formula:
  Capital_required ≈ 10-day VaR × multiplier
```

### **Client Risk Communication**

```
Use: Could be 1-day, 10-day, or 1-month depending on client
Typical: Monthly or quarterly rebalancing frequency
Example: "Your portfolio's 1-month 95% VaR is $185k"

Rationale: Client rebalances monthly, so 1-month horizon makes sense
```

### **Strategic Risk Appetite**

```
Use: Often 1-month or 1-year VaR
Why: Board-level decision about how much to lose in extreme month/year
Example: "We can tolerate a 5% one-month loss at 95% confidence"

Implication: Sets position size, leverage limits, everything else
```

---

## **How to Think About Horizon: The Planning Perspective**

### **Ask Yourself: When Can I Exit/Rehedge?**

```
Question 1: If today is bad, when can I rehedge?
  Tomorrow?  → 1-day horizon makes sense
  In a week?  → Maybe 5-day
  In a month? → 1-month
  In a year?  → 1-year

Answer determines your horizon choice.
```

### **The Liquidity Connection**

```
Horizon is also about liquidity:
  "How long before I can exit this position?"

Liquid asset (SPY):
  Can exit in minutes
  Use 1-day VaR
  
Illiquid asset (private equity, real estate):
  Can exit in months
  Use longer horizon VaR
  
Locked-up position (hedge fund with redemption restrictions):
  Can't exit for years
  Use very long horizon VaR
  
Your horizon should match your exit speed.
```

---

## **The Compounding Effect: Why Longer Horizons Are Significantly Worse**

### **Concrete Example**

```
Portfolio: $1M
1-day 95% VaR: -1%   → Loss: $10k

What about 10 days of average bad days?

Scenario: Each of next 10 days is a "bad day" (-1%)

Daily compounding:
  Day 1: $1M × (1 - 0.01) = $990k
  Day 2: $990k × (1 - 0.01) = $980.1k
  Day 3: $980.1k × (1 - 0.01) = $970.3k
  ...
  Day 10: Final value ≈ $904.4k
  
Total loss: $95.6k (9.56% loss, not 10%!)

But wait, this is average bad days. Worst 5% of 10-day periods?

Worst 10-day scenario (concatenated -1% days):
  Loss ≈ 9.56%
  
But if we had -1% daily for 10 days, that's an extreme scenario.
The actual 10-day 95% VaR is more like:
  (1-day VaR) × √10 ≈ 1% × 3.16 ≈ 3.16%
```

### **Why This Matters**

```
1-day VaR = $10k (1%)
10-day VaR ≈ $31.6k (3.16%)
1-month VaR ≈ $55k (5.5%)

Difference between 1-day and 10-day: 3.16x worse
Difference between 1-day and 1-month: 5.5x worse

If you only monitor 1-day VaR and ignore 10-day:
  You're blind to multi-day compounding
  You think your risk is 1/3 what it actually is
  That's dangerous
```

---

## **Real Example: Spreadex Dealer Risk**

### **Multi-Horizon Framework**

```
1-day horizon: $500k VaR limit
  Purpose: Intraday monitoring, autohedging trigger
  Action: If hit, hedge immediately
  Assumption: Can rehedge next day
  
10-day horizon: $1.2M VaR limit
  Purpose: Position limit, desk mandate
  Action: If trending toward limit, reduce exposition
  Assumption: Can't fully hedge for 10 days in crisis
  
1-month horizon: $2.1M VaR limit
  Purpose: Strategic, how much can lose in bad month
  Action: Capital set aside for this
  Assumption: Business as usual, can rehedge
```

**Why multi-horizon?**
- 1-day catches daily blowups
- 10-day catches compounding losses
- 1-month sets overall risk appetite

---

## **How Horizon Connects to the Assumption**

### **Stationarity Assumption Over Different Horizons**

```
1-day assumption:
  "Tomorrow's distribution = today's distribution"
  Usually holds: ✅ Likely (vol/correlations stable intraday)

10-day assumption:
  "Next 10 days' distribution = past 10 days' distribution"
  Sometimes holds: ⚠️ Less likely (vol can spike in 10 days)

1-month assumption:
  "Next month's distribution = past month's distribution"
  Often breaks: ❌ Likely to break (regime changes take weeks)

Longer horizons = more risky for distribution assumption to break
```

---

## **Your Checklist: Time Horizon Understanding**

- [ ] VaR always needs a time horizon specified (1-day? 10-day?)
- [ ] Different horizons give different numbers (longer horizon = bigger VaR)
- [ ] Time horizon should match your rehedging frequency
- [ ] Square root of time rule: VaR_10day ≈ VaR_1day × √10 (if i.i.d.)
- [ ] Longer horizons are more prone to distribution breaking (assumption more fragile)
- [ ] 1-day VaR: overnight risk (dealer monitoring)
- [ ] 10-day VaR: regulatory capital, crisis scenario
- [ ] 1-month VaR: client statements, strategic decisions
- [ ] Gap risk: liquidity events (weekends, halts) that break rehedging assumption

---

## **Why This Matters for You at Spreadex**

When you see VaR numbers:

```
Question 1: "What time horizon is this?"
           "1-day? 10-day? 1-month?"

Question 2: "How often can we actually rehedge?"
           "Does horizon match rehedging frequency?"

Question 3: "What if we can't rehedge?"
           "Gap risk, flights to safety, market closures?"

Question 4: "Is this the tightest constraint?"
           "Is 10-day limit the binding one?"
```

---

## **Next Layer: How Horizon Affects Everything Downstream**

Now that you understand:
- Time horizon is a choice based on rehedging ability
- Longer horizons give bigger VaR numbers (square root rule)
- Mismatches between horizon and reality are dangerous
- Horizon is tied to the stationarity assumption

Ready to explore:
- **Component 3: Confidence Level** (why 95%? why 99%? what's the difference?)
- **How horizons interact with confidence** (1-day 95% vs 10-day 99%)
- **How to choose the right horizon** (dealer vs investor vs regulator)
- **How horizon failures show up** (when markets gap, when hedging fails)

Which next?
