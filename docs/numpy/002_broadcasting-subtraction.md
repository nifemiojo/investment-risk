This is NumPy **broadcasting** — the single most useful (and most commonly confused) behaviour in NumPy. Let me build it from the shapes.

## The shapes, side by side

```python
returns   →  (6, 4)    6 days,  4 assets
means     →  (4,)      4 asset-means (one per column)
```

They have *different* shapes, yet `returns - means` works. The question is: *how does NumPy line them up?* The answer is a rule, not magic.

## The broadcasting rule

NumPy aligns shapes from the **right-hand side** (the *trailing* dimensions), then stretches the smaller one. Two steps:

**Step 1 — pad the smaller shape on the left with 1s:**

```
returns   (6, 4)
means     (4,)   →   (1, 4)      ← pad on the left
```

**Step 2 — compare dimension by dimension, right to left:**

```
returns   (6, 4)
means     (1, 4)
           │  │
           │  └── 4 vs 4 → match, keep 4
           └───── 6 vs 1 → 1 stretches to 6
```

Result shape: `(6, 4)`. Where one dimension is `1`, NumPy treats that dimension as "repeat this single value across all the others." So the one-row `means` is *virtually copied* down all 6 days.

## Why it aligns to the *columns* (assets)

This is the subtle part that makes the line *correct*. Because broadcasting aligns from the **right**, the `(4,)` in `means` matches `returns`'s **last** dimension — the 4 assets — *not* the 6 days. So `means` is treated as "one value per asset", and it gets repeated across days.

Which is exactly what we want: **each asset's mean is subtracted from that same asset, on every day.**

```
means = [   SPY        EFA        IEF        GLD     ]
        [ 0.003000,  0.002667,  -0.000333,  0.001167 ]

returns - means  →  every row subtracts this same vector:

day 1:  [0.010-0.003,  0.008-0.002667,  -0.003-(-0.000333),  0.002-0.001167]
day 2:  [ -0.004-0.003, -0.002-0.002667, 0.005-(-0.000333),  0.001-0.001167]
...     (same subtraction, repeated for all 6 days)
```

## The "virtual copy" is free

When NumPy stretches `(1, 4)` → `(6, 4)`, it does **not** actually allocate a 6×4 array with the means duplicated. It remembers "this dimension is broadcast" and applies the single row to every position at compute time. Zero extra memory, zero copying — that's what makes broadcasting fast, and it's why the idiom `returns - means` beats writing a loop.

## The C# bridge

`returns - means` is NumPy's version of:

```csharp
double[,] centered = new double[numDays, numAssets];
for (int day = 0; day < numDays; day++)
    for (int asset = 0; asset < numAssets; asset++)
        centered[day, asset] = returns[day, asset] - means[asset];
                                              // ^ notice: means[asset], not means[day]
```

The inner loop indexes `means` by `asset` only — the mean stays constant across `day`. Broadcasting does exactly that: it holds `means[asset]` fixed while `day` varies.

## The gotcha that proves the rule matters

If `means` had shape `(6,)` instead of `(4,)`, broadcasting would align that `6` against `returns`'s *last* dimension (4) — and `6 vs 4` is a mismatch:

```
returns   (6, 4)
wrong     (6,)   →  (1, 6)   →  trailing dims 4 vs 6  →  ERROR
```

NumPy would raise a shape error rather than silently subtract per-day. That failure is *useful* — it's broadcasting telling you "these don't line up the way you think." It only silently works when the shapes genuinely agree right-to-left.

## When broadcasting is NOT subtraction-by-position

Worth naming so you don't over-generalise: broadcasting works because `(4,)` matches the trailing dimension. It is **not** "subtract matching elements ignoring shape." If `returns` were `(4, 6)` (transposed — assets as rows), then `means` of shape `(4,)` would align to the *first* axis and the whole thing would mean something different. Shape order *is* the meaning in NumPy — which is why our convention (days as rows, assets as columns) is load-bearing.

## Memory hook

1. **Broadcasting aligns from the right**, pads the shorter shape with 1s on the left, and stretches any `1` dimension to match.
2. A `(4,)` array paired with a `(6, 4)` array aligns to the **columns** — so it subtracts per-column (per-asset), repeated across rows (days).
3. It's **free** (no actual copy) and it's the exact equivalent of an inner loop that indexes the small array by `asset` only.
