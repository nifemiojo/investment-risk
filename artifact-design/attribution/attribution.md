# Artifact Design: Attribution

**Status**: Design in progress — thinking captured, not yet finalised
**Date**: 2026-08-14
**Artifact type**: Attribution
**Answers**: "Where is the risk coming from?"

---

## PM Usage: From Gate to Lens

The Snapshot is a **gate** — one number in, a binary routing output out ("investigate / no action"). Attribution is the detail layer the PM opens *after* that gate fires. It is a **lens**, not a gate: its output is a *ranking*, not a verdict.

The PM's eyes move in this order:

```
1. Concentration summary (top-1, top-2 % of risk)   ← 1s — spread or concentrated?
2. Ranked contribution list (sorted by %)           ← 3s — which positions dominate?
3. Contribution vs weight contrast                  ← 2s — is anyone disproportionate?
4. Standalone risk per asset                        ← 2s — volatile, or correlated?
5. Diversification benefit                          ← 1s — is the structure working?
```

Where the Snapshot answers "should I look?", Attribution answers "where do I look?". It is a stateless function of `(weights, asset_returns, date)` — a cross-sectional decomposition of one Snapshot, nothing historical, no target.

---

## Frequency & Triggers

The artifact type is point-in-time. Frequency is set at the edge:

| Frequency | When | Use case |
|---|---|---|
| On demand | After the Snapshot flags "investigate" | "Where exactly is this risk coming from?" |
| Daily | Alongside the Snapshot in a daily brief | Routine transparency into risk sources |
| Monthly | As part of a monthly review composition | "Where has risk been living over the month?" |

No schedule of its own — it is usually *pulled* (by the Snapshot's decision) rather than *pushed*.

---

## Decisions It Enables

Attribution's decision is: **"Which positions do I look at, and in what order?"** It routes the investigation one hop forward, from portfolio-level ("investigate") to position-level ("look at SPY").

| What Attribution shows | PM decision | Next step |
|---|---|---|
| Single dominant contributor (e.g. SPY = 62% of risk) | Focus on SPY | Open Change Report / Drift Analysis on that position |
| Contributions roughly proportional to weights | Risk is diversified — nothing stands out | No position-level follow-up |
| A position's contribution far exceeds its weight | Concentration to investigate | Dig into that position's volatility and correlation |
| A position contributes ~0% or negative | It's a diversifier | Confirm that's intentional |

**What it does NOT decide** — and this is deliberate. Attribution has no target allocation and no trade-cost information, so it cannot say "reduce SPY". "Which to cut/add" is Drift Analysis (compare to target) → Rebalance (size the trade). Attribution stops one hop short and hands the PM a ranked shortlist.

| Artifact | Adds | Decision it can support |
|---|---|---|
| Snapshot | portfolio VaR | investigate / no action (gate, binary) |
| **Attribution** | **where risk lives, per asset** | **which positions to look at (lens, ranked)** |
| Drift | distance from target | which to cut / add |
| Rebalance | trade sizing, marginal VaR | specific trades |

---

## Business Justification

### 1. Transparency — No Black Box

"How much risk?" is answered by the Snapshot; "where from?" is the immediate follow-up from any investment committee or fiduciary. A risk number with no decomposition is a black box. Attribution makes the number inspectable and, therefore, discussable.

### 2. Diversification Is the Thesis

The entire point of a multi-asset portfolio is that risk is spread. Attribution is the *evidence* of whether that thesis is actually holding — the diversification benefit number literally shows whether the whole is safer than the parts.

### 3. Concentration Is a Risk in Its Own Right

Hidden concentration is the classic failure mode of "diversified" portfolios. A portfolio can look balanced by weight and still have one asset dominating the risk. Attribution is the only artifact that surfaces this — weight tells you what you *own*, contribution tells you what you *risk*.

### 4. PM Thinking, Not Trader Thinking

Attribution forces position-level awareness without losing the portfolio-level view. A trader sees positions; a PM sees how positions combine into a risk profile. This is the difference the artifact makes concrete.

### 5. Communication Currency

"Risk isn't a single number — here's where it lives" is the bridge from measurement to conversation. It lets the PM explain *why* a portfolio is safe or vulnerable, not just report *that* it is.

---

## The Display

First cut — will firm up alongside the engine API.

```
╔══════════════════════════════════════════════╗
║  RISK ATTRIBUTION                           ║
║  60/40 Multi-Asset                          ║
║  14 March 2022 · Close                      ║
║  Component contribution to volatility       ║  ← decomposition_base + risk_unit
╠══════════════════════════════════════════════╣
║                                              ║
║  WHERE IS THE RISK COMING FROM?              ║
║  SPY  40% wgt  ████████████░░  62% of risk   ║  ← ranked, sorted descending
║  EFA  20% wgt  ████░░░░░░░░░░  21% of risk   ║
║  IEF  20% wgt  █░░░░░░░░░░░░░   9% of risk   ║
║  GLD  20% wgt  █░░░░░░░░░░░░░   8% of risk   ║
║                                              ║
║  CONCENTRATION                               ║
║  Top 1 asset: 62% of risk                    ║
║  Top 2 assets: 83% of risk                   ║
║                                              ║
║  STANDALONE VS CONTRIBUTION                  ║
║  SPY  alone 1.1%  →  contributes 62%         ║  ← volatile, or correlated?
║  EFA  alone 0.9%  →  contributes 21%         ║
║  IEF  alone 0.4%  →  contributes  9%         ║
║  GLD  alone 0.7%  →  contributes  8%         ║
║                                              ║
║  DIVERSIFICATION BENEFIT                     ║
║  Σ standalone 3.1%  −  portfolio 2.0%        ║
║  = 1.1% diversified away (35% reduction)     ║
║                                              ║
║  ─────────────────────────────────────────── ║
║  Focus: SPY — contribution disproportionate  ║  ← descriptive, not a verdict
║         to weight                            ║
║                                              ║
╚══════════════════════════════════════════════╝
```

---

## Data Model

First cut — to be finalised alongside the engine API.

```python
@dataclass(frozen=True)
class AssetContribution:
    """One asset's contribution to portfolio risk."""
    ticker: str
    weight: float               # 0.40 — the asset's portfolio weight
    contribution_pct: float     # 0.62 — share of total variance (sums to 1.0)
    contribution_vol: float     # 0.0062 — component volatility, daily (sums to portfolio_vol)
    standalone_vol: float       # 0.011 — daily volatility of the asset in isolation
    marginal_vol: float         # 0.0155 — MCTR; computed, not surfaced (downstream: rebalance)


@dataclass(frozen=True)
class RiskAttribution:
    """Point-in-time decomposition of one snapshot's risk into its sources."""

    # === Identity ===
    portfolio_name: str
    timestamp: str               # "2022-03-14T16:30:00"
    data_freshness: str          # "Close" | "Intraday-14:30"
    decomposition_base: str      # "volatility" — what we decompose (see Design Decisions)
    risk_unit: str               # "daily" | "annualised"

    # === Core Decomposition ===
    assets: tuple[AssetContribution, ...]   # sorted by contribution_pct descending
    portfolio_vol: float          # sqrt(w'Σw) — the total being decomposed

    # === Concentration ===
    top1_contribution_pct: float  # 0.62
    top2_contribution_pct: float  # 0.83

    # === Diversification ===
    standalone_sum: float           # Σ standalone_vol across assets
    diversification_benefit: float  # standalone_sum − portfolio_vol (positive = working)
    diversification_ratio: float    # standalone_sum / portfolio_vol (≥ 1.0)

    # === Focus ===
    focus: str                     # descriptive summary of the ranking, NOT a decision
                                   # "SPY dominates (62% of risk vs 40% of weight)" | "spread across assets"
```

Inputs: `(weights, asset_returns)` — both already available. `Portfolio.assets` gives the weights; the returns provider already returns asset-level daily returns as a DataFrame. The *new* work is the covariance matrix `Σ` and the component decomposition `w × (Σw)`. One structural note: the Snapshot currently collapses asset returns to a portfolio series and discards the per-asset granularity; Attribution needs that granularity retained.

---

## Design Decisions

| Decision | Rationale |
|---|---|
| **Asset-level decomposition, not factor** | "Where from" can mean "which positions" or "which risk factors" (equity beta, rates, gold, FX). Factor attribution needs a factor model — a larger, separate slice. Asset-level now; defer factor. One method, one loop, end-to-end first. |
| **Component contribution (CTR), not marginal (MCTR)** | CTR answers "where is today's risk"; it sums exactly to portfolio variance. MCTR (`∂σ/∂w`) answers "how much does risk move if I change a weight" — a *sensitivity*, and the Rebalance artifact's job. MCTR is computed internally (`CTR = w × MCTR`) but not surfaced here. |
| **Cross-sectional only — no trend labels, no correlation shifts** | A "rising/falling" trend needs history; a correlation *shift* needs two points. Both belong to Diversification Monitor / Change Report. Keeping Attribution stateless matches the Snapshot's discipline. |
| **Volatility as the decomposition base (not historical VaR)** | The Snapshot's headline is historical VaR — an empirical quantile that is *not additively decomposable*. Component contribution is a covariance/volatility concept. Decompose volatility (exactly additive); report % contributions (what the PM reads). The % is unit-invariant across vol/variance/parametric VaR; only the £ absolute carries the mismatch. That mismatch is documented, not papered over. |
| **Contribution shown against weight** | Contribution is only meaningful relative to weight. "60% weight / 60% risk" = proportionate, nothing to see; "40% weight / 75% risk" = concentration. The weight column is what makes the contribution column readable. |
| **No forced binary decision field** | The Snapshot needed a `decision` field — it's a gate triaging many portfolios. Attribution is a lens: a ranked breakdown + concentration numbers, and the PM decides where to look. Forcing a "concentrated/diversified" binary is the cosplay trap — a verdict no threshold justifies. The `focus` field is descriptive prose, not a decision. |
| **Frozen dataclass** | Immutable once computed. No accidental mutation in display code. Consistent with the Snapshot. |
| **Standalone risk separates two causes of high contribution** | A volatile asset vs. a correlated asset both show high contribution but need different follow-up. Standalone vol is the diagnostic that tells them apart. |

---

## What Attribution Does NOT Include

| Excluded | Where it lives | Rationale |
|---|---|---|
| Marginal contribution (MCTR) surfaced to the PM | Rebalance Recommendation | A sensitivity, not a decomposition. Answers "what if I change a weight", not "where from". |
| Factor decomposition | Future slice (factor model) | Different question, different machinery. Deferred. |
| Diversification *trend* / correlation *shifts* | Diversification Monitor / Change Report | Needs history or two points. Attribution is stateless. |
| Target comparison / drift | Drift Analysis | Needs a `risk_allocation_target`. Attribution has no target. |
| Trade recommendations | Rebalance Recommendation | Observes, doesn't prescribe. |
| Reconciliation to historical VaR | (documented limitation) | Attribution decomposes volatility; the Snapshot's historical VaR is not decomposable. The % contributions are robust; the £ will not sum to the historical-VaR headline. |

---

## Edge Cases

| Scenario | How the model handles it |
|---|---|
| Negative or ~zero contribution (a hedge / low-correlation asset) | `contribution_pct` can be ≤ 0; the % breakdown still sums to 1.0. Display notes "diversifier" rather than treating it as noise. |
| Single asset dominates (top-1 ≈ 100%) | Valid; concentration numbers surface it directly. |
| Zero-weight asset | Excluded from the decomposition (contributes nothing). |
| Short position (negative weight) | Contribution sign flips. V1 portfolio is long-only (SPY/EFA/IEF/GLD); shorts noted as out of scope. |
| Missing price data | Engine raises; no partial attribution (consistent with the Snapshot). |
| Weight drift mid-period | Uses current weights — a snapshot of state at that moment. |
| Degenerate covariance (portfolio vol = 0) | Guard division by zero in `contribution_pct`. |

---

## Open Questions

To resolve before finalising this design:

1. **On the decision** — is the ranked output ("look at SPY first") the right shape, and are we explicitly stopping short of "cut/add"?
2. **On scope** — asset-level now, factor attribution deferred as its own later slice — agreed?
3. **On the decomposition base** — is decomposing *volatility* (with an honest "doesn't reconcile to historical VaR" note) acceptable, or should the numbers be made to reconcile?
4. **On the information set** — is anything missing from the five fields, or anything here that belongs to Change Report / Diversification Monitor / Drift Analysis instead?
