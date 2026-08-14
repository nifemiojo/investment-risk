# Feature Deep-Dive: Annualising VaR for Budget Comparison

**Artifact**: Risk Snapshot  
**Fields**: `var_annualised_pct`, `risk_budget_annual_pct`, `budget_utilisation`  
**Date**: 2026-08-11

---

## What Happens

The engine computes a daily VaR (1.11% of NAV) from historical returns. It then annualises it using the square-root-of-time rule:

$$\text{Annualised VaR} = \text{Daily VaR} \times \sqrt{252}$$

and compares it to the annual risk budget:

$$\text{Utilisation} = \frac{\text{Annualised VaR}}{\text{Risk Budget}} = \frac{17.6\%}{15\%} = 118\%$$

---

## Why Annualise At All?

### The Budget Is Set Annually By Governance

The Investment Policy Statement says "15% annualised VaR at 95% confidence" — not "0.94% daily VaR." Governance thinks in annual terms:

- Clients evaluate outcomes in annual returns
- The IC reviews budgets annually
- "15% annual" is the common language across asset classes, firms, and regulators

If we expressed the budget in daily terms (0.94% = 15% ÷ √252), we'd create a gap between "what the IPS says" and "what the snapshot shows." The PM would have to mentally convert back to explain utilisation to the IC. Better to keep the budget in its governance-native units and make the annualisation explicit.

### The PM Operates in Both Units

| Horizon | Number | Used for |
|---|---|---|
| Daily | 1.11% VaR | Operational intuition. "What could I lose tomorrow?" Trade sizing. |
| Annual | 17.6% VaR | Governance. Budget comparison. IC reporting. "Am I within mandate?" |

Both matter. The daily number is what the PM experiences day to day. The annual number is what connects to the governance framework. The snapshot shows both.

---

## The Square-Root-of-Time Rule

$$\sigma_{\text{annual}} = \sigma_{\text{daily}} \times \sqrt{252}$$

This is an industry convention, not a fact. It assumes:

1. **Returns are i.i.d.** — identically and independently distributed. Each day's return is drawn from the same distribution and doesn't depend on the previous day.
2. **Normality** — the scaling works exactly for variance under independence, but VaR isn't variance (it's a quantile), and the normality assumption is what makes the quantile scale the same way.

Neither assumption holds in reality:
- Volatility clusters (calm periods followed by turbulent periods)
- Returns have fat tails (extreme events happen more often than normality predicts)
- Autocorrelation exists (especially in less liquid assets)

**So why use it?** Because there isn't a universally accepted better alternative. Every risk system in the industry uses √t scaling. The alternatives all have their own problems:

| Alternative | Problem |
|---|---|
| Compute VaR directly on annual returns | Very few data points (10 years = 10 data points). Noisy and unreliable. |
| Scale using a different factor | Which factor? Data-mined factors don't survive out-of-sample. |
| Don't annualise — use daily budget | Creates a governance gap. The IC doesn't think in daily terms. |

The √252 convention is the least bad option — universally understood, mechanically simple, and doesn't introduce additional parameters to fit.

Is it precisely correct? No. Does it still produce useful comparisons? Yes — especially when the PM understands what it does and doesn't assume.

---

## Why the Annualised VaR Is Now Visible

Previously, the engine silently applied √252 and the PM only saw the utilisation result (118%). The annualised VaR itself (17.6%) was invisible.

The snapshot now shows:

```
### Risk Budget
Annualised VaR: 17.6% of NAV  |  Limit: 15% of NAV
███████████████████████ 118% utilised
```

This makes the annualisation step **visible and verifiable**. The PM can check: "Does 1.11% daily × √252 = 17.6%?" Yes. "Is 17.6% ÷ 15% = 118%?" Yes. The arithmetic is transparent.

---

## What the √252 Factor Actually Is

252 is the conventional number of trading days in a year. It's not exact — some years have 250, some 253, and holidays vary by market. But 252 is the convention for US equities and is used universally.

For other markets: 250 (UK), 245 (some European markets). The engine uses 252 for simplicity. If we ever support multiple markets, it becomes a per-portfolio parameter.

---

## The Display Explanation

Under the Risk Budget heading, the snapshot includes:

> *Limit = 15% annualised VaR at 95% confidence — the maximum loss the mandate allows in a typical year, set by the Investment Policy Statement.*

This does three things:

1. **Grounds the number** — "15% of what?" → "15% of NAV annualised"
2. **Names the source** — "Where does this limit come from?" → "The IPS"
3. **Defines the confidence** — "At what confidence?" → "95%"

Anyone reading the snapshot cold understands what the Risk Budget section means without needing prior context.

---

## The `risk_budget_annual_pct` Field Name

Previously `risk_budget_pct`. Renamed to `risk_budget_annual_pct` because:

- **Carries the frequency in the name** — removes ambiguity about whether it's daily or annual
- **Matches the governance language** — the IPS says "annualised"
- **Self-documenting** — a new developer reading the code knows immediately what unit this is in

---

## Summary

| Decision | Rationale |
|---|---|
| Keep √252 annualisation | Budget is annual in governance. Industry convention. Alternatives are worse. |
| Show annualised VaR in display | Makes the transformation visible and verifiable. |
| Daily VaR stays visible | PM's operational intuition lives in daily terms. |
| Show limit alongside utilisation | "118%" needs a referent. |
| 1-2 sentence explanation | Grounds the section for any reader. |
| `risk_budget_annual_pct` naming | Carries frequency. Self-documenting. |
