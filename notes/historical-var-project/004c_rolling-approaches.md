# Rolling calculation approaches in pandas + return type design

**Date:** 2026-07-12
**Topic:** Alternatives to Python loops for rolling calculations, and DataFrame vs custom objects
**Turn:** 004c

## User request

Why use a loop instead of pandas-native rolling? Why return a custom object rather than a DataFrame?

## Work and response

### 1. The loop vs. pandas-native rolling

Three approaches, ordered from most explicit to most pandas-idiomatic:

**Approach A: Python loop**

```python
for t in range(window, len(returns)):
    var = historical_var(returns.iloc[t - window : t], confidence=0.95)
```

Pro: completely transparent. You can see every step, drop in print statements, debug anything. Con: feels like C# in Python — you're manually managing indices.

**Approach B: `Series.rolling().apply()`**

```python
var_series = returns.shift(1).rolling(window=window).apply(
    lambda w: historical_var(w, confidence=0.95)
)
```

This is pandas' built-in sliding window. `.rolling(252)` creates 252-element windows that slide forward one step at a time. `.apply(func)` calls your function on each window. The `.shift(1)` is critical — it pushes every return forward by one day, so the window for Tuesday contains Monday and earlier, never Tuesday itself.

Pro: concise, idiomatic pandas. Con: `.apply()` is a Python loop under the hood anyway — it's not vectorised. And debugging a lambda inside `.apply()` is a black box compared to a for-loop.

**Approach C: `Series.rolling().quantile()` (bypasses our function)**

```python
var_series = -returns.shift(1).rolling(window=window).quantile(1 - confidence)
```

This is the fastest possible path — `.rolling().quantile()` is implemented in C. But it bypasses our `historical_var()` function entirely: no validation, no sign convention documentation, no method mapping. It's what you'd write in a throwaway notebook, not in a library.

**Recommendation:**

| Approach | Speed | Debuggable | Uses our function | 
|----------|-------|------------|-------------------|
| A (loop) | Same as B | Yes | Yes |
| B (rolling.apply) | Same as A | No | Yes |
| C (rolling.quantile) | Fastest | N/A | No |

For this project, Approach A (loop) is the right call. A and B have identical performance — `.apply()` is a Python loop. The difference is transparency. When you're learning how VaR behaves, you want to be able to inspect what's happening at each step. The loop lets you do that. The `.apply()` hides it.

### 2. Why return a DataFrame?

The list-of-dicts was just pseudocode. The real return should be a `pd.DataFrame` with a DatetimeIndex:

```python
def rolling_var(returns, window=252, confidence=0.95) -> pd.DataFrame:
    ...
    return pd.DataFrame({
        "VaR": var_values,
        "NextReturn": next_returns,
        "Breach": breaches,
    }, index=dates)
```

This gives you:
- `.plot()` directly on the result
- `.describe()` for summary stats
- `.to_csv()` for export
- `.loc["2020-03"]` for date-based slicing

The DataFrame is the native currency for downstream work. The list of dicts was just the build step — the return type is a DataFrame.