Good — that line hides a jump that the previous sections didn't flag. In the single-asset case, $r$ and $\mu$ were **single numbers** (scalars). That line silently promotes both to **lists** (vectors), and the promotion is where the confusion lives. Let me make that promotion explicit.

## Step 1: what $r$ and $\mu$ *were*

For **one asset**, "the return" is one number:

- $r$ = this asset's return, e.g. $0.010$ (1%)
- $\mu$ = this asset's average return, e.g. $0.004$

So $r - \mu$ is one number minus one number = one number (the deviation). Nothing new.

## Step 2: what happens with *two* assets

Now there isn't "a return" — there are **two returns at once** (one per asset), and **two means**. So "$r$" has to stand for *both* numbers at the same time. The notation we use for "a list of numbers, one per asset" is a vector:

$$ r = \begin{pmatrix} r_1 \\ r_2 \end{pmatrix}, \qquad \mu = \begin{pmatrix} \mu_1 \\ \mu_2 \end{pmatrix} $$

where $r_1$ is asset 1's return and $r_2$ is asset 2's return (same for the means).

## Step 3: the subtraction is just "do it once per asset"

When you subtract two vectors, the rule is **element by element** — match up position 1 with position 1, position 2 with position 2:

$$ r - \mu = \begin{pmatrix} r_1 \\ r_2 \end{pmatrix} - \begin{pmatrix} \mu_1 \\ \mu_2 \end{pmatrix} = \begin{pmatrix} r_1 - \mu_1 \\ r_2 - \mu_2 \end{pmatrix} $$

That's the entire line. It isn't a new operation — it's the *same* "$r - \mu$" subtraction you already did for one asset, just applied to each asset in turn and stacked into a column. The vector notation is shorthand for "subtract each asset's mean from its own return, all at once."

## Concrete numbers so it's not abstract

Take two assets on one particular day:

| | Asset 1 | Asset 2 |
|---|---|---|
| return $r$ | 0.010 | 0.005 |
| mean $\mu$ | 0.004 | 0.003 |

The vector of returns is $r = (0.010,\ 0.005)$, the vector of means is $\mu = (0.004,\ 0.003)$, and the deviation vector is:

$$ r - \mu = \begin{pmatrix} 0.010 - 0.004 \\ 0.005 - 0.003 \end{pmatrix} = \begin{pmatrix} 0.006 \\ 0.002 \end{pmatrix} $$

Asset 1 is $0.006$ above its own mean; asset 2 is $0.002$ above its own mean. Two numbers, one vector.

## Why this matters for the next step

The reason we care is the line *after* it. The variance definition was "square the deviation, then average." With one asset, "square the deviation" was $(r-\mu)^2$ — squaring a scalar. With two assets, "the deviation" is now a *vector*, so to "square" it we take the outer product $(r-\mu)(r-\mu)^\top$, which is what turns the $2\times1$ column into the $2\times2$ matrix. The vector line you asked about is the bridge that makes that "squaring a vector" step possible.

## In code, the same promotion

```python
import numpy as np

# ONE asset: r and mu are scalars
r_1 = 0.010
mu_1 = 0.004
deviation_1 = r_1 - mu_1          # a single number: 0.006

# TWO assets: r and mu are vectors (arrays)
r = np.array([0.010, 0.005])      # returns of asset 1 and asset 2
mu = np.array([0.004, 0.003])     # means  of asset 1 and asset 2
deviation = r - mu                # element-wise: [0.006, 0.002]

print("one asset  :", deviation_1)   # 0.006
print("two assets :", deviation)     # [0.006 0.002]
```

NumPy's `r - mu` on two arrays does exactly the element-by-element subtraction the vector notation describes — subtract matching positions. The "vector" is just a NumPy array; the "element-wise subtraction" is just `r - mu`.

---

The one thing to lock in: **a vector here is just a numbered list — one slot per asset — and vector subtraction is doing the same familiar subtraction in each slot.** Nothing else is going on.
