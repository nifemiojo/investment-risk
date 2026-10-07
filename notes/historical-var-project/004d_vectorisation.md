# Vectorisation in pandas — a refresher

**Date:** 2026-07-12
**Topic:** What vectorisation means, three layers of speed, and why our loop is fine
**Turn:** 004d

## User request

Refresher on vectorisation in the context of pandas.

## Work and response

Three layers, from slowest to fastest:

### Layer 1: Python loop over rows (slow)

```python
# Iterating row by row — Python interpreter runs every step
result = []
for i in range(len(df)):
    result.append(df["Close"].iloc[i] / df["Close"].iloc[i - 1] - 1)
```

Every `iloc[i]` is a Python function call. Every division is a Python float operation. For 1,000 rows, fine. For 1,000,000, slow.

### Layer 2: Pandas vectorised operations (fast)

```python
# One operation on the whole column — pandas hands it to NumPy
df["Returns"] = df["Close"].pct_change()
```

What looks like one line of Python is actually: pandas takes the entire "Close" column as a NumPy array, calls C code that does the division on every element in a tight compiled loop, and returns the result. The Python interpreter is invoked once, not once per row.

### Layer 3: NumPy directly (fastest)

```python
# No pandas overhead at all — raw NumPy
returns = np.diff(arr) / arr[:-1]
```

No index alignment, no dtype checking, no Series metadata. Just the raw array operation in C. This is what `.rolling().quantile()` does — it never touches Python for the computation.

### What "vectorised" actually means

It's not about vectors in the mathematical sense. It means: **the loop is in C, not Python**.

```python
# NOT vectorised: Python runs the loop
for price in prices:
    ...

# Vectorised: Python calls one function, C runs the loop
prices.pct_change()
```

The performance difference isn't 2× or 10×. It's 100× to 1000× for large arrays, because Python function call overhead dominates at scale.

### Why our rolling VaR loop is fine

Our loop calls `historical_var()` 1,600 times (once per trading day since 2020). Inside each call, `np.quantile()` is vectorised — it processes 252 numbers in C. The Python loop is just the outer scaffolding. The inner computation is fast.

The rule of thumb: if your loop body is a vectorised NumPy call, a Python loop over 1,000–10,000 iterations is fine. If your loop body does element-by-element Python operations, you need to vectorise it.

### The real trade-off in our case

```python
# Option 1: Loop (outer Python, inner C)
for t in range(252, len(returns)):
    var = historical_var(returns.iloc[t-252:t])  # np.quantile → C

# Option 2: rolling.apply (same thing, hidden)
returns.rolling(252).apply(lambda w: historical_var(w))
```

Both have identical performance — the `.apply()` is just a Python loop under the hood. The `.rolling().quantile()` path is genuinely faster because it eliminates the Python loop entirely, but it can't call our `historical_var()` function.