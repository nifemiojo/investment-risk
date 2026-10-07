# Attribution Design Decision: Remove Diversification Benefit

**Artifact**: Attribution  
**Date**: 2026-08-18  
**Status**: Decision recorded  

---

## Decision

Remove the diversification-benefit metric from the Attribution artifact.

The earlier design included a portfolio-level summary based on standalone volatility and portfolio volatility. That metric is not needed for Attribution because it does not help answer the artifact's core question:

> **Where does risk live, and which positions should the PM investigate first?**

The previous design documents are retained as historical reasoning. This document records the final decision for the current design.

---

## Why it does not belong in Attribution

Attribution is a position-level investigation-routing artifact. Its job is to show:

- which positions generate the largest share of current portfolio risk;
- whether a position's risk contribution is disproportionate to its weight;
- which positions are volatile or highly correlated with the rest of the portfolio;
- which positions are offsetting portfolio risk;
- where the PM should look next.

A diversification-benefit summary is different. It is a portfolio-level structural diagnostic. It may describe how the portfolio behaves as a whole, but it does not identify the position that should be investigated first.

Including it would broaden the artifact away from its decision and make the display answer two different questions:

```text
Where does risk live?
```

and:

```text
How much diversification does the portfolio provide overall?
```

The second question may be valuable, but it belongs in a future diversification-focused artifact rather than in Attribution.

---

## What remains in Attribution

The core Attribution output remains:

- portfolio volatility, as the total being decomposed;
- ranked component contribution by asset;
- component contribution as a percentage of total portfolio risk;
- component contribution in volatility units;
- portfolio weight;
- contribution-versus-weight contrast;
- standalone volatility as supporting diagnosis;
- concentration summaries such as top-one and top-two contribution;
- positive or negative contributions, including diversifying positions;
- a descriptive focus summary that routes the PM's attention without prescribing a trade.

The artifact continues to answer:

> **Which positions should the PM investigate first, and what should they understand about each position's role in portfolio risk?**

---

## What is removed

The following are removed from the current Attribution design and data model:

- `standalone_sum` as a portfolio-level field;
- `diversification_benefit`;
- `diversification_ratio`;
- the diversification-benefit section in the display;
- any interpretation such as “X% of risk diversified away.”

Standalone volatility remains at the asset level because it helps distinguish a volatile asset from an asset whose contribution is driven primarily by its relationship with the rest of the portfolio. That is directly relevant to position-level investigation.

---

## Future destination

A weight-aware diversification measure may be revisited in a separate artifact whose explicit question is:

> **How much diversification does the portfolio provide, and how has that changed across market conditions?**

That future artifact could consider measures such as:

- a weighted perfect-correlation reference;
- a diversification ratio;
- relative volatility reduction;
- diversification changes through time;
- correlation-regime analysis.

Those measures should be designed around that portfolio-level decision rather than added to Attribution by default.

---

## Updated visual design

The v1 display is intentionally focused on the PM's position-level investigation decision. It shows the total risk being decomposed, the ranked contributors, the contribution-versus-weight contrast, the standalone-risk diagnostic, and the next place to look.

It does **not** include a diversification-benefit panel or a portfolio-level diversification ratio.

```text
╔══════════════════════════════════════════════════╗
║  STRUCTURAL RISK ATTRIBUTION                     ║
║  60/40 Multi-Asset                               ║
║  14 March 2022 · Close                           ║
║  Component contribution to volatility · daily    ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  PORTFOLIO RISK                                  ║
║  Volatility: 2.0% daily                          ║
║  Historical VaR is not decomposed here           ║
║                                                  ║
║  WHERE DOES RISK LIVE?                           ║
║  Ranked by contribution to portfolio risk        ║
║                                                  ║
║  SPY  40% wgt  ████████████░░░░  62% of risk     ║
║       +22 percentage points vs weight            ║
║  EFA  20% wgt  ██████░░░░░░░░░░  21% of risk     ║
║       +1 percentage point vs weight              ║
║  IEF  25% wgt  ░░░░░░░░░░░░░░░░  -1% of risk     ║
║       -26 percentage points · diversifier        ║
║  GLD  15% wgt  ██░░░░░░░░░░░░░░  18% of risk     ║
║       +3 percentage points vs weight              ║
║                                                  ║
║  CONCENTRATION                                   ║
║  Top 1 asset: 62% of risk                        ║
║  Top 2 assets: 83% of risk                       ║
║                                                  ║
║  WHY DOES THE RANKING LOOK LIKE THIS?            ║
║  Asset       Standalone vol   Risk contribution  ║
║  SPY         1.1%             62%                ║
║  EFA         0.9%             21%                ║
║  IEF         0.4%             -1%                ║
║  GLD         0.7%             18%                ║
║                                                  ║
║  NEXT INVESTIGATION                              ║
║  Focus: SPY — risk contribution is              ║
║         disproportionate to its weight.         ║
║  Check next: volatility, correlation, and drift. ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

### Display principles

1. **Lead with the decision** — the first question is where the PM should look, not whether a portfolio-level diversification score is high or low.
2. **Show contribution against weight** — the contrast identifies hidden concentration without declaring that the allocation is wrong.
3. **Keep standalone volatility diagnostic** — it helps distinguish a high-contribution asset because it is volatile from one whose contribution is driven by correlation with the portfolio.
4. **Make negative contribution visible** — a diversifier should not be hidden or treated as a calculation error.
5. **End with a route, not a trade** — “focus on SPY” is supported; “reduce SPY” belongs to drift and rebalance analysis.
6. **State the decomposition boundary** — the artifact decomposes structural volatility, not the Snapshot's historical VaR headline.

## Consequence for v1

The first Attribution implementation should focus only on the component-contribution pipeline and the information needed to rank and interpret asset-level risk.

No diversification-benefit calculation is required for the v1 Attribution engine, data model, or display.

This keeps the artifact aligned with its decision, reduces interpretive burden, and avoids implementing a metric before there is a clearly defined portfolio-level decision for it to support.

---

## Final design position

> **Attribution is a point-in-time, asset-level decomposition of structural portfolio volatility. It identifies where risk lives and which positions deserve investigation. Portfolio-level diversification benefit is out of scope and deferred to a future diversification-focused artifact.**
