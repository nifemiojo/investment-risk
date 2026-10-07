# Why NumPy arrays internally, not pandas Series or Python lists

**Date:** 2026-07-12
**Topic:** Why historical_var works with numpy arrays internally
**Turn:** 002c

## User request

Why work internally with a numpy array rather than a pandas series or python list?

## Work and response

Three reasons, ordered by what actually matters for this function:

### 1. Vectorised operations are the whole point

The core of the function is `np.percentile(arr, ...)`. That's a single call that operates on the entire array at once — no loop, no indexing, no Python interpreter in the hot path. NumPy hands it off to compiled C. Compare:

```python
# NumPy: one C call, ~microseconds
np.percentile(arr, 5.0)

# Python list: you'd need to sort, compute index, interpolate — all in Python loops
# Pandas Series: Series.quantile() works, but it calls np.percentile under the hood anyway
```

For a 252-element array the difference is negligible, but it's the principle: the function does one mathematical operation on the whole dataset. NumPy is the native language for that.

### 2. NumPy is the universal intermediate

A list, a Series, and an ndarray all become the same thing after `np.asarray()`. That's the point — the function doesn't *care* what you passed in. Once it's an ndarray, everything below is uniform. If you worked with a list internally, you'd need different code paths for each input type.

### 3. Pandas is heavier than needed here

A pandas Series carries an index, a name, dtype metadata, and alignment logic. None of that matters for "sort these 252 numbers and pick the 13th worst." `np.percentile` on a raw ndarray is the lightest possible path.

The rule of thumb: **pandas for data wrangling (download, clean, join, label), NumPy for pure math.** This function sits at the pure-math layer — it should never know about dates, tickers, or DataFrames. That's the architecture separation the project plan calls for.