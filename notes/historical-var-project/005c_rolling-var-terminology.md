# Rolling VaR — formal terminology

**Date:** 2026-07-14
**Topic:** What rolling VaR does vs a static point-in-time VaR
**Turn:** 005c

## User request

So a rolling VaR takes a static result and makes it dynamic over time in a way? What is the formal way of saying this?

## Work and response

Yes, exactly. The formal terms:

### Static → Point-in-time / unconditional VaR

```python
historical_var(all_returns, confidence=0.95)  # one number
```

This is an **unconditional** estimate — it treats the entire return history as a single distribution and produces one number. It's unconditional because it doesn't condition on *when* the returns happened. A 2018 return and a 2024 return are treated identically.

### Dynamic → Time-varying / conditional VaR

```python
rolling_var(returns, window=252, confidence=0.95)  # one number per day
```

This is a **time-varying** or **rolling-window** VaR. Each day's estimate is conditioned on the specific 252-day window ending at that point. It answers: "given what the market looked like *recently*, what's the risk today?"

The formal term is **rolling estimation** or **recursive out-of-sample estimation**. You re-estimate the model at each point in time using only data available up to that point. The output is a **VaR process** — a time series of risk estimates, not a single number.

### The key distinction

| | Unconditional VaR | Rolling VaR |
|---|---|---|
| Data used | All returns | Recent window only |
| Output | One number | One time series |
| Assumption | Distribution is stationary | Distribution may change |
| Answers | "What was the risk on average?" | "What was the risk at each point in time?" |
| Regime change | Invisible | Visible as VaR drifts up/down |

The rolling nature is what makes the window-cliff visible and the regime-change lag measurable. The unconditional VaR would average across calm and crisis periods, producing a single number that's wrong in both regimes. The rolling VaR adapts — slowly, but it adapts.