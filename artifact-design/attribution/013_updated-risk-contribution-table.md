# Attribution Design Decision: Evidence-Only Output

**Artifact**: Attribution  
**Date**: 2026-08-18  
**Status**: Decision recorded  

---

## Decision

For v1, Attribution returns **the evidence only**.

It should calculate and present the asset-level decomposition clearly, but it should not generate descriptive observations or route the PM into downstream workflow steps.

The artifact's purpose is:

> **Attribution provides a transparent, ranked decomposition of current structural portfolio volatility into asset-level evidence. The PM interprets that evidence and decides what, if anything, warrants further investigation.**

This keeps the artifact focused on answering:

> **Where does risk live?**

It does not attempt to answer:

> **What does this mean?**  
> **What should I investigate next?**  
> **What should I do about it?**

---

## What Attribution returns

The v1 output includes:

- portfolio volatility;
- ranked component contributions;
- component contribution percentages;
- component contribution in volatility units;
- portfolio weights;
- contribution-versus-weight comparison;
- standalone volatility;
- positive, negative, and near-zero contributions;
- concentration summaries such as top-one and top-two contribution.

The ranked table is the primary output. It is the evidence from which the PM can see where structural portfolio volatility is concentrated and which positions offset it.

---

## What Attribution does not generate

### No generated descriptive observations

Attribution should not generate statements such as:

> “SPY is the dominant contributor.”

The PM can see that directly from the ranked evidence. Generated observations would risk:

- restating the obvious;
- introducing arbitrary interpretation thresholds;
- creating additional presentation logic before it is needed;
- making the artifact appear more opinionated than its evidence supports.

The evidence should be easy to inspect rather than translated into a separate narrative layer.

### No investigation routing

Attribution should not generate:

- a primary focus position;
- a next-investigation field;
- links or routes to Change Report, Drift Analysis, or Rebalance Analysis;
- workflow recommendations.

Those downstream routes depend on the designs of later artifacts. Defining them here would couple Attribution to workflows that have not yet been designed and may change.

### No investment judgement

Attribution should not produce:

- concentrated / diversified verdicts;
- acceptable / unacceptable judgements;
- risk-limit decisions;
- trade recommendations;
- cut / add instructions.

Those require information beyond current weights and covariance, such as targets, mandates, risk budgets, conviction, liquidity, transaction costs, and implementation constraints.

---

## Why evidence-only is sufficient

The component-contribution decomposition already provides meaningful decision support without an interpretation layer:

```text
SPY  40% weight  →  62% of risk
EFA  20% weight  →  21% of risk
IEF  25% weight  →  -1% of risk
GLD  15% weight  →  18% of risk
```

The PM can directly see:

- the largest contributors;
- contribution relative to capital weight;
- positive and negative contributors;
- whether risk is concentrated in one or two positions;
- the difference between standalone asset volatility and portfolio contribution.

The artifact therefore remains useful while avoiding unsupported interpretation.

---

## Data model consequence

The v1 data model should contain the evidence fields only.

It should not contain:

- `focus`;
- `observations`;
- `interpretation_rules`;
- `next_step`;
- `investigation_route`;
- `decision`.

The calculation object should represent the decomposition. Rendering can arrange that evidence into a PM-readable table without adding a narrative judgement layer.

---

## Updated visual design

The v1 display remains focused on the PM's position-level investigation decision. The only change is that the final **Next Investigation / Focus** section has been removed. The ranked contributors, contribution-versus-weight contrast, standalone-risk diagnostic, concentration summary, and methodological boundary remain unchanged.

It does **not** include a diversification-benefit panel or a portfolio-level diversification ratio.

```text
╔══════════════════════════════════════════════════╗
║  ATTRIBUTION                                     ║
║  60/40 Multi-Asset                               ║
║  As of 14 March 2022                             ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  PORTFOLIO RISK                                  ║
║  Volatility: 2.0% daily                          ║
║                                                  ║
║  WHERE DOES RISK LIVE?                           ║
║  Ranked by contribution to portfolio risk        ║
║                                                  ║
║  Asset  Risk contribution bar     Risk  Weight   ║
║                                    %              ║
║  SPY    ████████████████████       62%   40%      ║
║  EFA    ███████                    21%   20%      ║
║  GLD    ██████                     18%   15%      ║
║  IEF    ◄                          -1%   25%      ║
║                                                  ║
║  Asset  Component contribution    Standalone     ║
║         to volatility              volatility     ║
║  SPY    1.24% daily                1.10% daily   ║
║  EFA    0.42% daily                0.90% daily   ║
║  GLD    0.36% daily                0.70% daily   ║
║  IEF   -0.02% daily                0.40% daily   ║
║                                                  ║
║  Bar = percentage contribution to portfolio      ║
║  volatility. Component vol = contribution in    ║
║  daily volatility units. Standalone vol = asset  ║
║  volatility in isolation.                        ║
║                                                  ║
║  CONCENTRATION                                   ║
║  Top 1 asset: 62% of risk                        ║
║  Top 2 assets: 83% of risk                       ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

### Display principles

1. **Lead with the decision** — the first question is where the PM should look, not whether a portfolio-level diversification score is high or low.
2. **Show contribution against weight** — the contrast identifies hidden concentration without declaring that the allocation is wrong.
3. **Keep standalone volatility diagnostic** — it helps distinguish a high-contribution asset because it is volatile from one whose contribution is driven by correlation with the portfolio.
4. **Make negative contribution visible** — a diversifier should not be hidden or treated as a calculation error.
5. **State the decomposition boundary** — the artifact decomposes structural volatility, not the Snapshot's historical VaR headline.

---

## Methodological boundary

The final display should include a short boundary note:

> **Component contributions describe structural portfolio volatility over the estimation window. They are not a trade recommendation and do not decompose historical VaR.**

This note explains what the numbers represent without interpreting the portfolio for the PM.

---

## Deferred possibility

A later version may add interpretation or workflow routing if a subsequent artifact design demonstrates that it is needed. That decision should be made after the next artifacts have been designed and the evidence-only output has been used in practice.

For now, the correct boundary is:

```text
Calculate the decomposition.
Present the evidence.
Stop.
```

---

## Final design position

> **Attribution v1 is an evidence-only, point-in-time, asset-level decomposition of structural portfolio volatility. It ranks and exposes the risk evidence but does not interpret it, route the PM, or recommend action.**


