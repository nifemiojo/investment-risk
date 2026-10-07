Yes — with **one crucial qualifier** that's easy to miss and is the difference between "right" and "silently wrong."

## The short answer

$$ \Sigma = \frac{1}{n-1} X^\top X $$

is the sample covariance matrix **if and only if $X$ is the *centred* data** — the data with each column's mean already subtracted. If $X$ is the *raw* returns, the same formula gives you the wrong thing (a "second moment", not a covariance).

So the honest version is:

$$ \Sigma = \frac{1}{n-1}\, X_c^\top X_c, \qquad \text{where } X_c = X - \mu $$

The centring isn't an optional nicety — it's what makes the formula *covariance* at all.

## Why centring is the whole point

Covariance measures spread *around the mean*. The definition from doc `002` was:

$$ \Sigma = \mathbb{E}\big[(r - \mu)(r - \mu)^\top\big] $$

The matrix formula is just the **sample version** of that same definition, where the expectation $\mathbb{E}[\cdot]$ (a theoretical average) is replaced by a finite-sample average $\frac{1}{n-1}\sum_t$:

$$ \mathbb{E}\big[(r-\mu)(r-\mu)^\top\big] \;\longrightarrow\; \frac{1}{n-1}\sum_{t=1}^{n} (r_t - \mu)(r_t - \mu)^\top $$

And summing the outer products of the centred rows *is* $X_c^\top X_c$ (rows stacked on top of each other → $X_c^\top X_c$ sums them). So:

$$ \Sigma = \frac{1}{n-1} X_c^\top X_c $$

That's the whole identity. "Matrix form of sample covariance" is exactly right — the matrix notation just collapses the per-entry double definition into one expression.

## The subtle distinction: "second moment" vs "covariance"

This is where the qualifier bites. For a single variable, there are two related-but-different quantities:

- **Second moment** (average of *squared values*): $\frac{1}{n}\sum r_t^2$ — this is *not* centred.
- **Variance** (average of *squared deviations*): $\frac{1}{n-1}\sum (r_t - \mu)^2$ — centred.

They're related by $\mathrm{Var}(r) = \mathbb{E}[r^2] - \mu^2$. The same split exists in matrix form:

| Formula | $X$ is | What you get |
|---|---|---|
| $\frac{1}{n-1} X^\top X$ | raw returns | **second-moment matrix** $\approx \mathbb{E}[rr^\top]$ |
| $\frac{1}{n-1} X_c^\top X_c$ | centred returns | **covariance matrix** $\Sigma$ |

They differ by the outer product of the means, $\mu\mu^\top$. If your means are *exactly zero* they coincide — which is why it's a tempting mistake: with small daily returns near zero, raw vs centred look "almost" the same, so the bug is easy to miss and hard to notice. But it's still wrong, and it silently biases every number downstream.

## Unpacked to a single entry

To see it really is "just" the covariance, look at entry $(i,j)$ of $X_c^\top X_c$:

$$ (X_c^\top X_c)_{ij} = \sum_{t=1}^{n} (r_{ti} - \mu_i)(r_{tj} - \mu_j) $$

Divide by $n-1$ and you have exactly the **sample covariance of asset $i$ with asset $j$** — the textbook formula. On the diagonal ($i=j$) it's the sample *variance* of asset $i$. So the matrix is literally "the sample covariance for every pair, written as one object."

## The $n-1$, flagged not explained

The $n-1$ (instead of $n$) is **Bessel's correction**, and it's precisely what makes this the *sample* covariance rather than a plain average. You flagged earlier that you'd want the full story on it — it deserves its own doc, so I'll just name it here and leave the *why* for when you ask.

## In code, proving both halves of the claim

```python
import numpy as np

returns = np.array([
    [ 0.010,  0.008, -0.003,  0.002],
    [-0.004, -0.002,  0.005,  0.001],
    [ 0.006,  0.005, -0.004,  0.003],
    [ 0.002,  0.001,  0.003, -0.001],
    [-0.001,  0.000, -0.002,  0.002],
    [ 0.005,  0.004, -0.001,  0.000],
])

n = returns.shape[0]

# Centred data — the qualifier
centered = returns - returns.mean(axis=0)

# (a) sample covariance via the matrix formula, on CENTRED data
sigma_matrix = (centered.T @ centered) / (n - 1)

# (b) numpy's built-in sample covariance
sigma_numpy = np.cov(returns, rowvar=False)

# (c) the WRONG version — matrix formula on RAW data
sigma_wrong = (returns.T @ returns) / (n - 1)

print("matrix formula (centred) == np.cov?",
      np.allclose(sigma_matrix, sigma_numpy))
print("\nmatrix formula on RAW data == np.cov?",
      np.allclose(sigma_wrong, sigma_numpy))
print("raw differs by the means' outer product:\n",
      sigma_wrong - sigma_matrix)
```

The first check prints `True`, the second `False`. The difference `sigma_wrong - sigma_matrix` is (approximately) $\mu\mu^\top$ — the exact term that separates "second moment" from "covariance".

## Memory hook

1. $\frac{1}{n-1}X^\top X$ is the sample covariance **only when $X$ is centred**. The centring is what makes it *covariance* rather than *second moment*.
2. Centred ↔ covariance; raw ↔ second moment; they differ by $\mu\mu^\top$.
3. In code it's a two-step: `centered = X - X.mean(axis=0)`, then `Sigma = centered.T @ centered / (n-1)` — and `np.cov` does both for you.
