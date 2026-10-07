Good question to sharpen — because the honest answer is: **it doesn't depend on the *count* of means, it depends on the *shape*.** NumPy has no idea what "columns" mean; it only knows dimensions. Two outcomes: it either broadcasts silently, or it raises an error. There's no third option where it "sort of" subtracts.

## The two possibilities

### 1. Shape broadcasts → NumPy subtracts, no complaint

Broadcasting is a mechanical shape rule. It works whenever the two shapes are "compatible" — equal, or one is `1`. That can produce a *valid* result even when it's *semantically* not what you intended. The shapes, against `returns (6, 4)`:

| `means` shape | Broadcasts? | Result | What it actually subtracts |
|---|---|---|---|
| `(4,)` | ✅ | `(6, 4)` | each asset's mean, per asset, across days — **what we want** |
| `(1, 4)` | ✅ | `(6, 4)` | same as above (a row vector) |
| `(6, 1)` | ✅ | `(6, 4)` | one mean **per day**, repeated across assets — **valid but wrong** |
| `(4, 1)` | ❌ | error | — |
| `(6,)` | ❌ | error | — |
| `(3,)` | ❌ | error | — |

Look at the `(6, 1)` row. It has **one** value per column, yet it broadcasts fine — because the trailing dimension is `1`, which stretches to `4`. NumPy happily subtracts a per-*day* number from every asset on that day. That's a completely different (and here, meaningless) calculation, and NumPy will never warn you.

**That's the real answer to your question:** NumPy will not tell you the means "don't match the columns." It only cares whether the shapes are broadcast-compatible. If they happen to be — even in a way that's semantically wrong — it runs silently.

### 2. Shape doesn't broadcast → NumPy refuses

If the trailing dimensions clash (neither equal nor `1`), NumPy raises immediately, before computing anything:

```python
returns - np.zeros(3)   # (6,4) vs (3,)
```

```text
ValueError: operands could not be broadcast together with shapes (6,4) (3,)
```

The message names both shapes and points at the mismatch. This is the *good* failure: it stops you, rather than producing garbage. The bad failure is the `(6,1)` case, which doesn't stop you at all.

## The precise rule, restated

For `returns (6, 4)` and `means` of any shape, align right-to-left and check each pair:

- equal → OK;
- one is `1` → OK, stretch it;
- anything else (e.g. `4 vs 3`) → **ValueError**.

The only shapes that *fail* are the ones whose trailing dimensions are genuinely different and neither is `1`.

## Why this matters for us specifically

Our line is correct *only because of our convention* — days as rows (`6`), assets as columns (`4`), so `means = returns.mean(axis=0)` naturally has shape `(4,)`, which aligns to the assets. If we ever transposed the data (assets as rows), `means` would still be `(4,)` but it would align to the *rows* and silently subtract per-asset instead of per-day. Nothing would error. The shape rule won't save us — the convention does.

## One flag: pandas behaves differently

This is pure NumPy behaviour (our notebook's `returns` is a `np.array`). But in the real engine you're often holding a `pandas` `DataFrame`. There, `df - series` does **label alignment**, not broadcasting: it matches on index and column *names*. So a Series whose columns don't match can produce `NaN`s (or drop/misalign) rather than a shape error. Same word — "subtract a vector" — very different failure mode. Worth keeping separate in your head.

## Memory hook

1. NumPy never checks *meaning* — it checks *shape*. `(6,1)` is "valid" even when it's wrong.
2. Incompatible shapes raise a `ValueError` naming both shapes.
3. The silent-but-wrong case is more dangerous than the error. We rely on the days-as-rows convention, not on NumPy, to keep the subtraction correct.
