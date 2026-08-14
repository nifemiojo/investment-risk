# Feature Deep-Dive: NAV vs Notional

**Artifact**: Risk Snapshot  
**Field**: `nav`  
**Date**: 2026-08-11

---

## What the Number Actually Is

The Risk Snapshot includes the portfolio's NAV (Net Asset Value) — the total market value of the portfolio. This is what investors own. It's the denominator that gives all the risk numbers their scale.

`nav` replaces what was previously called `notional` in both the `Portfolio` and `RiskSnapshot` dataclasses. The rename is deliberate and consistent across all layers.

---

## The Distinction

| Term | Definition | Example (60/40 unlevered) | Example (1.5× levered) |
|---|---|---|---|
| **NAV** (Net Asset Value) | Total market value of the portfolio. What investors own. | £10M | £10M |
| **Notional** / Notional Exposure | Face value of all positions. Gross exposure. | £10M | £15M |

For an unlevered portfolio, NAV and notional are the same number. For a levered or derivatives-heavy portfolio, notional exceeds NAV.

---

## Why NAV, Not Notional

### 1. It's the PM's Language

A PM says "I run a £10M portfolio." They don't say "I run a £10M notional." "Notional" is a risk/derivatives term — it means "the face value of swaps or options" in a PM's head. "NAV" is "what the portfolio is worth."

The field name should match the language the PM uses when they think about it.

### 2. It's the Denominator for Everything

The PM's mental model is built on NAV:

- VaR: 2.18% of NAV → £218K
- Risk budget: 15% of NAV → £1.5M
- Position sizing: 5% of NAV → £500K allocation
- Headroom: "I have 3% of NAV in unused risk budget"

Everything scales off NAV. The field should reflect that central role.

### 3. Consistency Across Layers

The `Portfolio` dataclass, the `RiskSnapshot` dataclass, and the renderer all use `nav`. The PM sees "NAV" in the snapshot display and the same concept flows through the entire system. No translation layer where `Portfolio.notional` becomes visible as "NAV" in the renderer.

### 4. Future-Proof: When Leverage Arrives

If we later add levered portfolios, `nav` remains correct — it's still what the portfolio is worth. We add `gross_notional` as a separate field when the distinction matters. The snapshot doesn't need a rename when that happens.

---

## What the PM Gets From Seeing NAV

### Context for Currency VaR

£218K means nothing without scale. £218K on £1M is catastrophic (21.8% daily VaR). £218K on £100M is sleep-well-at-night (0.22%). The NAV is the frame that gives the currency number meaning.

### Identity Signal

A PM managing multiple portfolios of different sizes sees "NAV: £10,000,000" and immediately knows which mandate they're looking at. It's an identity field as much as `portfolio_name`.

### Drift Awareness

Over time, NAV changes — inflows, redemptions, P&L, currency effects. Seeing it on every snapshot flags growth or shrinkage. A PM who sees NAV drift from £10M to £11M over six months knows their risk budget in currency terms (£1.5M → £1.65M at 15%) has expanded without any policy change.

---

## Why This Decision Was Made Now

The `var-as-pct-of-nav.md` design doc (2026-08-04) explicitly called out the NAV vs notional distinction and noted that for v1 unlevered portfolios they're identical. It used `notional` as the field name with the understanding that both meanings could be derived from it.

The decision to rename to `nav` reflects a design principle: **the PM-facing artifact should use the PM's language, even when the underlying concept is the same number.** The field isn't wrong as `notional` — it's just not how PMs think.

---

## The `var-as-pct-of-nav.md` Document

The earlier design doc (`design/artifacts/risk-snapshot/var-as-pct-of-nav.md`) remains unchanged. It captures the original design thinking about the NAV/notional distinction for levered portfolios. It's a historical record of the analysis that informed this decision. The current document (`nav-vs-notional.md`) is the resolution — the decision we actually made.

---

## Implication for the Data Model

```python
# Portfolio definition (domain layer)
@dataclass(frozen=True)
class Portfolio:
    nav: float                     # 10_000_000 — Net Asset Value
    risk_budget_annual_pct: float         # 0.15 — annualised VaR limit at 95% confidence

# Risk Snapshot (domain layer)
@dataclass(frozen=True)
class RiskSnapshot:
    var_currency: float            # £218,400
    var_pct: float                 # 0.0218
    nav: float                     # 10_000_000 — stored for context and audit
```

When leverage arrives, `gross_notional` joins as a separate field. The PM still reads `nav` and it still means what it always meant.
