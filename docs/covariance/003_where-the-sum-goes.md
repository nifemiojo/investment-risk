This is the exact right thing to be confused about, because you've spotted a real asymmetry between the scalar case and the matrix case. The short version: **the outer product is not one number — it's a full $N\times N$ matrix — so the summation sums $n$ matrices, not $n$ numbers.**

Let me unpack that.

## The thing you're missing: the outer product is a matrix per day

For **one** variable, the squared deviation $(r-\mu)^2$ is a **single number**. So the estimator

$$ \frac{1}{n-1}\sum_t (r_t - \mu)^2 $$

is a sum of $n$ numbers. Clean, familiar.

For **$N$ variables**, the "deviation" is a *vector* $x_t = r_t - \mu$ (one entry per asset), and to "square" a vector you take the **outer product**, which is a full $N\times N$ matrix:

$$ x_t x_t^\top = \begin{pmatrix} x_{t1}^2 & x_{t1}x_{t2} \\ x_{t2}x_{t1} & x_{t2}^2 \end{pmatrix} $$

So *each day $t$ contributes a whole matrix*, not a number. That's the asymmetry: the summand is an $N\times N$ grid, so the sum is a sum of grids.

## Where the summation goes

The sum is over **days** ($t$), not over matrix entries. You stack up one matrix per day and add them **entry by entry** — the $(i,j)$ cell of day 1 plus the $(i,j)$ cell of day 2 plus …:

$$ \sum_{t=1}^{n} x_t x_t^\top = \begin{pmatrix} \sum_t x_{t1}^2 & \sum_t x_{t1}x_{t2} \\[2pt] \sum_t x_{t2}x_{t1} & \sum_t x_{t2}^2 \end{pmatrix} $$

Then divide every cell by $n-1$. So the summation doesn't "go" somewhere mysterious — it lands in each cell, and each cell's sum is over the *days*. The covariance between asset 1 and asset 2 is:

$$ \hat\Sigma_{12} = \frac{1}{n-1}\sum_{t=1}^{n} x_{t1}\, x_{t2} $$

That's the textbook scalar formula you already know. The matrix form is just *all four* of those scalar sums written in one object.

## Worked example — 2 assets, 3 days, every step visible

Returns:

| Day | Asset 1 | Asset 2 |
|---|---|---|
| 1 | 0.02 | 0.01 |
| 2 | −0.02 | 0.00 |
| 3 | 0.03 | 0.02 |

Means: $\bar r_1 = 0.01$, $\bar r_2 = 0.01$. Centred rows $x_t = r_t - \bar r$:

| Day | $x_{t1}$ | $x_{t2}$ |
|---|---|---|
| 1 | 0.01 | 0.00 |
| 2 | −0.03 | −0.01 |
| 3 | 0.02 | 0.01 |

Now the outer product **per day** (three separate $2\times2$ matrices):

$$ \text{Day 1: } x_1 x_1^\top = \begin{pmatrix} 0.0001 & 0 \\ 0 & 0 \end{pmatrix} $$

$$ \text{Day 2: } x_2 x_2^\top = \begin{pmatrix} 0.0009 & 0.0003 \\ 0.0003 & 0.0001 \end{pmatrix} $$

$$ \text{Day 3: } x_3 x_3^\top = \begin{pmatrix} 0.0004 & 0.0002 \\ 0.0002 & 0.0001 \end{pmatrix} $$

Add them cell by cell:

$$ \sum_t x_t x_t^\top = \begin{pmatrix} 0.0001{+}0.0009{+}0.0004 & 0{+}0.0003{+}0.0002 \\ 0{+}0.0003{+}0.0002 & 0{+}0.0001{+}0.0001 \end{pmatrix} = \begin{pmatrix} 0.0014 & 0.0005 \\ 0.0005 & 0.0002 \end{pmatrix} $$

Divide by $n-1 = 2$:

$$ \hat\Sigma = \begin{pmatrix} 0.0007 & 0.00025 \\ 0.00025 & 0.0001 \end{pmatrix} $$

Spot-check: the (1,2) entry is the sample covariance of assets 1 and 2:

$$ \frac{(0.01)(0.00) + (-0.03)(-0.01) + (0.02)(0.01)}{2} = \frac{0 + 0.0003 + 0.0002}{2} = 0.00025 \quad\checkmark $$

So the summation is over $t$, and it happens *inside each cell* of the resulting matrix.

## Why $X_c^\top X_c$ is the compact form of exactly that sum

Here's the payoff. $X_c$ has the centred rows stacked (days as rows). The product $X_c^\top X_c$ is precisely "sum of the outer products":

$$ X_c^\top X_c = \sum_{t=1}^{n} x_t x_t^\top $$

(Each term $x_t x_t^\top$ is the outer product of row $t$ with itself; the matrix multiply accumulates them.) So:

$$ \hat\Sigma = \frac{1}{n-1} X_c^\top X_c = \frac{1}{n-1}\sum_{t=1}^{n} x_t x_t^\top $$

The matrix notation is not a *different* summation — it's the same "sum over days" rewritten so the $\sum_t$ disappears into one matrix multiplication.

## One thing to NOT confuse it with

There *is* a legitimate operation where you sum the matrix entries into a single number: it's the **trace** (sum of the diagonal), and it gives *total variance*, not covariance. But that's not what $\sum_t$ is doing here. Two different sums:

- $\sum_t$ → sums **across days**, producing a matrix. (This is our estimator.)
- $\sum_i$ of the diagonal → sums **across assets**, producing a scalar. (Total variance, a different thing.)

The $\frac{1}{n-1}\sum_t$ you're asking about is the first one.

## One-line summary

The outer product of a vector is an $N\times N$ **matrix** (not a number), so the estimator $\frac{1}{n-1}\sum_t x_t x_t^\top$ is a sum of $n$ matrices added entry-by-entry — equivalently, the sum over days lands *inside each cell*, giving $\hat\Sigma_{ij} = \frac{1}{n-1}\sum_t x_{ti} x_{tj}$.
