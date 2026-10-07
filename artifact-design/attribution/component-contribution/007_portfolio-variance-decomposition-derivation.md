# Portfolio Variance Decomposition: The Two-Asset Derivation

A focused walkthrough of exactly how we get from the portfolio return to the variance expansion with the covariance cross-term. No prior knowledge assumed.

## The definition of variance

Variance is the expected squared deviation from the mean:

$$\text{Var}(X) = \mathbb{E}\big[(X - \mathbb{E}[X])^2\big]$$

In words: "on average, how far is X from its own average, squared?" Everything else is just algebra applied to this definition.

## Step 1: Write down the deviation of the portfolio return

We know $r_p = w_S r_S + w_I r_I$.

The mean (expected value) of $r_p$ is:

$$\mathbb{E}[r_p] = \mathbb{E}[w_S r_S + w_I r_I] = w_S \mathbb{E}[r_S] + w_I \mathbb{E}[r_I]$$

(The $w$'s are constants — expectation passes right through them.)

Now the deviation from the mean:

$$r_p - \mathbb{E}[r_p] = (w_S r_S + w_I r_I) - (w_S \mathbb{E}[r_S] + w_I \mathbb{E}[r_I])$$

Group the $w_S$ terms and the $w_I$ terms:

$$= w_S(r_S - \mathbb{E}[r_S]) + w_I(r_I - \mathbb{E}[r_I])$$

This is the key setup. The portfolio's deviation from its mean is just the weighted sum of each asset's deviation from its own mean.

## Step 2: Square it

Variance wants the square of that deviation:

$$(r_p - \mathbb{E}[r_p])^2 = \big[w_S(r_S - \mathbb{E}[r_S]) + w_I(r_I - \mathbb{E}[r_I])\big]^2$$

This is exactly $(a + b)^2 = a^2 + b^2 + 2ab$, where:

- $a = w_S(r_S - \mathbb{E}[r_S])$
- $b = w_I(r_I - \mathbb{E}[r_I])$

Expanding:

$$(r_p - \mathbb{E}[r_p])^2 = \underbrace{w_S^2(r_S - \mathbb{E}[r_S])^2}_{a^2} + \underbrace{w_I^2(r_I - \mathbb{E}[r_I])^2}_{b^2} + \underbrace{2\,w_S w_I (r_S - \mathbb{E}[r_S])(r_I - \mathbb{E}[r_I])}_{2ab}$$

Three things to notice:

- **The weights get squared** in the first two terms. A 40% weight becomes 0.16 in variance terms — doubling a position quadruples its contribution to variance.
- **The cross term** has $2 \times w_S \times w_I$. It's proportional to both weights — it only exists when you hold *both* assets.
- The cross term contains $(r_S - \mathbb{E}[r_S])(r_I - \mathbb{E}[r_I])$ — the product of the two assets' deviations. This is where correlation lives.

## Step 3: Take the expectation

Apply $\mathbb{E}[\cdot]$ to each term:

$$\mathbb{E}[(r_p - \mathbb{E}[r_p])^2] = w_S^2\,\underbrace{\mathbb{E}[(r_S - \mathbb{E}[r_S])^2]}_{\text{this is Var}(r_S)} + \; w_I^2\,\underbrace{\mathbb{E}[(r_I - \mathbb{E}[r_I])^2]}_{\text{this is Var}(r_I)}$$

$$+ \; 2 w_S w_I\,\underbrace{\mathbb{E}[(r_S - \mathbb{E}[r_S])(r_I - \mathbb{E}[r_I])]}_{\text{this is Cov}(r_S, r_I)}$$

And that's it:

$$\sigma_p^2 = w_S^2 \sigma_S^2 + w_I^2 \sigma_I^2 + 2 w_S w_I \, \text{Cov}(r_S, r_I)$$

## Step 4: What is that covariance term actually doing?

Covariance is the expected product of the two deviations:

$$\text{Cov}(r_S, r_I) = \mathbb{E}[(r_S - \mathbb{E}[r_S])(r_I - \mathbb{E}[r_I])]$$

Think about what happens day by day:

| Day type | $(r_S - \mathbb{E}[r_S])$ | $(r_I - \mathbb{E}[r_I])$ | Product |
|---|---|---|---|
| Both above average | + | + | **+** |
| Both below average | − | − | **+** |
| SPY up, IEF down | + | − | **−** |
| SPY down, IEF up | − | + | **−** |

When they move together (both above or both below), the product is positive. When they move opposite, the product is negative. The covariance is the *average* of these products:

- **Positive covariance:** most days, they're on the same side of their means → the $+2w_S w_I \text{Cov}$ term *adds* to portfolio variance → these assets amplify each other's risk.
- **Negative covariance:** most days, they're on opposite sides → the cross term *subtracts* from variance → the assets dampen each other.
- **Zero covariance:** no systematic pattern → the cross term averages to zero → risk is just the weighted standalone variances.

For SPY and IEF, the covariance is negative — when equities fall, bonds tend to rise. So on a bad day for SPY ($r_S - \mathbb{E}[r_S]$ is negative), IEF's deviation is typically *positive*, the product is negative, and the $2w_S w_I \text{Cov}$ term *reduces* the portfolio's total squared deviation. That's diversification working, right there in the algebra.

## Step 5: The full 4-asset expansion (just to see the pattern)

With SPY, EFA, IEF, GLD, you square a sum of four terms:

$$(a + b + c + d)^2 = a^2 + b^2 + c^2 + d^2 + 2ab + 2ac + 2ad + 2bc + 2bd + 2cd$$

That's 4 diagonal terms (the standalone variances) and 6 off-diagonal terms (one for each pair). The double-sum notation $\sum_i \sum_j$ is just a compact way of writing this for any $n$.

## The one-sentence summary

The $2 w_S w_I \text{Cov}(r_S, r_I)$ term exists because $(a + b)^2$ is not $a^2 + b^2$ — squaring a sum always creates cross terms, and those cross terms *are* the correlation structure of the portfolio.
