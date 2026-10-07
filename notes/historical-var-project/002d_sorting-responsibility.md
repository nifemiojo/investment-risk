# Should the caller sort returns before passing to historical_var?

**Date:** 2026-07-12
**Topic:** Design decision — sorting responsibility
**Turn:** 002d

## User request

So the consumer must pass in the returns already sorted? From a software design perspective should this be a responsibility of historical_var or consumer?

## Work and response

The function doesn't require sorted returns — `np.percentile` sorts internally. So as it stands, the caller can pass returns in any order and it works correctly. The real question is: **should it?**

The answer is no, and here's why.

### Sorting is an implementation detail, not a semantic requirement

What does `historical_var` actually need? A distribution of returns. The time ordering is irrelevant — historical VaR throws away the sequence and only cares about the shape. Sorting is *how* `np.percentile` finds the quantile, not *what* the function needs from the caller.

If you pushed sorting to the caller:

```python
# Bad design: leaks implementation detail
var = historical_var(sorted_returns)  # caller must remember to sort
```

You've created a footgun. Someone passes unsorted data, `np.percentile` sorts it anyway, so no error — but now the caller thinks sorting matters when it doesn't. Or worse, you write your own percentile logic that assumes sorted input and silently produces garbage.

### The design principle

> The function's contract should express what it needs **semantically**, not how it computes the answer.

`historical_var` needs: "a collection of historical returns." Period. Whether it sorts them, builds a histogram, or uses a tree is its own business. That's encapsulation.

### The C# parallel

In C# you wouldn't write:

```csharp
// Leaky: exposes that Percentile() requires sorted input
public static double HistoricalVaR(List<double> sortedReturns, double confidence)
```

You'd write:

```csharp
public static double HistoricalVaR(IEnumerable<double> returns, double confidence)
{
    var sorted = returns.OrderBy(r => r).ToArray();  // sort internally
    // ... percentile logic
}
```

Same principle: the sort is an implementation step, not part of the API contract.