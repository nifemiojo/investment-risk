Sharp observation. You're right — the monitoring layer I mapped is all detection. "Something changed." "Risk is here." "Diversification is weakening." None of it actually tells anyone to *do* anything. It's a smoke detector, not a fire plan.

The question is: what's the most natural action decision that flows from VaR monitoring?

---

## The Obvious Candidate: Rebalance

A real systematic portfolio doesn't sit static. Volatilities shift. Correlations shift. A 60/40 capital allocation drifts — sometimes it's 70/30 in risk terms without a single trade.

The decision isn't "should I investigate?" It's:

> **"The portfolio's risk profile has drifted from target. Do I rebalance to restore it, or let it ride?"**

Here's why this is the right v1 action decision:

| Why rebalancing works as the v1 action | Why it's better than just monitoring |
|---|---|
| **It's directly VaR-driven**. Drift is measured in risk terms (VaR contribution per asset), not capital terms. This is the *point* of having the VaR system. | Monitoring says "equity risk is rising." Rebalancing says "equity risk has risen above threshold — reduce SPY by £X to bring it back to target." |
| **It's binary and trackable**. Rebalance or don't rebablance. You can measure the outcome. | You can't measure the outcome of "I decided to investigate." |
| **It's a real PM decision**. Every systematic PM faces this monthly. It's not a contrived problem. | "Should I investigate?" is a meta-decision. It doesn't touch the portfolio. |
| **It changes the portfolio**. The system impacts something. The weights actually move. | Monitoring observes. Rebalancing acts. |
| **It creates a natural decision journal**. "On date X, risk drift was Y. We rebalanced. Next month, risk was back at target." Or: "We didn't rebalance. Drift continued. Drawdown followed." | Every entry has a measurable consequence. |

---

## How the v1 Workflow Changes

The daily Risk Brief doesn't go away — it becomes the **input** to the monthly decision. The Brief is the smoke detector. The Monthly Risk Review is the fire plan.

```
DAILY                           MONTHLY
═════                           ═══════

Risk Brief #1  ──┐
Risk Brief #2  ──┤
Risk Brief #3  ──┤
   ...            ├──→  Monthly Risk Review
Risk Brief #20 ──┤      ─────────────────────
Risk Brief #21 ──┘      │ Risk drift since
                        │ last review
                        │
                        │ Attribution trend
                        │
                        │ Diversification trend
                        │
                        │ RECOMMENDATION:
                        │ Rebalance? Y/N
                        │ If Y: which assets,
                        │ by how much?
                        │
                        └──→ PM DECISION
                             Rebalance or not?
                                │
                             ┌──┴──┐
                             │     │
                            YES   NO
                             │     │
                         Execute  Record
                         trades   rationale
                             │     │
                             └──┬──┘
                                │
                         Next month:
                         Measure outcome
                         (did risk return
                          to target?)
```

The monthly artifact is now the primary decision artifact. The daily briefs are supporting evidence — the trail of data that builds toward the monthly call.

---

## The Monthly Risk Review — Structure

```markdown
╔══════════════════════════════════════════════════════════════╗
║  MONTHLY RISK REVIEW                                        ║
║  Portfolio: 60/40 Multi-Asset | March 2022                  ║
║  Prepared: 31 March 2022                                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  RISK SNAPSHOT                                               ║
║  Portfolio VaR: £241,000 (2.41% of NAV)                     ║
║  vs. Risk Budget: ██████████████████░ 96% utilised  ⚠       ║
║  Change this month: +£32,000 (+15.3%)                       ║
║                                                              ║
║  RISK DRIFT                                                  ║
║                                                              ║
║              TARGET     ACTUAL    DRIFT    ACTION?            ║
║  SPY          40%        52%     +12%     ⚠ REDUCE          ║
║  EFA          20%        24%      +4%     ⚠ REDUCE          ║
║  IEF          25%        16%      −9%     ⚠ ADD             ║
║  GLD          15%         8%      −7%     ⚠ ADD             ║
║                                                              ║
║  Risk concentration: 76% in equities (target: 60%)          ║
║  Diversification ratio: 1.31 (trend: ↓ falling)             ║
║                                                              ║
║  RECOMMENDATION                                              ║
║  Rebalance to target risk allocation.                        ║
║                                                              ║
║  Proposed trades (restore risk targets):                    ║
║  SELL SPY: ~£180,000 (reduce risk contribution)             ║
║  SELL EFA: ~£60,000                                          ║
║  BUY  IEF: ~£200,000 (increase risk contribution)           ║
║  BUY  GLD: ~£100,000                                         ║
║                                                              ║
║  RATIONALE                                                   ║
║  Equity vol has risen 28% this month while bond vol          ║
║  is flat. The equity-bond correlation has risen from         ║
║  −0.28 to +0.05 — bonds are no longer offsetting            ║
║  equity risk. The portfolio is effectively a 75/25           ║
║  in risk terms despite being 60/40 in capital.               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

The PM decision: accept the recommendation and rebalance, or override with a rationale ("I believe equity vol will keep rising — let it drift, we'll review in 2 weeks").

Either way, the decision is recorded, and the outcome is measured at the next review.

---

## The Decision Journal (Now With Teeth)

| Month | Drift detected? | Decision | Action | Next month VaR | Did drift correct? | Notes |
|---|---|---|---|---|---|---|
| Jan 2022 | SPY +3%, IEF −2% (mild) | No rebalance | — | £198K | — (below threshold) | Drift within tolerance band |
| Feb 2022 | SPY +8%, IEF −5% (building) | No rebalance | — | £209K | Drift continued | PM overrode: "vol spike is temporary" |
| Mar 2022 | SPY +12%, IEF −9% (breached) | Rebalance | Sell SPY, buy IEF | £195K (after) | ✓ Returned to target | PM accepted recommendation |
| Apr 2022 | SPY +2%, IEF +1% (normal) | No rebalance | — | £192K | — | Portfolio stable post-rebalance |

This journal is the artifact that proves you understand the loop — not just "I built a VaR system" but "I built a system that drove specific portfolio decisions, and here's what happened."

---

## The Rebalance Decision — Deeper Mechanics

The decision isn't "drift exists → rebalance." That's naive. Real PMs face a trade-off:

| Argument for rebalancing | Argument against |
|---|---|
| Risk is off-target — the portfolio isn't doing what it's designed to do | Rebalancing incurs transaction costs |
| Risk concentration is rising — you're less diversified than you think | Drift might be informative — equities are vol'ing up because something is happening. Cutting exposure means cutting return potential |
| If risk keeps drifting and you don't act, a drawdown hurts more | If the vol spike is temporary, rebalancing into it locks in losses and then you rebalance back when vol falls |

The system should present both sides. The Risk Review includes:
- The drift numbers (objective)
- The recommendation (system output)
- The counterargument (the case for letting it ride)
- The historical context ("last 3 times drift hit this level, rebalancing improved risk-adjusted returns within 3 months")

The PM decides. The system records. The outcome is measured. **That's the loop.**

---

## What Changes in the v1 Scope

| Before (monitoring only) | After (monitoring → rebalance) |
|---|---|
| Primary artifact: Daily Risk Brief | Primary: Monthly Risk Review. Daily Brief becomes input/evidence, not the deliverable. |
| Decision: "Investigate?" | Decision: "Rebalance?" |
| Outcome: not tracked | Outcome: measured — did risk return to target? |
| System role: smoke detector | System role: smoke detector + recommended action |
| Frequency: daily | Daily briefs feed monthly review. Two frequencies, one pipeline. |
| Decision journal: "I investigated this" | Decision journal: "I acted / didn't act on this, and here's what happened" |

The code doesn't change much. The incremental VaR, diversification ratio, change detection — all the same. What changes is the **framing**. The system now produces a *proposal*, not just a *report*.

---

## The Rebalance Logic (Technical Sketch)

The system needs a rule for when to recommend a rebalance. Simple v1 approach:

```
For each asset:
    risk_drift[i] = actual_risk_contribution[i] - target_risk_contribution[i]

If any(|risk_drift[i]| > tolerance_threshold):
    flag = "REBALANCE RECOMMENDED"
    for each asset where |drift| > threshold:
        proposed_trade = rebalance_amount(drift[i], current_value[i])
else:
    flag = "WITHIN TOLERANCE"
```

The `tolerance_threshold` is a parameter — say ±5% of target risk allocation. A ±5% band means SPY at 45% risk contribution doesn't trigger (within band of 40% target). SPY at 47% triggers. This prevents rebalancing on noise.

The `rebalance_amount` translates risk drift back to capital:
- If SPY is 12% over its risk target, the system computes how much SPY to sell to bring its risk contribution back to target
- This requires a model of how changes in position size affect VaR contribution — marginal VaR is exactly this

---

Does this framing work — monthly rebalance as the v1 action decision? Or were you thinking of a different action?