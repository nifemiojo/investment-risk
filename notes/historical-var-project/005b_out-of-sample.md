# What "out-of-sample" means for rolling VaR

**Date:** 2026-07-14
**Topic:** Out-of-sample forecasting and why in-sample is cheating
**Turn:** 005b

## User request

Why is it "out-of-sample" — what does this mean?

## Work and response

"Out-of-sample" means the data used to make a forecast is **not** in the data used to evaluate it.

### The wrong way: in-sample (look-ahead bias)

```python
# Hypothetical: what you must NOT do
all_returns = returns[-252:]  # includes today
var = historical_var(all_returns)
today_return = all_returns[-1]
breach = -today_return > var
```

This is worthless. Today's return is in the 252-day window used to compute VaR. If today is a -10% crash, the VaR will be inflated because that -10% is part of the percentile calculation. The model claims it "predicted" the crash because it peeked at the answer.

### The right way: out-of-sample (what rolling_var does)

```python
past_returns = returns[t - 252 : t]  # up to yesterday, exclusive
var = historical_var(past_returns)
today_return = returns[t]             # NOT in the window
breach = -today_return > var
```

The VaR for Tuesday uses Monday and earlier. Tuesday's return is unknown at the time of the forecast. The breach check is a genuine out-of-sample test — "did the model predict this before it happened?"

### Why it matters

If you compute VaR in-sample, the breach rate will always look good — the model "predicted" what it already contained. The 2008 financial crisis wouldn't breach a 2007-2008 in-sample VaR because the crash days are in the window inflating the VaR.

Out-of-sample testing is the only honest way to evaluate a forecasting model. It answers: "on days when the model didn't know what was coming, how often was it wrong?"