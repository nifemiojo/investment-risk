Good question — "Σ is the covariance matrix" is a statement that skips the interesting part, which is *how a single number (variance) turns into a grid (matrix)* when you go from one asset to several. Let me build it from the variance you already understand.

## Start from variance of ONE asset

For a single asset with return $r$ and mean return $\mu$, the variance is:

$$ \sigma^2 = \mathbb{E}\big[(r - \mu)^2\big] $$

Read that literally: take the deviation of the return from its mean, square it, and average. Squaring the *scalar* $(r-\mu)$ gives a *scalar*.

So one asset → one number. There's nowhere for a matrix to hide because there's only one thing to vary.

## The problem with two assets

The moment you have two assets, "how spread out are they" is no longer one question — it's three:

1. How much does asset 1 vary on its own? → $\mathrm{Var}(r_1)$
2. How much does asset 2 vary on its own? → $\mathrm{Var}(r_2)$
3. How do they move *together*? → $\mathrm{Cov}(r_1, r_2)$

One number can't hold all three. You need a **grid**, and the natural grid is a $2\times2$ table where:

- the **diagonal** holds the two variances,
- the **off-diagonal** holds the covariance (both corners, since $\mathrm{Cov}(r_1,r_2) = \mathrm{Cov}(r_2,r_1)$):

$$ \Sigma = \begin{pmatrix} \mathrm{Var}(r_1) & \mathrm{Cov}(r_1, r_2) \\ \mathrm{Cov}(r_2, r_1) & \mathrm{Var}(r_2) \end{pmatrix} $$

With $N$ assets it's the same idea, just bigger: an $N\times N$ grid where **entry $(i,j)$ is $\mathrm{Cov}(r_i, r_j)$**.

## The elegant way to write all of that at once

Here's the move that turns the single-variable variance into the matrix. In the one-asset case we squared a scalar deviation, $(r-\mu)^2$. Now the "deviation" is a whole *vector* of deviations, one per asset:

$$ r - \mu = \begin{pmatrix} r_1 - \mu_1 \\ r_2 - \mu_2 \end{pmatrix} $$

To "square" a vector, you can't multiply it by itself — but you can multiply the column by its own transpose, which gives a matrix (this is called an **outer product**):

$$ (r-\mu)(r-\mu)^\top = \begin{pmatrix} (r_1-\mu_1)^2 & (r_1-\mu_1)(r_2-\mu_2) \\ (r_2-\mu_2)(r_1-\mu_1) & (r_2-\mu_2)^2 \end{pmatrix} $$

Now take the expectation (the average), exactly as we did for variance:

$$ \Sigma = \mathbb{E}\big[(r-\mu)(r-\mu)^\top\big] = \begin{pmatrix} \mathbb{E}[(r_1-\mu_1)^2] & \mathbb{E}[(r_1-\mu_1)(r_2-\mu_2)] \\ \mathbb{E}[(r_2-\mu_2)(r_1-\mu_1)] & \mathbb{E}[(r_2-\mu_2)^2] \end{pmatrix} $$

And each of those expectations *is* the variance/covariance definition:

$$ \Sigma = \begin{pmatrix} \mathrm{Var}(r_1) & \mathrm{Cov}(r_1,r_2) \\ \mathrm{Cov}(r_2,r_1) & \mathrm{Var}(r_2) \end{pmatrix} $$

So the definition of $\Sigma$ is literally: **"variance, but for a vector"** — square each deviation by taking the outer product instead of the scalar square, then average. That's the entire "how."

## Why the symbol Σ specifically

This is a notation convention, not a new fact:

- $\sigma$ (lowercase sigma) is the standard symbol for **standard deviation**.
- $\sigma^2$ is **variance** — the standard deviation squared.
- When you generalise variance from one variable to $N$ variables, the single number becomes a matrix, and the convention is to use the **capital** of the same Greek letter: $\Sigma$.

The intuition that makes it stick: look at the **diagonal** of $\Sigma$. Its entries are $\mathrm{Var}(r_i)$, which is exactly $\sigma_i^2$ for each asset. So $\Sigma$ is the matrix whose diagonal *is* the $\sigma^2$ you already know — it's variance promoted to a matrix, with the covariances filling in the off-diagonal slots. Capital-for-matrix is just how mathematics signals "the multivariate version of this thing."

(You'll also see it called the **variance–covariance matrix**, which is the most honest name: variances on the diagonal, covariances off it.)

## How the code actually builds it

The compact definition $\Sigma = \mathbb{E}[(r-\mu)(r-\mu)^\top]$ maps almost one-to-one onto NumPy/pandas:

1. **Mean-center** each asset's returns (subtract its own mean).
2. **Form the outer-product average** — for a data matrix with days as rows and assets as columns, that's $\frac{1}{n-1}X^\top X$ where $X$ is the centered data.
3. Divide by $n-1$ (the sample-covariance correction), not $n$.

```python
import numpy as np

# 3 assets, 5 days of daily decimal returns
returns = np.array([
    [ 0.010,  0.005, -0.002],
    [-0.004,  0.008,  0.001],
    [ 0.006, -0.003,  0.004],
    [ 0.002,  0.011, -0.001],
    [-0.001,  0.002,  0.003],
])

# What .cov() does under the hood:
centered = returns - returns.mean(axis=0)     # step 1: mean-center each asset
n = len(returns)
Sigma_by_hand = (centered.T @ centered) / (n - 1)   # step 2+3: outer-product average

Sigma_numpy = np.cov(returns, rowvar=False)   # the same thing, in one call

print("By hand:\n", Sigma_by_hand)
print("np.cov: \n", Sigma_numpy)
print("Equal:", np.allclose(Sigma_by_hand, Sigma_numpy))
```

`Sigma_by_hand` and `Sigma_numpy` are the same matrix. You can read the diagonal to confirm it really is each asset's $\sigma^2$, and the off-diagonals are the pairwise covariances.

Want me to run this so you can see the actual numbers and point at which entry is which? It's the fastest way to make "Σ is a grid of pairwise covariances" concrete rather than abstract.
