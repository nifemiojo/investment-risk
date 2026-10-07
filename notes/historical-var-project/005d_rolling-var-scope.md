# rolling_var: backtesting vs forward-looking VaR

**Date:** 2026-07-14
**Topic:** What rolling_var does and doesn't produce
**Turn:** 005d

## User request

So if I'm correct rolling_var does not calculate today's VaR i.e. using the last day in the sample?

## Work and response

Correct — and there are two distinct cases here.

### What `rolling_var` does produce

It produces a VaR estimate for **every day from `window` to the end of the sample**, including the very last day. The last row of the output says:

> "Using the preceding 252 returns, the VaR for the final day in the sample was X%, and the actual return that day was Y%."

So the last day *is* forecasted, and the breach flag for that day *is* computed. There's just no day after it to continue the series.

### What `rolling_var` does NOT do

It doesn't produce a VaR for **today** in the "what's the risk right now" sense. If you download data through yesterday and want "what's the 1-day VaR for tomorrow?" — `rolling_var` can't answer that. Its last row is a *backtest* of yesterday, not a *forecast* of tomorrow.

For a forward-looking VaR estimate, you'd run `historical_var` directly on the most recent window:

```python
# VaR for tomorrow (no actual return to check against yet)
today_var = historical_var(returns.iloc[-252:], confidence=0.95)
```

`rolling_var` is a backtesting tool — it answers "how did the model perform historically?" `historical_var` is the forward-looking tool — it answers "what's the risk right now?"

A comment was added to `src/rolling.py` to make this distinction clear.