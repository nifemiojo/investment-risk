Good — this is a real gap worth closing, because "axis" trips up almost everyone coming from C# where you'd write the loop yourself. Let me build it from the shape of the array.

## What `returns` actually is

In the notebook, `returns` has shape `(6, 4)`:

- **6 rows** = days (axis 0)
- **4 columns** = assets (axis 1)

```
              SPY     EFA     IEF     GLD     ← axis 1 (columns = assets)
day 1  [     0.010   0.008  -0.003   0.002 ]
day 2  [    -0.004  -0.002   0.005   0.001 ]
day 3  [     0.006   0.005  -0.004   0.003 ]
day 4  [     0.002   0.001   0.003  -0.001 ]
day 5  [    -0.001   0.000  -0.002   0.002 ]
day 6  [     0.005   0.004  -0.001   0.000 ]
  ↑
axis 0 (rows = days)
```

In NumPy, **axis 0 is the first dimension (rows), axis 1 is the second (columns)**. `axis=0` literally means "the dimension at position 0."

## What `axis=` means when you aggregate

`mean` collapses a dimension. The rule:

> **The axis you pass is the axis that disappears.**

So `returns.mean(axis=0)` means "average *along* the days direction" — squash the 6 rows down into 1. You're left with one number **per column** (per asset).

```
mean(axis=0)  →  [ 0.003,  0.002667,  -0.000333,  0.001167 ]
                   └ SPY ┘ └── EFA ──┘ └── IEF ───┘ └── GLD ┘
```

Shape goes `(6, 4)` → `(4,)`. The `6` (days) vanished; the `4` (assets) survived.

## Why "collapse the rows" gives one number per *column*

Because averaging *down* a column is exactly "sum all the days in that column, divide by the count." For SPY:

$$ \frac{0.010 + (-0.004) + 0.006 + 0.002 + (-0.001) + 0.005}{6} = \frac{0.018}{6} = 0.003 $$

Same for each asset column. That's SPY's **mean return** — the $\mu_1$ from our earlier docs.

## The contrast: what `axis=1` would do

`returns.mean(axis=1)` collapses the *columns* instead — average across assets within each day. You'd get one number per **day** (6 of them), which is mostly meaningless here (averaging SPY with IEF on the same day mixes unrelated things). That's how you can tell axis=0 is right: we want one mean *per asset*, assets are columns, so we collapse the rows.

## The C# bridge

`returns.mean(axis=0)` is NumPy's built-in version of this loop you'd write yourself in C#:

```csharp
double[] assetMeans = new double[numAssets];
for (int asset = 0; asset < numAssets; asset++)
{
    double sum = 0;
    for (int day = 0; day < numDays; day++)
        sum += returns[day, asset];
    assetMeans[asset] = sum / numDays;
}
```

The outer loop runs over **columns** (assets); the inner loop runs over **rows** (days). "axis=0" is just NumPy saying "the dimension I'm averaging over is the rows" — the inner loop — in one word instead of two nested loops.

## Why this particular step exists at all

Mean-centring is the first step of building Σ (doc `002`). Variance measures spread *around the mean*, so before we can square deviations we need each asset's mean. `returns.mean(axis=0)` gives all four means at once, so the next line —

```python
centered = returns - means    # each asset minus its own mean
```

— can subtract the right mean from the right column, element-wise, in one shot.

## Memory hook

Two things to lock in:

1. **axis 0 = rows, axis 1 = columns** (first index = down, second = across).
2. **The axis you pass is the axis you remove.** `mean(axis=0)` removes the rows, leaving one value per column.
