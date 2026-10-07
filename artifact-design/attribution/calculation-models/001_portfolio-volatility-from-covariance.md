This is one of those places where a single symbol is hiding two separate facts. Let me pull them apart, then rebuild the notation from the ground up — because I think the notation itself (the transpose, the matrix product) is where the gap is, not the underlying idea.

## Fact A and Fact B, separated

$$ \sigma_p = \sqrt{w^\top \Sigma w} $$

is two things stacked:

- **Inside the root** is **portfolio variance** — the double sum you already derived in the component-contribution work.
- **The root itself** is just the variance→volatility conversion.

So the only genuinely new piece is "how is $w^\top \Sigma w$ the same thing as that double sum?" Everything else you already have.

## First, what the symbols literally mean

- $w$ is the weight vector written as a **column** (one row per asset):

$$ w = \begin{pmatrix} w_1 \\ w_2 \\ \vdots \\ w_N \end{pmatrix} $$

- $w^\top$ (read "w transpose") is the same numbers laid **sideways as a row**: $(w_1,\ w_2,\ \dots,\ w_N)$. Transposing doesn't change any values — it just flips the orientation so the multiplication lines up.
- $\Sigma$ (capital sigma) is the **covariance matrix** — an $N\times N$ grid where the entry in row $i$, column $j$ is $\operatorname{Cov}(r_i, r_j)$. Its diagonal holds variances (the covariance of an asset with itself), its off-diagonals hold pairwise covariances.

The product $w^\top \Sigma w$ is $(\text{row})\times(\text{matrix})\times(\text{column}) = (1\times N)(N\times N)(N\times 1)$, which collapses to a single number.

## Fact A: the matrix form IS your double sum

From the component-contribution derivation you already trust:

$$ \sigma_p^2 = \operatorname{Var}(r_p) = \sum_i \sum_j w_i\, w_j\, \operatorname{Cov}(r_i, r_j) $$

That double sum is *exactly* what $w^\top \Sigma w$ computes — just written compactly. Let me make it visible with two assets, where $\Sigma$ is:

$$ \Sigma = \begin{pmatrix} \sigma_1^2 & c \\ c & \sigma_2^2 \end{pmatrix}, \qquad c = \operatorname{Cov}(r_1, r_2) $$

First compute $w^\top \Sigma$ (a row vector):

$$ (w_1,\ w_2) \begin{pmatrix} \sigma_1^2 & c \\ c & \sigma_2^2 \end{pmatrix} = \big(\ w_1\sigma_1^2 + w_2 c,\ \ w_1 c + w_2\sigma_2^2\ \big) $$

Then multiply by $w$:

$$ w^\top\Sigma w = (w_1\sigma_1^2 + w_2 c)\,w_1 + (w_1 c + w_2\sigma_2^2)\,w_2 $$

$$ = w_1^2\sigma_1^2 + w_1 w_2 c + w_1 w_2 c + w_2^2\sigma_2^2 $$

$$ = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1 w_2 c $$

That last line is the classic two-asset portfolio variance: each asset's variance scaled by weight², plus the cross term ($2w_1w_2$ times the covariance). The general $N$-asset statement is identical — the matrix product just mechanically produces every $w_i w_j \operatorname{Cov}(r_i,r_j)$ term and adds them up:

$$ w^\top \Sigma w = \sum_{i=1}^{N}\sum_{j=1}^{N} w_i w_j \Sigma_{ij} $$

So: **no new maths, only new spelling.** We write it as a matrix because (a) it's one compact symbol, and (b) NumPy computes it in a single optimised call.

## Fact B: why the square root

Variance is the *average squared* deviation from the mean, so its units are "return²". If a daily return is around $1\% = 0.01$, the variance is around $0.0001$ — a number that doesn't sit on the same scale as returns and is awkward to read.

Volatility (equivalently, standard deviation) is the square root of variance, which puts it back in the **same units as the returns themselves**:

$$ \sigma_p = \sqrt{\sigma_p^2} $$

"Portfolio vol of 1.5% daily" is a number you can hold up against "SPY returned 0.8% today." Variance can't be compared that way. The square root isn't a modelling choice — it's a units correction.

## The connection that ties it back to what you already did

In the plan I also wrote:

```python
covariance_with_portfolio = covariance_matrix @ weights   # this is Σw
```

It's worth seeing the difference between the two matrix expressions, because they're easy to blur:

- $\Sigma w$ is a **vector** — entry $i$ is $\operatorname{Cov}(r_i, r_p)$. You already derived why in 009: $\sum_j w_j \operatorname{Cov}(r_i, r_j) = \operatorname{Cov}(r_i, r_p)$, and row $i$ of $\Sigma w$ is exactly that sum.
- $w^\top\Sigma w = w^\top(\Sigma w)$ is a **scalar** — it's the dot product of the weights with that covariance-with-portfolio vector.

So $w^\top\Sigma w$ is literally "$w$ dotted with the covariance-with-portfolio vector", which written out is:

$$ w^\top\Sigma w = \sum_i w_i \operatorname{Cov}(r_i, r_p) = \sigma_p^2 $$

That is the *same identity* you already trust from the component-contribution work ($\sigma_p^2 = \sum_i w_i \operatorname{Cov}(r_i,r_p)$). The matrix form, the double sum, and the component-contribution sum are three spellings of one equation.

## In code, proving the three spellings agree

```python
import numpy as np

# 3 assets, 5 days of daily decimal returns (made up, small enough to inspect)
returns = np.array([
    [ 0.010,  0.005, -0.002],
    [-0.004,  0.008,  0.001],
    [ 0.006, -0.003,  0.004],
    [ 0.002,  0.011, -0.001],
    [-0.001,  0.002,  0.003],
])

weights = np.array([0.40, 0.20, 0.40])   # must sum to 1

Sigma = np.cov(returns, rowvar=False)    # N×N covariance matrix

# (1) matrix form — what's in the plan doc
variance_matrix = weights @ Sigma @ weights

# (2) the definition, written literally as a double loop
variance_double_sum = 0.0
for i in range(len(weights)):
    for j in range(len(weights)):
        variance_double_sum += weights[i] * weights[j] * Sigma[i, j]

# (3) w dotted with the covariance-with-portfolio vector
cov_with_portfolio = Sigma @ weights            # Σw  → a VECTOR
variance_dot = weights @ cov_with_portfolio     # wᵀ(Σw) → a SCALAR

volatility = np.sqrt(variance_matrix)

print("variance = w @ Σ @ w :", variance_matrix)
print("variance = double sum :", variance_double_sum)
print("variance = w · (Σw)   :", variance_dot)
print("volatility = √variance:", volatility)
```

The three variance lines print the same number, and `volatility` is its square root. If you'd like, I can run it so you can see the actual covariance matrix and the three agreeing values side by side.

Two footnotes that will matter later, flagged now so they don't surprise you:

1. **"Structural" vs "true" volatility** — the $\Sigma$ we actually use is an *estimate* from the trailing window (via `.cov()`), not the population's true covariance. That's precisely why the artifact's boundary note says "structural portfolio volatility over the estimation window" — we're measuring the volatility *implied by the recent history*, not an unknown ground truth.
2. **The `n−1` divisor** — both pandas `.cov()` and `np.cov` use *sample* covariance by default (divide by $n-1$, not $n$). It's a small, defensible correction, but it's a choice baked into whatever number comes out. Happy to go into why `n−1` if it's part of the stats refresh — just say the word.
