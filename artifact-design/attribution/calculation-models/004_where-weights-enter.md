Sharp catch — and the answer is that the weights were *never supposed to be in Σ*. They didn't get lost; they live at a different level. Let me show you exactly where the split is, because it's the single most useful distinction in this whole calculation.

## Two different objects, two different levels

We've been building two things, and it's easy to blur them because they share the letter "sigma" nearby:

| Object | What it describes | Weights? |
|---|---|---|
| $\Sigma$ (covariance matrix) | how the **assets** move | **no** |
| $\sigma_p^2 = w^\top \Sigma w$ (portfolio variance) | how the **portfolio** moves | **yes** |

$\Sigma$ is built from **asset returns only** — $r_1, r_2, \dots$ — because "how much does SPY co-move with EFA?" is a property of *the market*, not of *your portfolio*. SPY and EFA have whatever correlation they have, regardless of whether you hold 40% of one or 2% of the other. That fact exists before you make any allocation decision.

The weights are your *decision* — how much of each asset to hold. That's a separate input, and it only enters at the **next** step, when you ask "given these assets move this way, and *I hold them in these proportions*, how volatile is the whole thing?"

## Where the weights actually re-enter

The portfolio return is the weighted sum of asset returns:

$$ r_p = w_1 r_1 + w_2 r_2 = w^\top r $$

Take the variance of that:

$$ \mathrm{Var}(r_p) = \mathrm{Var}(w^\top r) = w^\top \mathrm{Var}(r)\, w = w^\top \Sigma w $$

So the weights don't appear *inside* Σ — they appear **wrapped around it**. That's the whole story of $w^\top\Sigma w$: it's "the asset covariance (weights-free) sandwiched between the weights on both sides."

## The memory hook

Three things in three roles:

- **$\Sigma$** is the **ingredients list** — the raw risk properties of the assets, same for everyone who trades them.
- **$w$** is the **recipe** — your specific choice of proportions.
- **$w^\top\Sigma w$** is the **dish** — the resulting portfolio variance, which depends on both.

The same $\Sigma$ serves *every* portfolio over those assets. Only $w$ changes from one investor to the next. That's precisely why the clean-architecture design separates them: the covariance comes from **returns data** (market), the weights come from the **portfolio definition** (decision). Two sources, two steps.

## In code, the two-step separation made visible

```python
import numpy as np

returns = np.array([
    [ 0.010,  0.005, -0.002],
    [-0.004,  0.008,  0.001],
    [ 0.006, -0.003,  0.004],
    [ 0.002,  0.011, -0.001],
    [-0.001,  0.002,  0.003],
])

# Step 1 — covariance matrix: from returns ONLY, no weights anywhere
Sigma = np.cov(returns, rowvar=False)
print("Sigma (asset-level, no weights):\n", Sigma)

# Step 2 — portfolio variance: weights enter HERE, sandwiching Sigma
weights = np.array([0.40, 0.20, 0.40])
portfolio_variance = weights @ Sigma @ weights
portfolio_volatility = np.sqrt(portfolio_variance)

print("\nportfolio variance:", portfolio_variance)
print("portfolio volatility:", portfolio_volatility)
```

`Sigma` is computed before `weights` even exists in the script. The weights are applied as a separate, later step — and that ordering in the code mirrors the conceptual ordering exactly.

---

So: nothing happened to the weights — they were always the *second* ingredient, applied at the portfolio-variance step. The covariance-matrix step is deliberately weights-free because it's answering a different question ("how do the assets move") from the one the weights answer ("how much did I choose to hold").
