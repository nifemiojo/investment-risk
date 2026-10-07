# Component Contribution: Definition, PM Relevance, and Rebalancing Feed

## 1. What Component Contribution Is

Component contribution is each asset's contribution to portfolio return variance — but it's not standalone variance. It's the covariance of the asset *with the whole portfolio*:

$$\text{Contribution}_i = w_i \times \text{Cov}(r_i, r_p)$$

where:

$$\text{Cov}(r_i, r_p) = \sum_j w_j \, \text{Cov}(r_i, r_j)$$

This bakes in every pairwise correlation. The pieces sum exactly to $\sigma_p^2$ (additivity), and the percentage form is $w_i \times \beta_i$.

The move that separates this from standalone vol: $\text{Cov}(r_i, r_p)$ captures not just whether asset $i$ is volatile, but whether its movements *align with or offset* the rest of the portfolio. GLD might be volatile on its own, but if it's uncorrelated with equities, it's not a risk driver in *this* portfolio. Component contribution sees that; standalone vol doesn't.

## 2. Why This Matters to the PM

The PM can't manage what they can't see — and weight alone is a misleading risk map. For a multi-asset mandate, component contribution provides:

**It surfaces hidden concentration.** SPY at 40% weight producing 61% of risk means the portfolio is more of an equity bet than the allocation table suggests. The PM allocated to four assets for diversification; the contribution table tells them whether that diversification is actually working.

**It validates the hedges.** IEF at 25% weight and −1.1% contribution isn't dead weight — it's offsetting equity risk and earning its keep. If that number flips positive, the diversification thesis has broken. Without component contribution, IEF just looks like a low-return drag.

**It creates accountability.** The PM made allocation choices. Component contribution shows the *risk consequences* of those choices — not in hindsight ("IEF lost money") but structurally ("IEF is reducing your tail risk by X"). It closes the loop between the allocation decision and its risk outcome.

**It bridges from gate to investigation.** The Snapshot says "investigate." Attribution says "start with SPY." Without that ranking, the PM opens a four-asset portfolio with no structured way to begin.

## 3. How This Feeds into Rebalancing

Component contribution doesn't prescribe trades — it provides the ranked input that rebalancing acts on:

**Step 1 — Identify the outliers.** SPY: 40% weight, 61% of risk — disproportionate. EFA: 20% weight, 33% of risk — also disproportionate. SPY + EFA: 60% of capital, 94% of risk. That's the shortlist.

**Step 2 — Compare to target.** Drift analysis confirms: SPY target is 40%, actual is 43%. Weight drift and risk concentration converge on the same asset. Converging evidence.

**Step 3 — Size the impact via MCTR.** Component contribution says where risk *is*. Marginal contribution says what happens if you *change* it:

$$\text{MCTR}_i = \frac{\text{Cov}(r_i, r_p)}{\sigma_p} = \frac{\text{CTR}_i}{w_i \times \sigma_p}$$

SPY with 61% CTR on 40% weight → MCTR ~1.5× the portfolio average. Cutting SPY 1% reduces vol by 1.5× more than a proportional cut. IEF with near-zero or negative MCTR → cutting IEF *increases* risk. The MCTR ranking IS the rebalancing priority list.

**Step 4 — Execute.** Rebalancing takes the MCTR ranking, the drift from target, and trade costs, and produces specific sizes. Attribution doesn't do this step — but it hands rebalancing a ranked, quantified input.

## What Component Contribution Doesn't Do

It doesn't say whether 61% in SPY is *wrong*. That depends on mandate, conviction, and market environment. A PM bullish on equities might accept it. A risk parity PM would consider it a failure. Attribution is value-neutral: it surfaces the fact, the PM brings the judgment.