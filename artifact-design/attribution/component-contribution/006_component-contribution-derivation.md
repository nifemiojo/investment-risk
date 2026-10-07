# Component Contribution: First-Principles Derivation

A from-scratch derivation of $\text{Contribution}_i = w_i \times \text{Cov}(r_i, r_p)$, assuming no prior knowledge beyond what a return is.

## Step 0: What we're trying to do

We have a portfolio whose returns bounce around — that's risk. We want to answer: *which assets cause that bouncing, and how much of it is each one's fault?*

We need to decompose total portfolio variance into per-asset pieces. But we can't look at each asset in isolation, because assets move together (SPY and EFA rise and fall on the same days). That shared movement means risk isn't neatly separable. We need a decomposition that *accounts for correlation* and *still adds up exactly*.

## Step 1: Portfolio return

Portfolio return on any day is the weighted sum of asset returns:

$$r_p = w_1 r_1 + w_2 r_2 + \dots + w_n r_n = \sum_i w_i r_i$$

If SPY is 40% of the portfolio and returns +1%, it contributes 0.40 × 1% = 0.40% that day.

## Step 2: Variance

Variance measures spread. For a random variable $X$ with mean $\mu$:

$$\text{Var}(X) = \mathbb{E}[(X - \mu)^2]$$

Take each observation, subtract the average, square, then average the squared deviations. Squaring makes everything positive (up and down deviations don't cancel) and penalises large deviations more than small ones.

For daily returns, $\mu \approx 0$, so $\text{Var}(r) \approx \mathbb{E}[r^2]$ — roughly the average squared daily return.

## Step 3: The two-asset case — where correlation enters

Two assets, SPY and IEF, weights $w_S$ and $w_I$:

$$r_p = w_S r_S + w_I r_I$$

Apply the variance operator. **Variance is bilinear:**

$$\text{Var}(aX + bY) = a^2\text{Var}(X) + b^2\text{Var}(Y) + 2ab\,\text{Cov}(X, Y)$$

The $2ab\,\text{Cov}(X,Y)$ term exists because of joint movement: if SPY and IEF both have bad days together, the portfolio's bad days are worse (losses compound). If IEF rises when SPY falls (negative correlation), the portfolio's bad days are cushioned. Covariance captures this: positive when they move together, negative when opposite, zero when unrelated.

So:

$$\sigma_p^2 = w_S^2 \sigma_S^2 + w_I^2 \sigma_I^2 + 2 w_S w_I \, \text{Cov}(r_S, r_I)$$

First two terms: each asset's own variance scaled by weight². Third term: the *interaction* — risk that belongs to both assets jointly.

## Step 4: Generalising to N assets

Every pair has a covariance term. Portfolio variance becomes a double sum:

$$\sigma_p^2 = \sum_{i=1}^n \sum_{j=1}^n w_i w_j \, \text{Cov}(r_i, r_j)$$

When $i = j$, $\text{Cov}(r_i, r_i) = \text{Var}(r_i)$ — the diagonal captures standalone variances, everywhere else captures interactions. For four assets this is a 4×4 grid, 16 terms. That's the full covariance structure.

## Step 5: The regrouping trick — from pairs to assets

The double sum answers "what is total risk?" but doesn't assign it to assets. Group by asset $i$, pulling $w_i$ out of the inner sum:

$$\sigma_p^2 = \sum_i w_i \left[ \sum_j w_j \, \text{Cov}(r_i, r_j) \right]$$

The bracket is asset $i$'s covariance with every asset in the portfolio, weighted by holdings — which is exactly covariance with the portfolio itself:

$$\text{Cov}(r_i, r_p) = \text{Cov}\!\left(r_i, \sum_j w_j r_j\right) = \sum_j w_j \, \text{Cov}(r_i, r_j)$$

(The $w_j$ are constants; covariance is linear — covariance of $r_i$ with a weighted sum is the weighted sum of covariances.)

Substituting back:

$$\sigma_p^2 = \sum_i w_i \, \text{Cov}(r_i, r_p)$$

Each term $w_i \, \text{Cov}(r_i, r_p)$ is asset $i$'s **contribution to portfolio variance**.

## Step 6: Why this decomposition works

**1. Additivity.** The pieces sum exactly to $\sigma_p^2$. Nothing missing, nothing double-counted. That's what makes it a trustworthy "where from" answer.

**2. It accounts for correlation.** $\text{Cov}(r_i, r_p)$ is not asset $i$'s own variance — it's how asset $i$ interacts with everything else. If IEF is negatively correlated with SPY, $\text{Cov}(r_{\text{IEF}}, r_p)$ can be negative, and IEF gets a negative contribution — it *reduces* risk. Standalone variance can never capture that.

## Step 7: Concrete example (40/20/25/15 portfolio)

For SPY:

$$\text{Cov}(r_{\text{SPY}}, r_p) = w_{\text{SPY}}\text{Var}(r_{\text{SPY}}) + w_{\text{EFA}}\text{Cov}(r_{\text{SPY}}, r_{\text{EFA}}) + w_{\text{IEF}}\text{Cov}(r_{\text{SPY}}, r_{\text{IEF}}) + w_{\text{GLD}}\text{Cov}(r_{\text{SPY}}, r_{\text{GLD}})$$

SPY's $\text{Cov}(r_i, r_p)$ is large because: high own-variance (first term), strong co-movement with EFA (second term), small negative IEF term (slight offset), near-zero GLD term (uncorrelated).

IEF's is negative: moderate own-variance, but *negative* covariance with SPY and EFA — and those have big weights, so the negative terms dominate. IEF is a net risk reducer.

That's why SPY contributes 61% and IEF contributes −1.1%.

## Step 8: The memorable one-liner

Define beta against the portfolio (contribution beta, not CAPM beta):

$$\beta_i = \frac{\text{Cov}(r_i, r_p)}{\sigma_p^2}$$

Then:

$$\text{\% contribution}_i = w_i \times \beta_i$$

An asset's share of risk = how big it is × how much it co-moves with the portfolio. SPY: big *and* highly correlated → dominant. IEF: moderately big *but* moves opposite → negative. GLD: small *and* uncorrelated → barely registers.

## The intuition to carry forward

One idea: **instead of asking "how volatile is this asset?" ask "how does this asset interact with the portfolio I actually hold?"** Covariance-with-the-portfolio captures the interaction; multiplying by weight gives the contribution. The pieces add up because variance is bilinear — that property guarantees the decomposition closes.