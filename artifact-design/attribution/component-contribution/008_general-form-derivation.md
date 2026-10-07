# General Form: From Two Assets to N Assets and the Regrouping Trick

A walkthrough of how the two-asset variance formula generalises to N assets, and how the double sum regroups into per-asset contributions. No prior knowledge assumed.

## Step 1: The three-asset case (to see the pattern)

For SPY, EFA, IEF with weights $w_1, w_2, w_3$:

$$r_p = w_1 r_1 + w_2 r_2 + w_3 r_3$$

We square this sum. The rule for squaring a sum of three terms is *every term times every term*:

$$(a + b + c)^2 = a^2 + b^2 + c^2 + 2ab + 2ac + 2bc$$

So the variance becomes:

$$\sigma_p^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + w_3^2\sigma_3^2 + 2w_1 w_2\text{Cov}(r_1,r_2) + 2w_1 w_3\text{Cov}(r_1,r_3) + 2w_2 w_3\text{Cov}(r_2,r_3)$$

Three "self" terms, three "pair" terms.

## Step 2: See the table

Visualise this as a grid. Write each asset's weighted deviation as a row and a column, then fill in every cell with the product:

|  | $w_1(r_1-\mu_1)$ | $w_2(r_2-\mu_2)$ | $w_3(r_3-\mu_3)$ |
|---|---|---|---|
| $w_1(r_1-\mu_1)$ | $w_1^2(r_1-\mu_1)^2$ | $w_1 w_2(r_1-\mu_1)(r_2-\mu_2)$ | $w_1 w_3(r_1-\mu_1)(r_3-\mu_3)$ |
| $w_2(r_2-\mu_2)$ | $w_2 w_1(r_2-\mu_2)(r_1-\mu_1)$ | $w_2^2(r_2-\mu_2)^2$ | $w_2 w_3(r_2-\mu_2)(r_3-\mu_3)$ |
| $w_3(r_3-\mu_3)$ | $w_3 w_1(r_3-\mu_3)(r_1-\mu_1)$ | $w_3 w_2(r_3-\mu_3)(r_2-\mu_2)$ | $w_3^2(r_3-\mu_3)^2$ |

Every cell is a product. Add them all up and take expectations:

- The **diagonal** cells: $w_i^2 \mathbb{E}[(r_i - \mu_i)^2] = w_i^2\sigma_i^2$ — the variances.
- The **off-diagonal** cells: $w_i w_j \mathbb{E}[(r_i-\mu_i)(r_j-\mu_j)] = w_i w_j \text{Cov}(r_i, r_j)$ — the covariances.

There are 9 cells total: 3 diagonal, 6 off-diagonal. The grid has $n^2$ cells, $n$ on the diagonal and $n^2 - n = n(n-1)$ off the diagonal. Each pair appears twice (cell $(i,j)$ and cell $(j,i)$), so we get $n(n-1)/2$ *distinct* pairs. For 3 assets: $3 \times 2 / 2 = 3$ pairs.

## Step 3: Compress with the double sum

Let $i$ label the row and $j$ label the column. "Add up every cell in the grid" becomes:

$$\sigma_p^2 = \sum_{i=1}^n \sum_{j=1}^n w_i w_j \, \text{Cov}(r_i, r_j)$$

Reading it: for each $i$ (each row), sum over all $j$ (every column), and add up all the resulting terms. The inner sum runs across a row; the outer sum stacks the rows.

- When $i = j$: $\text{Cov}(r_i, r_i) = \text{Var}(r_i) = \sigma_i^2$, and the cell is $w_i^2 \sigma_i^2$ — a diagonal term.
- When $i \neq j$: the cell is $w_i w_j \text{Cov}(r_i, r_j)$ — an off-diagonal term.

One expression captures *all* $n^2$ cells without enumerating them.

## Step 4: The regrouping — from grid to contributions

The double sum answers "what's the total variance?" We want "which asset is responsible for how much?"

The insight: **group by row**. Each row $i$ contains asset $i$'s interactions with every asset (including itself). Pull out the common factor $w_i$ from row $i$:

$$\sigma_p^2 = \sum_i w_i \underbrace{\left[\sum_j w_j \, \text{Cov}(r_i, r_j)\right]}_{\text{row } i \text{'s total}}$$

The bracket is row $i$ in the grid, summed across all columns $j$:

$$\sum_j w_j \text{Cov}(r_i, r_j) = w_1\text{Cov}(r_i, r_1) + w_2\text{Cov}(r_i, r_2) + \dots + w_n\text{Cov}(r_i, r_n)$$

This is "how much asset $i$ co-moves with everything in the portfolio, weighted by how much of each thing you hold" — which is precisely covariance with the *portfolio*:

$$\text{Cov}(r_i, r_p) = \text{Cov}\!\left(r_i, \sum_j w_j r_j\right) = \sum_j w_j \text{Cov}(r_i, r_j)$$

(The second equality is covariance's linearity: the covariance of $r_i$ with a weighted sum is the weighted sum of covariances.)

Substituting back:

$$\sigma_p^2 = \sum_i w_i \, \text{Cov}(r_i, r_p)$$

## Step 5: What this means

Each term $w_i \text{Cov}(r_i, r_p)$ is asset $i$'s **contribution to portfolio variance**. The whole derivation:

1. Variance of a sum = sum of all cells in the covariance grid (bilinearity).
2. Group the grid by rows, one row per asset.
3. Each row's total is $w_i \times \text{Cov}(r_i, r_p)$.
4. The sum of all row totals = total variance.

The additivity (pieces sum exactly to $\sigma_p^2$) is guaranteed by construction — no cell was dropped or double-counted, just rearranged.

## Step 6: A sanity check with the two-asset case

For $n = 2$:

$$\sigma_p^2 = w_1\text{Cov}(r_1, r_p) + w_2\text{Cov}(r_2, r_p)$$

First term:

$$w_1\text{Cov}(r_1, r_p) = w_1\text{Cov}(r_1, w_1 r_1 + w_2 r_2) = w_1[w_1 \text{Cov}(r_1, r_1) + w_2 \text{Cov}(r_1, r_2)] = w_1^2 \sigma_1^2 + w_1 w_2 \text{Cov}(r_1, r_2)$$

Similarly:

$$w_2\text{Cov}(r_2, r_p) = w_2^2 \sigma_2^2 + w_1 w_2 \text{Cov}(r_1, r_2)$$

Add them:

$$\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \text{Cov}(r_1, r_2)$$

Exactly the two-asset formula. The contribution form splits the $2 w_1 w_2 \text{Cov}$ term in half — half credited to asset 1, half to asset 2 — which is why it "adds up" while still being fair.

## The one-sentence summary

The general form is just "square a sum of $n$ terms, which produces an $n \times n$ grid of pairwise products; write that grid compactly as a double sum; then group the grid by rows — each row is one asset's covariance with the portfolio, scaled by its weight, and those rows sum to the total."
