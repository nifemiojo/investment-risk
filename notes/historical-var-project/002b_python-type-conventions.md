# Python type conventions: array-like and np.asarray

**Date:** 2026-07-12
**Topic:** Clarifying the "array-like" pattern and why historical_var casts immediately
**Turn:** 002b

## User request

Coming from C#, wanted to understand: why does `returns` have no type annotation, what does "array-like" mean, and why the immediate `np.asarray()` cast?

## Work and response

### 1. "Array-like" — what does that mean?

It's a NumPy convention, not a Python language feature. "Array-like" means: **anything that `np.asarray()` can convert to a numpy array**. That includes:

```python
# All of these work:
np.asarray([1, 2, 3])              # list
np.asarray((1, 2, 3))              # tuple
np.asarray(np.array([1, 2, 3]))    # already an ndarray
np.asarray(pd.Series([1, 2, 3]))   # pandas Series
np.asarray([1, 2, 3], dtype=float) # with type coercion
```

Compare to C# where you'd write:

```csharp
// C#: explicit overloads or an interface constraint
double HistoricalVaR(double[] returns, ...) { }
double HistoricalVaR(List<double> returns, ...) { }
// or
double HistoricalVaR(IEnumerable<double> returns, ...) { }
```

In Python you *could* annotate it as `np.ndarray`, but that forces every caller to convert their data first. If someone has a list or a pandas Series, they'd have to call `np.array(my_list)` before calling your function. The "array-like" convention says: *the function does that for you*. The caller passes whatever they have; `np.asarray()` at the top normalises it.

### 2. Why not specify a type annotation?

Because the set of acceptable types is broad and awkward to express:

```python
from typing import Union, List, Tuple
import numpy as np
import pandas as pd

# This is ugly and incomplete:
def historical_var(
    returns: Union[List[float], Tuple[float, ...], np.ndarray, pd.Series],
    ...
)
```

NumPy itself doesn't try to type-annotate this. The convention in scientific Python is: say "array-like" in the docstring, and let `np.asarray()` do the validation at runtime. If someone passes a string or a dict, `np.asarray()` raises a clear error. The type checker can't express the constraint well; the runtime enforces it perfectly.

### 3. Why the immediate `np.asarray()` cast?

This is the pattern:

```python
def historical_var(returns, ...):
    arr = np.asarray(returns, dtype=float)  # ← normalisation gateway
    # Everything below this line assumes arr is a float ndarray
```

Three reasons:

| Reason | What it gives you |
|--------|-------------------|
| **Uniform interface** | List, tuple, Series, ndarray — all become the same thing at line 1 |
| **Guaranteed dtype** | `dtype=float` ensures integers become floats; no mixed-type surprises |
| **Immutable input** | `asarray` doesn't copy if the input is already an ndarray of float — it's a zero-cost no-op in that case, unlike `np.array()` which always copies |

That last point is subtle but important: `np.asarray()` is the "convert only if needed" function. `np.array()` always allocates new memory. In the hot path (someone passes a numpy array of floats), `asarray` is free.

The C# mental-model translation: you're used to method signatures being the contract. In Python data-science code, the docstring + the `asarray` gatekeeper at line 1 together form the contract. The type annotation is secondary — it's documentation, not enforcement. The runtime cast is the enforcement.