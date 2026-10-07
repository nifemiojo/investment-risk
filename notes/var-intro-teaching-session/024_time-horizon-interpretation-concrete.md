# Concrete VaR Time Horizon Interpretation: Working Definition

**Date:** 2026-07-03  
**Topic:** How to interpret and communicate time horizon in your VaR definition

---

## **The Core Interpretation Question**

When someone says:

> "Our portfolio's 95% VaR is 1.85% loss over 1 day"

What exactly does that mean? Let's unpack it completely.

---

## **Breaking Down the Statement**

### **"95% VaR"**

Confidence level: On 95% of trading days (historically), losses were BETTER than the threshold.

```
Out of 252 trading days:
  239 days: Losses ≤ threshold
  13 days: Losses > threshold
  
That 5% is where VaR marks the boundary.
```

### **"1.85% loss"**

The specific loss magnitude we're calling the threshold.

```
This means:
  Loss = Negative return
  Magnitude: 1.85% of portfolio value
  
On a $10M portfolio:
  Dollar loss = 1.85% × $10M = $185k
```

### **"Over 1 day"** ← This Is the Time Horizon

The critical part. What does "1 day" really mean?

---

## **Interpreting the Time Horizon: What "1 Day" Means**

### **1-Day Horizon: The Standard Interpretation**

```
"Over 1 day" means:

  The loss between market close TODAY
  and market close TOMORROW
  
  Or: The overnight + next trading day combined
```

**Concretely:**

```
Today: 4:00 PM close
  Portfolio value: $10M
  
Tomorrow: 4:00 PM close
  Portfolio value: $9.815M (if worst 5% day)
  Loss: $185k
  
Your hedging/rehedging opportunity:
  "If tomorrow is bad, I can rehedge on tomorrow's market"
  
The assumption:
  "I assume I can respond to losses within 24 hours"
```

### **What 1-Day Does NOT Mean**

```
❌ NOT: "If the market moves 1.85%, I can recover from anything"
   (It might move -3% because it's in the worst 5%)

❌ NOT: "No loss tomorrow will exceed 1.85%"
   (5% of days it will)

❌ NOT: "I can instantly rehedge if I lose 1.85%"
   (Takes time to execute, market impact, gaps, etc.)

❌ NOT: "The market will be open for me to trade"
   (Not over weekends or market halts)
```

---

## **Interpreting Longer Horizons: 10-Day and 1-Month**

### **10-Day Horizon**

```
"Over 10 days" means:

  The cumulative loss from today's close
  through 10 trading days later
  
  You CANNOT rehedge for 10 days
  (Either because you're forced to hold, or it's a crisis scenario)
  
Concretely:
  Today (close):     Portfolio = $10M
  Day 1 (close):     Day 1 move
  Day 2 (close):     Day 2 move (compounded)
  Day 3 (close):     Day 3 move (compounded)
  ...
  Day 10 (close):    Final portfolio value
                     
  Loss could be:     -5.2% (if that's the worst 5% point over 10 days)
  Dollar loss:       -$520k
```

**The assumption:**
```
"For the next 10 days, I can't exit this position"

Why you can't exit:
  - Regulatory lock-up period
  - Illiquid position (can't find buyer)
  - Market disruption (no buyers at any price)
  - Internal: taking a "hold" bet, not touching position
  
Example from real world:
  - Lehman bankruptcy on Monday
  - No one trading Lehman bonds
  - Forced to hold through Friday
  - 5-day horizon is what matters
```

### **1-Month Horizon**

```
"Over 1 month" (21 trading days) means:

  The cumulative loss from today's close
  through the entire next month
  
  You won't rebalance for a full month
  
Concretely:
  Today (close):          Portfolio = $10M
  After next 21 days:     Portfolio value after 21 compounding moves
  
  Maximum loss (95%):     -8.1% (if that's worst 5% 21-day period)
  Dollar loss:            -$810k
```

**The assumption:**
```
"I rebalance monthly, so my 'lock-up' period is one month"

Why:
  - Pension fund rebalances quarterly
  - Doesn't want to trade more than needed (costs/taxes)
  - Accepts the drift over a month
  - Needs to know: "What's my worst month?"
```

---

## **Three Time Horizons: Three Risk Perspectives**

### **1-Day VaR: Overnight Risk**

```
Definition:
  Loss between close today and close tomorrow
  
Rehedging assumption:
  "Tomorrow's market opens, I can trade if needed"
  
Used for:
  - Daily position limits
  - Intraday monitoring
  - Overnight risk dashboard
  
Example at Spreadex:
  "Your desk: $500k 1-day VaR limit
   Meaning: Each close of business, your position is 95% safe
            On 5% of days, you exceed this"
```

### **10-Day VaR: Stress-to-Exit Period**

```
Definition:
  Cumulative loss over 10 trading days
  
Rehedging assumption:
  "I have no exit for 10 days
   Could be illiquid, crisis, or strategic choice"
  
Used for:
  - Regulatory capital (Basel standard)
  - Position limits (desk mandate)
  - "If we can't trade for 10 days, can we survive?"
  
Example:
  "Our $1.2M 10-day VaR limit means:
   Longest stress without trading should not exceed $1.2M
   At 95% confidence it doesn't"
```

### **1-Month VaR: Rebalancing Cycle Risk**

```
Definition:
  Cumulative loss over the calendar month
  (or 21 trading days)
  
Rehedging assumption:
  "I rebalance on a monthly cycle
   That's my natural lock-up period"
  
Used for:
  - Client reporting ("Here's your monthly risk")
  - Portfolio-level decisions
  - Strategic risk appetite ("Can we tolerate a 5% bad month?")
  
Example:
  "Your fund's 1-month 95% VaR is $2.1M
   Meaning: In a bad month (5% of months),
            losses could reach $2.1M
            But 95% of months are better"
```

---

## **Interpreting the Horizon in Context: Examples**

### **Example 1: Daily Dealer Position**

```
Statement: "Your 95% daily VaR is $500k"

Interpretation:
  Time horizon: Overnight through tomorrow close
  Meaning: "On 95% of days, your overnight + next day loss ≤ $500k
            On 5% of days (roughly 13 per year), loss > $500k"
  
  Action: If you're at $485k end of day, you have $15k headroom
          If you exceed $500k, trigger hedge
          
  Why 1-day? You can rebalance daily
            Risk measured per trading day
            Overnight is your constraint
```

### **Example 2: Fund Position (Can't Exit for 10 Days)**

```
Statement: "We're $1.2M 10-day VaR on this position"

Interpretation:
  Time horizon: Next 10 trading days without exit
  Meaning: "If we're stuck with this position for 10 days,
            95% of 10-day periods show loss ≤ $1.2M
            5% show loss > $1.2M"
  
  Why 10-day? Position is illiquid
             Takes 10 days to unwind without market impact
             Can't exit faster
             
  Risk view: "We need $1.2M capital for this 10-day exposure
             If markets move bad for 10 days, we might lose it all"
```

### **Example 3: Client Statement (Monthly Rebalancing)**

```
Statement: "Your portfolio's 1-month 95% VaR is 2.1%"

Interpretation:
  Time horizon: Next calendar month (21 trading days)
  Meaning: "In a typical month, you see small losses
            In a BAD month (5% of months = 1 per year),
            you could see a 2.1% loss"
  
  Dollar version: "On a $1M portfolio, that's $21k
                  Bad months happen, this is what to prepare for"
  
  Why monthly? You rebalance quarterly
              Monthly is your reporting/thinking period
              Want to know: "What's my monthly risk?"
```

---

## **The Hidden Assumption: Can You Actually Rehedge?**

The time horizon interpretation depends on ONE thing:

```
Can you rehedge / trade / exit at the end of the horizon?

If YES (1-day dealer):
  You can trade tomorrow at close
  1-day VaR makes sense
  
If NO (illiquid position):
  You can't trade for 10 days
  1-day VaR is MISLEADING
  You need 10-day VaR
  
If MAYBE (market crisis):
  You might not be able to trade
  Use longer horizon as insurance
  E.g., use 10-day even if you usually trade daily
```

### **The Mismatch Problem**

```
Scenario: You're a dealer using 1-day VaR

Reality check: Can you REALLY rehedge tomorrow?
  Friday close: Market event happens
  Saturday/Sunday: Market closed (can't hedge)
  Monday open: Market gap down 10%
  
Result: Your 1-day VaR prediction (1.85% loss) was wrong
        Actual loss: 8% because you couldn't rehedge over weekend
        
Fix: Use 3-day VaR on Friday (Fri close → Mon close)
     Accounts for: Weekend gap risk
```

---

## **Reading the Horizon from a VaR Statement**

### **Checklist: What to Ask**

When you see a VaR number with a horizon, ask:

```
1. [ ] What is the time horizon? (1-day? 10-day? 1-month?)

2. [ ] Does it match my rehedging ability?
         Can I rehedge/exit at end of this period?
         If NO → horizon is wrong for me
         
3. [ ] What's the actual calendar period?
         "1-day" = overnight + next trading day
         "10-day" = next 10 trading days (not 2 calendar weeks)
         "1-month" = next 21 trading days (not calendar month)
         
4. [ ] What breaks my assumption?
         Weekend? Halts? Market closure?
         Illiquidity? Forced holding?
         If any YES → actual horizon is longer
         
5. [ ] What's my backup if horizon breaks?
         If I can't rehedge? What's my hedge?
         What's my stress scenario?
```

---

## **Horizon in Your VaR Definition**

### **How to State It**

When you define VaR, be specific about horizon:

**Weak:**
> "VaR is the loss threshold at a confidence level over some period."

**Better:**
> "VaR is the loss threshold at a specified confidence level (e.g., 95%) 
> over a specified time horizon (e.g., 1 day), assuming you can rehedge 
> or adjust the position at the end of that horizon."

**Best:**
> "95% daily VaR is the loss where, historically, 95% of 1-day trading periods 
> had better outcomes, and 5% had worse outcomes, assuming you can rehedge 
> tomorrow. The number scales with time horizon (daily VaR × √10 ≈ 10-day VaR) 
> but this scaling assumes independent returns—an assumption that breaks 
> in crises when correlations emerge."

---

## **At Spreadex: Interpreting Horizon in Production**

### **What You'll See**

```
Desk A (Equities dealer):
  1-day 95% VaR: $500k
  → Nightly rehedge, overnight risk dominant
  
Desk B (FX options):
  10-day 95% VaR: $2M
  → Month-long positions, can't rehedge daily
  
Risk Ops:
  Regulatory 10-day 95% VaR: $8.5M to $12M (across firm)
  → Capital calculation, Basel requirement
```

### **Questions to Ask**

```
1. "Why is Desk A using 1-day but Desk B using 10-day?"
   Answer: Different rehedging speeds
   
2. "What happens to Desk A's VaR on Friday EOD?"
   Answer: Should it increase? (Weekend gap risk)
   Should they use 3-day on Friday?
   
3. "When do these VaRs conflict?"
   "If 1-day VaR is $500k but 10-day is $2M,
    which is the binding limit?"
   
4. "What's the backup if we can't rehedge?"
   "VaR assumes we can exit. What if we can't?"
```

---

## **Building Your Concrete Definition: Time Horizon Edition**

### **Add to Your VaR Definition**

Before you said:
> "VaR is a threshold loss at a specified percentile from historical data."

Now add the horizon clarity:

> "VaR at a specified **time horizon** (e.g., 1 day, 10 days) means:
> The loss where, historically, you'd see worse losses on (100-X)% of those periods.
> 
> Time horizon = how long until you can rehedge/exit/adjust.
> 
> 1-day VaR: Overnight + next daily close → can rehedge tomorrow
> 10-day VaR: 10 trading days → can't rehedge for 10 days (illiquid or crisis)
> 1-month VaR: Monthly rebalancing period → rehedge at month-end
> 
> Longer horizon = bigger loss (compounding). Scale by √T if returns are independent,
> but this breaks when correlations strengthen in crises."

---

## **The Time Horizon Interpretation: Your Checklist**

- [ ] Time horizon = how long until I can rehedge
- [ ] 1-day = overnight through tomorrow close
- [ ] 10-day = 10 trading days of potential holdings
- [ ] 1-month = monthly rebalancing cycle
- [ ] Shorter horizon = smaller VaR (less time to compound)
- [ ] Longer horizon = bigger VaR (more time, more compounding)
- [ ] Scaling rule: VaR_10day ≈ VaR_1day × √10 (if independent)
- [ ] This rule breaks: When correlations, vol regimes, or distributions change
- [ ] Weekend/market closures: Break the rehedging assumption
- [ ] Horizon mismatch: Using 1-day VaR when you can't rehedge for 10 days = dangerous

---

## **Practical Exercise: Interpreting a VaR Statement**

Imagine you see:

### **Statement**
> "Based on 252 trading days of data, the historical 95% daily VaR 
> for the Equities desk is $485k. The 10-day VaR is approximately $1.55M."

### **Your Interpretation**

```
1. Confidence level (95%):
   On 95% of trading days (239 days), losses ≤ $485k
   On 5% of days (13 days), losses > $485k

2. Time horizon (daily):
   Period: From today's close to tomorrow's close
   Rehedging: Assumed you can rehedge tomorrow
   
3. Method:
   Historical: Built from actual 252 days of observed returns
   No assumptions about distribution shape
   
4. The 10-day number ($1.55M):
   $1.55M ≈ $485k × √10 (scaled mathematically)
   Assumption: Daily returns independent and constant volatility
   Reality check: Are they? (Probably not, but close in normal times)
   
5. Interpretation:
   "On 95% of 10-day periods, loss ≤ $1.55M
    On 5% of 10-day periods, loss > $1.55M
    (If we can't rehedge the whole 10 days)"

6. Red flags:
   Missing: What if we can't rehedge between days?
   Missing: What about weekends/halts?
   Missing: What if vol spikes? (√10 rule breaks)
   Missing: What if positions are correlated? (Independence breaks)
```

---

## **Next Question: Confidence Level**

Now that you've understood time horizon:

```
You know:
  ✅ Time horizon = rehedging period
  ✅ Longer horizon = bigger VaR
  ✅ Scaling rule presumes independence
  ✅ Assumptions matter and break

Next: Confidence level

  Why 95% not 99%?
  Why 99% not 99.9%?
  What do these mean?
  How does confidence interact with horizon?
```

Ready to dial into Component 3: Confidence Level?
