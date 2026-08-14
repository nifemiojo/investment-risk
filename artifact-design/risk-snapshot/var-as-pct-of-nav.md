# Feature Deep-Dive: VaR as Percentage of NAV

**Artifact**: Risk Snapshot  
**Field**: `var_pct`  
**Date**: 2026-08-04

---

## What the Number Actually Is

`var_pct` is the (negated) quantile of the portfolio return distribution. If the 5th percentile of historical daily portfolio returns is −2.18%, then the 95% daily VaR is 2.18% of NAV.

For an unlevered portfolio where NAV = notional, the return distribution quantile and the NAV percentage are the same number. This identity — *the quantile of returns IS the percentage of NAV at risk* — is why the percentage works as a universal risk language. The return distribution is scale-free.

---

## Why a PM Wants to See Percentage (Not Just Currency)

### 1. It's the Budget Language

The Investment Policy Statement doesn't say "daily VaR shall not exceed £1.5M." It says "15% annualized VaR at 95% confidence." The budget is written in percentages because percentages survive portfolio growth, inflows, redemptions, and NAV drift. A currency limit would need renegotiation every time the portfolio size changed.

The PM thinks in percentages because the governance framework thinks in percentages.

### 2. It Strips Out Scale Effects

| What the PM sees | What it actually means |
|---|---|
| VaR rose from £200K to £240K | Could mean risk increased. Could mean the portfolio grew from £10M to £12M and risk per unit is identical. |
| VaR rose from 2.0% to 2.4% | Risk per unit genuinely increased. NAV is stripped out. Pure risk signal. |

The currency number conflates risk changes with size changes. The percentage isolates the risk change. A PM who only looks at currency VaR will misinterpret portfolio growth as rising risk and portfolio shrinkage as risk reduction.

### 3. It Enables Cross-Portfolio Comparison

A PM running a £10M 60/40 portfolio and a £50M risk parity portfolio can't compare £218K to £400K and know which is riskier. But 2.18% vs. 0.80% tells them immediately: the 60/40 is taking 2.7× more risk per unit of capital.

This matters for:
- **Risk allocation**: "I have two sleeves — am I deploying risk evenly?"
- **Strategy evaluation**: "Is the risk parity strategy actually delivering lower risk per unit?"
- **Manager comparison**: In a multi-manager setup, percentages make risk-taking comparable across mandates

### 4. It's How the PM Builds Intuition

A PM who sees "2.18% daily VaR" enough times builds a mental calibration:

> *At 2.18% daily VaR at 95% confidence, I expect to lose more than 2.18% on roughly one day per month (~13 days per year). That's about £218K on a £10M portfolio. A 3σ event would be roughly 3× that — ~£650K. If the market gaps 5%, I'm looking at £500K — within my stress scenario but outside my daily VaR expectation.*

This intuition is scaffolded on percentages, not currency. The currency number follows from the percentage × NAV. The percentage is the mental model; the currency is the consequence.

### 5. It Survives Regime Changes

In a high-vol regime, a PM managing a fixed-size portfolio sees currency VaR spike. The percentage captures the same spike. But in a *growing* portfolio in a *declining vol* regime, the currency VaR might be flat (scale up, vol down) while the percentage VaR is falling. The PM needs the percentage to know that risk per unit is actually declining — they have capacity to deploy.

The percentage is the signal that says: *"You have more risk budget available than you think."*

---

## Percentage vs. Currency: Which for What Decision

| Decision | Uses | Why |
|---|---|---|
| "Am I within my risk budget?" | Percentage | The budget is stated as a percentage. `var_pct / risk_budget_pct → utilisation` |
| "Is risk rising or falling?" | Percentage | Strips out NAV effects. Pure signal. |
| "How does this portfolio compare to my other sleeve?" | Percentage | Cross-portfolio comparison only works when normalized. |
| "What should I tell the IC?" | Percentage | Governance language. "We're running at 82% utilisation." |
| "How much SPY do I need to sell to reduce risk?" | Currency | Trade sizing needs absolute numbers. |
| "What's my actual loss exposure tonight?" | Currency | The PM goes home thinking in pounds. |
| "How much headroom do I have for a new position?" | Both | Headroom as % tells you budget remaining. Headroom as currency tells you how much you can actually buy. |

The percentage is the **assessment** number. The currency is the **action** number. The Snapshot shows both because the PM needs both — but they serve different moments in the decision flow.

---

## The Normalization Question

`var_pct` as a percentage of NAV works cleanly for unlevered portfolios:

| Portfolio type | What `var_pct` means | Gotcha |
|---|---|---|
| Unlevered 60/40 (£10M NAV, £10M notional) | 2.18% of NAV at risk | Clean. Return distribution quantile = NAV percentage. |
| Levered (e.g., 1.5×, £10M NAV, £15M notional) | 2.18% of *notional* at risk, which is 3.27% of NAV | Need to be explicit: is this % of NAV or % of exposure? |
| Long/short (gross exposure > NAV) | Same issue | Return distribution is computed on NAV. The % is % of NAV — but the PM also needs % of gross. |

For v1 (unlevered 60/40), this isn't an issue. But the data model is explicit: `var_pct` is percentage of NAV, and `notional` is stored alongside it. If the portfolio becomes levered, both numbers exist to calculate either view.

---

## Implication for the Data Model

The `RiskSnapshot` stores both:

```python
var_currency: float    # £218,400 — the action number (trade sizing, loss exposure)
var_pct: float         # 0.0218   — the assessment number (budget, comparison, intuition)
notional: float        # 10_000_000 — stored so var_pct can be derived and audited
```

Neither is redundant. The currency isn't just `var_pct × notional` — it's independently meaningful as the number the PM uses to size trades and think about loss exposure. The percentage isn't just `var_currency / notional` — it's the number that connects to the governance framework. Both earn their place.