# Session 3 plan: Rolling VaR + model behaviour investigation

**Date:** 2026-07-12
**Topic:** Plan for combining Sessions 3 and 4 — rolling machinery and model analysis
**Turn:** 004

## User request

Plan out the next session, focusing on explaining and understanding the model's behaviour.

## Work and response

### What we build

**`src/rolling.py`** — two functions:

```python
rolling_var(returns, window=252, confidence=0.95) -> pd.DataFrame
    # Columns: Date, VaR, Next-day return, Breach

breach_summary(rolling_df) -> dict
    # Breach count, breach rate, expected rate, simple comparison
```

**Tests** — the four rolling-specific tests from the plan:

| Test | What it verifies |
|------|-----------------|
| First VaR only after window | No estimates before day `window + 1` |
| No look-ahead bias | Day t's VaR uses only returns through t-1 |
| Synthetic loss enters window | A -10% day becomes part of VaR calculation exactly when expected |
| Synthetic loss exits window | A -10% day drops out of VaR calculation exactly when expected |

The last two make the "window cliff" visible and testable.

**Notebook** — `notebooks/historical_var_analysis.ipynb`:

1. Pull SPY, compute rolling VaR at 95% and 99%
2. Show the table (first 10 rows, last 10 rows)
3. **Plot 1:** Rolling VaR + realised losses + breach scatter points
4. **Plot 2:** Three windows overlaid (60d, 252d, 504d) with COVID and 2022 annotations
5. **Plot 3:** Breach clustering — are breaches randomly scattered or bunched?
6. Answer the five investigation questions from the plan

### What we learn

The central insight is the bias-variance trade-off made visible. We'll see:

- The 60-day line jumping around while the 504-day line barely moves
- COVID: 252-day VaR staying low through late Feb 2020 while the market is already crashing — the regime change lag in action
- The window cliff: the March 2020 crash days entering and exiting the 252-day window, creating visible bumps in the VaR series
- Breach clustering: 5% breach rate holds on average, but all breaches happen in a few concentrated periods

### Architecture

```
rolling_var(returns, window, confidence)
    ├── calls historical_var() for each rolling window
    ├── records next-day return and breach flag
    └── returns DataFrame ready for plotting

breach_summary(df)
    └── pure reporting: counts, rates, no new calculations
```

`rolling_var` is the only function that depends on `historical_var`. `breach_summary` is a pure reporting function on the DataFrame output.

This is the session that turns the calculator into a real risk tool.