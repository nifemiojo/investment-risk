# How Practitioners Actually Use Parametric VaR — Despite Everything

**Date:** 2026-07-07
**Topic:** Practical decision-making with parametric VaR in contexts relevant to you (Spreadex, dealer, systematic investing, institutional)

---

## The Core Tension

You've now seen the full picture:

```
Parametric VaR is:
  ✅ Simple, fast, universally understood
  ❌ Built on assumptions that are wrong
  ❌ Procyclical
  ❌ Blind to tail events it hasn't seen
  ❌ Fragile to correlation breaks
  ❌ Reported with false precision
```

And yet — every major bank, dealer, hedge fund, and asset manager uses it. Every day. For real decisions.

**Why? And how?**

---

## The Practitioner's Relationship With VaR: Four Truths

### Truth 1: VaR Is Not a Forecast — It's a Common Language

Practitioners don't use VaR to predict tomorrow's loss. They use it because everyone else uses it. It's the **lingua franca** of risk.

```
Regulator: "What's your market risk?"
You:      "95% 1-day VaR is £1.2M"
Regulator: "Understood. Capital requirement is 3× VaR."

Counterparty: "What's your exposure to us?"
You:         "VaR of our position with you is £400k."
Counterparty: "Understood. We'll post £500k margin."

Board: "How much risk are we taking?"
You:   "VaR is running at £1.2M, inside the £2M limit."
Board: "Understood. Carry on."
```

The value isn't the number's accuracy. It's that everyone agrees on the **definition** and can act on it. VaR is a coordination device, not a prediction.

---

### Truth 2: VaR Is a Speedometer, Not a GPS

```
GPS:         "Turn left in 200m, arrive at 2:15pm"
             → Prediction. Specific. Wrong if road is closed.

Speedometer: "You're going 65 mph"
             → Measurement. Tells you current state. 
             → Doesn't tell you where to go, but you'd be stupid to ignore it.
```

VaR is a speedometer. It tells you: "At current volatility and positions, under normal conditions, this is the boundary of your 95% range."

It does NOT tell you:
- Where to go (what to trade)
- Where the potholes are (tail events)
- Whether the road is closing (regime change)

Practitioners use it as a **current-state measurement**, not a forecast. You check it, you don't navigate by it.

---

### Truth 3: VaR Is a Conversation Starter, Not a Conversation Ender

When VaR changes, the right response is not "adjust position." It's **"why?"**

```
Scenario A:
  VaR jumps from £1.2M to £1.8M.
  Investigation: equity vol up 30%, correlation with bonds shifted.
  Decision: "Makes sense given the macro. Position is fine. Monitor."

Scenario B: 
  VaR jumps from £1.2M to £1.8M.
  Investigation: one trader put on a massive concentrated bet in small-caps.
  Decision: "This is not what we signed up for. Reduce."

Scenario C:
  VaR stays at £1.2M. No change.
  Investigation: equity vol up 40% but trader reduced positions.
  Decision: "Nice. Trader adjusted before VaR forced it. Give them more capacity."
```

Same VaR number. Three different responses. The number started the conversation — it didn't end it.

---

### Truth 4: VaR Is a Fence, Not a Wall

A VaR limit of £2M doesn't mean "never exceed £2M." It means:

```
£0-1.5M:    Green zone. No questions asked.
£1.5-2M:    Yellow zone. Heads-up to risk manager.
£2M:        The fence. You can go over, but you need a conversation.
£2-2.5M:    Red zone. Active discussion required. Must have a plan to reduce.
£2.5M+:     Hard stop. Reduce immediately.
```

The fence has a gate. The limit is a **trigger for a conversation**, not an automatic constraint. This is critical because automatic VaR-based limits create the procyclical feedback loop (failure mode 6). The human override breaks the loop.

---

## How Practitioners Use VaR in Specific Contexts

### Context 1: Dealer Risk Management (Spreadex)

**What you're managing:** Customer flow, hedging decisions, multi-asset book, intraday positions.

**How VaR is used:**

```
LAYER 1: Overnight risk budget
  "You can hold up to £X VaR of inventory overnight."
  → VaR sets the risk budget. Not the position limit — the risk budget.
  → A diversified book of 50 small positions can have the same VaR as one concentrated bet.

LAYER 2: Hedge sizing
  "Book VaR is £800k. We want to be hedged to £400k."
  → VaR tells you the gap between where you are and where you want to be.
  → Not used to size the hedge mechanically — used to frame the decision.

LAYER 3: New product approval
  "Adding a new FX pair. What does it do to book VaR?"
  → VaR shows the marginal risk contribution.
  → "This pair adds £50k VaR but is uncorrelated with everything else. Approved."
  → "This pair adds £50k VaR but is highly correlated with existing positions. Needs discussion."
```

**The key insight for dealers:** VaR is used to measure **risk concentration**, not just risk level. A book with £1M VaR from 100 independent positions is very different from a book with £1M VaR from one position. Same number, different risk.

---

### Context 2: Systematic Investing / Portfolio Construction

**What you're managing:** Portfolio allocation, factor exposures, risk budgeting.

**How VaR is used:**

```
RISK BUDGETING (not capital allocation):

Traditional: "60% equity, 40% bonds"
Risk-based:  "50% of risk budget to equity, 50% to bonds"

This means:
  Equity VaR = 50% × total portfolio VaR
  Bond VaR = 50% × total portfolio VaR
  
  If equity vol is 3× bond vol, you hold LESS equity:
    Equity allocation: 25% of capital (but 50% of risk)
    Bond allocation: 75% of capital (but 50% of risk)
```

**Why this matters:** Risk parity and similar strategies use VaR (or vol) to determine position sizes. The goal is balance the **risk contribution** of each asset, not the capital allocation.

**The connection to your thinking:** This is closely related to the Wealth-Income framework from your notes — objectives define spending, spending defines risk budget. VaR is the metric that makes the risk budget operational.

---

### Context 3: Institutional / Sovereign Wealth (Your Direction)

**What you're managing:** Long-horizon portfolios, multiple asset classes, governance requirements.

**How VaR is used:**

```
GOVERNANCE LAYER: Board-level risk appetite

Board: "We're comfortable with a 95% annual VaR of 8%."
       → This is a policy statement, not a trading limit.

Investment team: "Current portfolio 95% annual VaR is 6.2%."
       → We're inside the envelope. We can take more risk.

Investment team: "The new private equity allocation would add 1.5% VaR."
       → Total would be 7.7%. Still inside 8%. Approved.

Board: "Show us stress test results."
       → VaR is the communication tool. Stress tests are the real risk control.
```

**The key insight:** At this level, VaR is used for **governance and communication**, not for trading. The board doesn't trade — they set the risk appetite. VaR translates that appetite into something the investment team can act on.

---

## The Multi-Layered Defense: How Practitioners Live With VaR's Flaws

No practitioner uses parametric VaR alone. They use it inside a **defense-in-depth** system:

```
LAYER 1: Parametric VaR (normal, EWMA, daily)
  → Fast, simple, universal. First alert.
  → "Something might be changing."

LAYER 2: Multiple VaR variants (triangulation)
  → Normal VaR, t-distribution VaR, Cornish-Fisher VaR
  → Different windows (60-day, 252-day, 500-day)
  → If they agree → model is stable. If they diverge → investigate.

LAYER 3: Expected Shortfall
  → "VaR says -1.3%. But when it breaches, the average loss is -2.1%."
  → ES is the real risk number. VaR is just the threshold.

LAYER 4: Stress testing
  → "What if we replay 2008? What if vol doubles? What if correlations go to 1?"
  → These are the scenarios VaR can't see.
  → Stress tests are the counter-cyclical anchor.

LAYER 5: Backtesting
  → Kupiec test, Christoffersen test, traffic light system
  → "Is the model actually working?"
  → Catches silent drift (failure mode 4).

LAYER 6: Human judgment
  → "VaR says we're fine. But it feels like 2007. I'm reducing."
  → The ultimate circuit breaker.
```

---

## The Decision Flow: A Real Example

```
MORNING RISK MEETING — 8:30 AM

1. DESK HEAD: "Yesterday's 95% VaR closed at £1.2M. Inside the £2M limit."
   → VaR as speedometer. Current state check.

2. RISK MANAGER: "EWMA σ̂ jumped 15% overnight. If today trades like yesterday,
   VaR will open at £1.35M. Still inside limit but moving up."
   → VaR as early warning. Trend, not level.

3. QUANT: "Normal VaR says £1.2M. t-distribution (ν=4) says £1.45M. 
   Cornish-Fisher says £1.38M. Spread is widening."
   → Triangulation. Divergence = signal.

4. TRADER: "I'm seeing heavy put buying in the options market. 
   Implied vol is above realized. Market is pricing in a move."
   → External signal. VaR doesn't capture this.

5. DESK HEAD: "OK. Reduce position in the concentrated small-cap bet 
   by 30%. Keep the diversified macro positions. If VaR hits £1.5M 
   before lunch, we meet again."
   → Decision. VaR informed the conversation, didn't dictate it.

6. END OF WEEK: Backtest report shows 7 breaches in 252 days.
   Expected: 12.6. We're in green territory (Kupiec test).
   → Model is actually conservative. Good.
```

---

## What This Means for You

At Spreadex, you're not going to be the person who computes VaR. You're going to be the person who **interprets** it.

The skill is:
1. Know what VaR is actually measuring (and what it's not)
2. Know its failure modes and watch for them
3. Use it to start conversations, not end them
4. Triangulate — never trust a single number
5. Understand that the limit is a fence with a gate, not a wall

---

## The Practitioner's Summary

| Question | Answer |
|---|---|
| Is parametric VaR "correct"? | Almost never. That's not the point. |
| Then why use it? | Common language. Starts conversations. |
| What SHOULDN'T it be used for? | Predicting tail losses. Setting hard limits. Automated trading without override. |
| What SHOULD it be used for? | Risk budgeting. Concentration measurement. Governance communication. Trend monitoring. |
| How do you survive using it? | Layer it with ES, stress tests, backtesting, and human judgment. |

---

## Check-In

You're at Spreadex. The autohedge system is probably using parametric VaR to size hedges. Given everything we've covered, what's the one question you'd want to ask the quant who built it about how they use VaR?