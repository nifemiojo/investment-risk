# Feature Deep-Dive: Risk Budget & Utilisation

**Artifact**: Risk Snapshot  
**Fields**: `risk_budget_pct`, `budget_utilisation`, `is_breach`, `headroom_pct`  
**Date**: 2026-08-04

---

## What "Budget" Means in Finance

When you hear "budget," your brain probably goes to cash: *"I have £10,000 to spend this quarter."* That's a **capital budget** — a constraint on how much money you can deploy.

A risk budget is different. It's a constraint on how much **uncertainty** you can deploy.

The Investment Policy Statement doesn't say "you may invest up to £10M." It says:

> *"The portfolio shall operate within a 15% annualized Value-at-Risk limit at 95% confidence."*

This is a risk budget. It doesn't limit how much capital you deploy — it limits how much loss you're allowed to expose the portfolio to. Capital is the raw material. Risk is what you do with it.

---

## Capital Allocation vs. Risk Budgeting

The core mental model shift:

| Capital allocation thinks in... | Risk budgeting thinks in... |
|---|---|
| "Put 60% of the money in equities" | "Take 60% of the risk from equities" |
| Weights are static — 60/40 is 60/40 | Weights are dynamic — a 60/40 capital portfolio becomes 75/25 in risk terms when equity vol spikes |
| A 10% position is a 10% position | A 10% capital position could be 5% of the risk (bonds in calm markets) or 25% of the risk (equities in a crash) |
| The PM asks: "How much should I buy?" | The PM asks: "How much risk am I taking on, and is it worth it?" |

Concrete example — same 60/40 portfolio (SPY/IEF), two regimes:

| | Calm regime (2024) | Stress regime (Mar 2020) |
|---|---|---|
| SPY daily vol | 0.8% | 4.5% |
| IEF daily vol | 0.4% | 1.2% |
| SPY-IEF correlation | −0.3 | +0.1 |
| **Capital allocation** | 60% SPY, 40% IEF | 60% SPY, 40% IEF *(unchanged)* |
| **Risk contribution** | SPY: ~55%, IEF: ~45% | SPY: ~82%, IEF: ~18% |

The capital allocation hasn't moved. No trades. But the risk allocation has shifted dramatically. Capital weights lie. Risk weights tell the truth. **This is why risk budgeting exists.**

---

## Where the Risk Budget Comes From

The risk budget isn't the PM's personal preference. It flows from governance:

```
Client Mandate
  │  "We want long-term growth with moderate risk.
  │   Max drawdown of 20% in any 12-month period."
  ▼
Investment Policy Statement
  │  Translates client preferences into measurable constraints:
  │  "Portfolio shall operate within 15% annualized VaR
  │   at 95% confidence. No single asset class shall
  │   contribute more than 60% of total VaR."
  ▼
Portfolio Manager
  │  Operates within those constraints.
  │  Deploys the risk budget across positions.
  │  Monitors utilisation.
  │  Reports to IC.
  ▼
Investment Committee
  │  Reviews risk budget utilisation.
  │  Adjusts the budget if the mandate changes.
  │  Holds the PM accountable for breaches.
```

The PM didn't choose 15%. The client's risk tolerance, filtered through the IPS, produced 15%. The PM's job is to **deploy that 15% efficiently** — to take risk where it's compensated and avoid risk where it isn't.

---

## What Utilisation Means

`budget_utilisation = var_pct / risk_budget_pct`

| Utilisation | What it means | PM's situation |
|---|---|---|
| 30% | The portfolio is taking very little risk relative to its mandate. | "I'm being too conservative. The client is paying me to take risk and I'm not deploying it. I need to add positions or explain to the IC why I'm underweight risk." |
| 60–80% | Normal operating range. Risk is deployed, headroom exists. | "I'm doing my job. I have room to add a new position if I see an opportunity." |
| 85–95% | Elevated. Approaching the limit. | "I need to be careful. Any new position needs to come with a corresponding reduction elsewhere. I'm capacity-constrained." |
| 100%+ | Breach. The portfolio has exceeded its mandate. | "This is a formal breach. I must reduce risk or get IC approval for an override. This will be recorded. Clients may need to be informed." |

The sweet spot for an active PM is roughly 70–90%. Enough deployed to generate returns. Enough headroom to act on opportunities without hitting the limit. Below 50%, the IC asks: *"Why are we paying you to manage risk you're not taking?"* Above 95%, the IC asks: *"Are you about to breach our mandate?"*

---

## The PM's Decisions Around Utilisation

### Decision 1: Can I add this position?

> *"My analyst has a strong conviction call on EM equities. I'd like to add 5% exposure. Current utilisation is 82%. Adding EM would push me to ~90%. That's within operating range — but I'd only have 10% headroom after. If vol spikes, I breach. Is the idea worth the reduced capacity?"*

Every new position consumes risk budget. The risk budget is the scarce resource, not capital.

### Decision 2: Should I reduce something to make room?

> *"I'm at 93% utilisation and I want to add EM. I can't add without reducing something else. Which position is consuming risk without generating returns? EFA is contributing 22% of risk but has underperformed for 3 quarters. Reduce EFA by £X → frees up Y% risk budget → deploy into EM."*

Risk budgeting as **portfolio discipline**. It forces the PM to justify every unit of risk: "Am I being compensated for this risk?" If not, redeploy.

### Decision 3: Is current utilisation appropriate for the environment?

> *"We're in a low-vol regime. VaR is at 8.5% vs. 15% budget. I'm at 57% utilisation. This looks like under-deployment, but I believe vol is artificially suppressed and a spike is coming. If I add risk now, I'll breach when vol normalises. I'll stay at 57% and document my rationale for the IC."*

The PM isn't a slave to the utilisation number. They can run below budget with a documented rationale. "I'm being cautious" is not a rationale. "Forward-looking vol estimates suggest regime shift" is.

### Decision 4: Am I in breach, and what do I do about it?

> *"VaR hit 15.8% vs. 15% limit. I'm in breach. This is a formal event — IC must be notified within 24 hours. Options: (1) reduce positions immediately, (2) request a temporary override from IC, (3) argue the breach is technical (vol spike will fade). The safest path: reduce the largest risk contributor by £X to bring utilisation below 100%. Document everything."*

A breach isn't a failure — it's an event that triggers a protocol. What matters is how the PM responds.

---

## The Business Perspective: Why This Matters

### 1. It's the Fiduciary Contract

The client gave the manager capital with conditions attached. Those conditions are expressed as a risk budget. The manager's job isn't just to generate returns — it's to generate returns **while staying within the risk budget**. If the manager breaches, they've violated the fiduciary contract, regardless of whether they made money.

A PM who returned 25% but breached the risk limit three times is in more trouble than a PM who returned 12% and stayed within limits. The first PM got lucky; the second PM did their job.

### 2. It Forces Explicit Thinking About Risk-Return Trade-offs

Without a risk budget, a PM can always justify one more position. "It's a good idea, let's add it." The budget says: *"You have finite risk capacity. Every unit of risk you deploy must earn its place. What are you giving up to add this?"*

This is the difference between a PM and a trader. A trader adds positions based on conviction. A PM allocates a scarce resource (risk budget) across positions based on risk-adjusted conviction.

### 3. It Prevents the Worst Outcome: Forced Liquidation

The nightmare scenario: being forced to sell into a falling market because of a risk limit breach. This crystallizes losses at the worst possible moment. The risk budget, properly monitored, prevents this. It gives the PM time to reduce risk gradually before it becomes an emergency.

### 4. It's the Governance Trail

When the IC reviews the portfolio quarterly, they look at risk budget utilisation over time:

> *"You were at 90%+ utilisation for six consecutive months. You had no capacity to act on opportunities. Why didn't you request a budget increase or reduce positions to create headroom?"*

The utilisation history IS the governance record. It shows whether the PM was managing risk actively or just letting it drift.

### 5. It's How Institutional Portfolios Are Actually Built

At an AQR-type firm, risk budgeting isn't just a constraint — it's the **construction principle**. A risk parity portfolio doesn't allocate 25% capital to each of four assets. It allocates 25% of the **risk budget** to each. The capital weights are whatever they need to be to achieve that — and they change constantly.

---

## Concrete Walkthrough: Utilisation Over Time

Tracing utilisation through the 2020–2024 replay:

| Date | VaR % | Budget % | Utilisation | What's happening |
|---|---|---|---|---|
| Jan 2020 | 8.2% | 15% | 55% | Calm markets. PM has plenty of headroom. |
| Mar 2020 | 18.6% | 15% | **124% BREACH** | COVID crash. Vol exploded. PM must reduce or get IC override. |
| Apr 2020 | 14.2% | 15% | 95% | Vol fading but still elevated. PM reduced positions in March. Tight but within limits. |
| Jun 2020 | 10.1% | 15% | 67% | Recovery rally. Vol normalising. PM has headroom again. |
| Jan 2022 | 11.3% | 15% | 75% | Normal. Inflation concerns building but vol hasn't spiked yet. |
| Mar 2022 | 14.8% | 15% | 99% | Rates shock. Bonds selling off alongside equities. Diversification breaking down. |
| Oct 2022 | 13.2% | 15% | 88% | PM reduced equity exposure in summer. Better position now. |
| Dec 2024 | 9.5% | 15% | 63% | Calm. PM has room. |

The utilisation number tells the story of the PM's decisions. 55% → 124% → 95% → 67% → 75% → 99% → 88% → 63%. Each number is the consequence of a market event and a PM response. The utilisation history IS the decision trail.

---

## The Simple Mental Model

> **Risk budget is the PM's working capital. It's measured in units of permissible loss, not pounds. Deploy it where you have edge. Preserve headroom for opportunity. Never breach without a plan. Document everything.**

The Risk Snapshot's `budget_utilisation` and `headroom_pct` fields give the PM this information in a single scan. Combined with `is_breach`, it answers: *"Can I act, or am I constrained?"*