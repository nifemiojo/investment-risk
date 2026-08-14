# Attribution — Thinking Response (verbatim)

Now I have what I need — including one finding that materially shapes the design. Here's my thinking.

## 1. The decision — name it precisely (and name what it isn't)

The Snapshot was a **gate**: one number in, a binary routing output out ("investigate / no action"). Attribution is a different shape of thing — it's the detail layer the PM opens *after* the gate fires. So its decision isn't another binary gate; it's a **lens** that produces a **ranking**.

The decision attribution enables is: **"Which positions do I look at, and in what order?"**

The trap to name up front: this is exactly where it's tempting to let the artifact prescribe — "SPY is 82% of risk, so reduce SPY." Attribution can't support that. It has no target allocation and no trade-cost information, so it can only say *where* the risk lives, not *whether that's wrong*. "Reduce SPY" is Drift Analysis (compare to target) → Rebalance (size the trade). Attribution stops one hop short and hands the PM a ranked shortlist.

| Artifact | Adds | Decision it can support |
|---|---|---|
| Snapshot | portfolio VaR | investigate / no action (gate, binary) |
| **Attribution** | **where risk lives, per asset** | **which positions to look at (lens, ranked)** |
| Drift | distance from target | which to cut / add |
| Rebalance | trade sizing, marginal VaR | specific trades |

So the framing you asked for resolves to: **question** = "where is the risk coming from"; **decision** = "which positions do I look at"; and the artifact stops short of "which to cut/add".

## 2. The information required to make that decision

To decide *which positions to look at*, the PM needs five things — all derivable from `(weights, covariance)` at a single point in time, nothing historical, no target:

1. **Component risk contribution per asset** — the "where" answer itself. As % of total (the ranking) and in £ (the scale). This is `CTR_i = w_i × (Σw)_i`, which sums exactly to portfolio variance — that additive property is *why* it works as a decomposition.

2. **Weight per asset** — the reference point. Contribution is only meaningful *against* weight. 60% weight / 60% of risk = proportionate, nothing to see. 40% weight / 75% of risk = that's your culprit. Without the weight column, the contribution column is unreadable.

3. **Standalone risk per asset** — separates two different causes of high contribution: a genuinely volatile asset vs. one that's just highly correlated with everything else. Same symptom (high contribution), different diagnosis, different follow-up.

4. **Diversification benefit** — `Σ standalone − portfolio risk`, one number. Tells the PM whether the whole is actually safer than the parts — the whole point of a multi-asset portfolio.

5. **Concentration summary** — % of risk in the largest asset, top two. The at-a-glance "spread or concentrated" read.

All five are cross-sectional — a decomposition of one snapshot, not a history. That's a clean boundary and it matters (see tension C below).

## 3. The design tensions to resolve

These are the real forks. My lean on each is in **bold**.

**A. Asset vs. factor decomposition.** "Where is risk coming from" can mean "which *positions*" or "which *risk factors*" (equity beta, rates, gold, FX). Factor attribution needs a factor model — a different and larger slice. **Lean: asset-level now, factor as a separate future slice.** This matches the "one method, one portfolio, one loop" discipline — don't open the factor-model door before the asset-level pipeline works end-to-end.

**B. Component contribution (CTR) vs. marginal contribution (MCTR).** CTR answers "where is today's risk". MCTR (∂σ/∂w) answers "how much does risk move if I change a weight" — that's a *sensitivity*, and it's the Rebalance artifact's job (the taxonomy already lists "marginal VaR" under Rebalance). **Lean: surface CTR; compute MCTR internally (CTR = w × MCTR) but don't put it in the PM's face here.** Clean boundary, no duplicated concept.

**C. Cross-sectional only — trim the trend labels.** The taxonomy's Attribution row currently has "diversification ratio + trend label (rising/falling/stable)". A trend needs history; a correlation *shift* needs two points. Those belong to the Diversification Monitor / Change Report. **Lean: keep the point-in-time diversification *benefit* and concentration (both cross-sectional), drop the "trend" and "which pairs moved" from Attribution.** It keeps this artifact stateless — same discipline as the Snapshot.

**D. The decomposition base — this is the one I hadn't fully clocked until I read the engine.** The Snapshot's headline number is **historical VaR** — an empirical quantile of the portfolio's own return series. Historical VaR is *not additively decomposable*; there's no clean "component historical VaR". Component contribution is fundamentally a **covariance/volatility** concept. So attribution can't decompose the exact number the Snapshot produces. **Lean: decompose volatility (exactly additive), report % contributions — which are what the PM actually reads for "where from" — and express the £ figure as component volatility (or parametric VaR = z×vol), with an explicit, honest note that this won't reconcile to the historical-VaR headline.** The % attribution is robust and unit-invariant (same whether you decompose vol, variance, or parametric VaR); only the £ absolute carries the mismatch. We document it rather than paper over it.

**E. Does attribution need a binary decision field at all?** The Snapshot needed one — it's a gate triaging many portfolios. Attribution is a lens. **Lean: no forced "concentrated/diversified" binary.** The output is a ranked breakdown plus a concentration number; the PM reads it and decides where to look. Forcing a binary here is the cosplay trap — inventing a verdict no threshold actually justifies.

## 4. The bottom-up reality check

What exists today: weights (`Portfolio.assets`), asset-level daily returns as a DataFrame (`returns_provider.load`), single-asset historical VaR, rolling VaR. What's missing: the covariance matrix, per-asset vol, and CTR — all new but small. One structural note: the Snapshot currently *collapses* asset returns to a portfolio series and throws away the per-asset granularity; Attribution needs that granularity retained. The returns provider already gives us the DataFrame, so the meeting point is clean — attribution adds one covariance-based decomposition on top of data we already load.

---

**Where I'd converge**: asset-level, CTR-based, cross-sectional volatility decomposition; decision = "which positions to look at" (ranked list + concentration number, no binary verdict).

Four questions to pressure-test before I'd write anything down:

1. On the decision — do you agree attribution's output is a *ranking* ("look at SPY first") rather than a gate, and that we explicitly stop it short of "cut/add"?
2. On scope — asset-level now, factor attribution deferred as its own later slice?
3. On the decomposition base — is decomposing *volatility* (with an honest "doesn't reconcile to historical VaR" note) acceptable, or do you want me to push toward making the numbers reconcile?
4. On the information set — is anything missing from the five fields, or anything there you'd push out to Change Report / Diversification Monitor / Drift Analysis?
