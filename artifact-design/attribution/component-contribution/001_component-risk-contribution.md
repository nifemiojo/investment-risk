# Component Risk Contribution (verbatim)

Here's the concept, worked through from the ground up.

## What component risk contribution *is*

The snapshot hands the PM a single number — portfolio volatility (or VaR). Component contribution answers the follow-up: *which positions make up that number, and how much of it is each one's fault*.

The reason this isn't trivial is **correlation**. If SPY and EFA always move together, then a chunk of the portfolio's risk is *shared* between them — it doesn't cleanly "belong" to either. Standalone volatility can't answer the question (it ignores correlation entirely). Component contribution is the standard way to slice the risk so that the pieces are *fair* (each asset credited for its full interaction with the portfolio) *and* they **add up exactly to the total**. That "adds up exactly" property is what makes it a trustworthy "where is the risk coming from" answer.

## The derivation, step by step

Start from what we already know: portfolio return is a weighted sum.

$$r_p = \sum_i w_i\, r_i$$

Variance is bilinear, so:

$$\sigma_p^2 = \text{Var}(r_p) = \sum_i \sum_j w_i w_j\, \text{Cov}(r_i, r_j)$$

Now the key move: **group the double sum by asset $i$**, pulling $w_i$ out of the inner sum:

$$\sigma_p^2 = \sum_i w_i \underbrace{\Big[\sum_j w_j\, \text{Cov}(r_i, r_j)\Big]}_{\text{Cov}(r_i, r_p)}$$

The inner bracket is exactly $\text{Cov}(r_i, r_p)$ — the covariance of asset $i$ *with the whole portfolio* — because:

$$\text{Cov}(r_i, r_p) = \text{Cov}\Big(r_i,\ \sum_j w_j r_j\Big) = \sum_j w_j\, \text{Cov}(r_i, r_j)$$

(the $w_j$ are constants, and covariance is linear in each argument). So:

$$\sigma_p^2 = \sum_i w_i\, \text{Cov}(r_i, r_p)$$

Each term is asset $i$'s contribution. Define:

- **Contribution to variance:** $w_i\,\text{Cov}(r_i, r_p)$ — these sum to $\sigma_p^2$.
- **Contribution to volatility:** $\dfrac{w_i\,\text{Cov}(r_i, r_p)}{\sigma_p}$ — these sum to $\sigma_p$.
- **Percentage contribution:** $\dfrac{w_i\,\text{Cov}(r_i, r_p)}{\sigma_p^2}$ — these sum to **1** (100%).

One precision point worth noting: the *percentage* is identical whether you work in variance or volatility terms (dividing by $\sigma_p^2$ vs $\sigma_p$ then normalising gives the same number). So "what % of risk is asset $i$" is unambiguous — only the absolute units differ.

## The memorable form: weight × beta

The percentage has a clean rewrite. Define the asset's **beta against the portfolio** (not the market — this is *contribution* beta, a different animal from CAPM beta):

$$\beta_i = \frac{\text{Cov}(r_i, r_p)}{\sigma_p^2}$$

Then:

$$\text{\% contribution}_i = w_i \times \beta_i$$

This is the whole intuition in one line: **an asset contributes risk in proportion to (a) how big it is, and (b) how much it co-moves with the portfolio.** Big weight *and* high co-movement → dominant. Small weight *or* moves against the portfolio → little, or even *negative*.

## A worked example (your actual 40/20/25/15 portfolio)

Using illustrative vols/correlations (no local price data yet — I'll flag where real data slots in below):

| Asset | Weight | $\text{Cov}(r_i,r_p)$ | Contribution to vol (daily) | **% of risk** |
|---|---|---|---|---|
| SPY | 40% | 0.000073 | 0.00423 | **60.9%** |
| EFA | 20% | 0.000080 | 0.00231 | **33.2%** |
| IEF | 25% | −0.000002 | −0.00008 | **−1.1%** |
| GLD | 15% | 0.000022 | 0.00048 | **6.9%** |
| **Total** | 100% | | **0.00694** (= $\sigma_p$) | **100%** |

Three things to read off this table:

1. **SPY is the story** — 40% of the portfolio, 61% of the risk. Disproportionate.
2. **EFA is *more* disproportionate than it looks** — 20% weight but 33% of risk. Its beta is ~1.66 (the highest), because it's the most volatile asset *and* 85% correlated with SPY. Its risk is almost all *shared* risk.
3. **IEF is negative.** It's 25% of the portfolio yet contributes *−1.1%* — it *reduces* risk, because it's negatively correlated with the equity sleeve. Negative contributions are real and meaningful: they're your diversifiers doing their job.

**Why not just use standalone vol?** Sum the standalone daily vols: SPY 1.13% + EFA 1.26% + IEF 0.38% + GLD 0.94% = **3.72%**, versus actual portfolio vol **0.69%** — standalone overstates by **5.4×**, because it double-counts the shared equity risk and completely ignores IEF's offsetting effect. Component contribution is the version that's honest about correlation.

## What this tells the PM (the "so what")

You open the attribution view at 8am and see that table:

- **Where to look first** — the ranking *is* the triage. SPY first, then EFA. That's the funnel narrowing from "investigate this portfolio" to "investigate SPY".
- **Concentration** — top-1 is 61%. One asset carries most of the risk. Worth knowing before it becomes a problem.
- **The equity-concentration story** — SPY + EFA = 94% of risk from 60% of the weight. The portfolio is effectively an equity bet. This is the "hidden concentration" the snapshot can't see but attribution surfaces.
- **The hedge check** — IEF's negative number means it's *earning its keep* by offsetting equity risk. If that negative ever flips positive, diversification has broken down and the PM should notice.
- **Trustworthiness** — the pieces sum to 100%, nothing missing, nothing double-counted. The "where from" answer is complete.

## How to calculate it (the recipe)

Four lines of numpy, given a returns matrix and weights:

```python
Sigma   = returns.cov()            # N×N covariance (daily)
w       = weights_array            # N-vector, sums to 1
sigma_p = np.sqrt(w @ Sigma @ w)   # portfolio volatility
marginal = Sigma @ w               # = Cov(r_i, r_p) for each asset
comp_vol = w * marginal / sigma_p  # sums to sigma_p
comp_pct = comp_vol / sigma_p      # sums to 1.0  (== w_i * beta_i)
```

`Sigma @ w` is the single step that does all the correlation accounting — it gives each asset its covariance with the portfolio in one matrix-vector product.

---

**Check before we go on:** EFA's contribution (33%) exceeds its weight (20%), while IEF's (25% weight) is negative. What's the single number that explains *both*? And what would happen to IEF's contribution if the SPY–IEF correlation flipped from −0.30 to +0.30?

That last question is also the natural bridge to **Q3**: I decomposed *volatility* here, but the snapshot's headline is *historical VaR* — so next we should pin down whether (and how) the £ figures reconcile. Want me to take that next, or did you want to sit with this first?
