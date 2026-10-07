# Session 1: Smallest correct calculator

**Date:** 2026-07-12
**Topic:** Implement and verify the core historical VaR function
**Turn:** 002

## User request

Kick off the historical VaR project. Guided implementation — walk through together, not just write all the code.

## Work and response

### Step 1: Hand-worked example

Sample: `[-5%, -3%, -2%, -1%, 0%, 1%, 2%, 3%, 4%, 5%]`

95% VaR under linear interpolation:

$$i = 0.05 \times (10 - 1) = 0.45$$

$$\text{Quantile}_{0.05} = -5\% + 0.45 \times (-3\% - (-5\%)) = -4.1\%$$

$$\text{VaR}_{95\%} = -(-4.1\%) = 4.1\%$$

Key moves:
- $1-c$: 95% confidence → 5th percentile (left tail)
- Interpolation: $i = P \times (n-1)$, interpolate between adjacent values
- Positive loss convention: negate the negative quantile

### Step 2: Core function (`src/historical_var.py`)

```python
historical_var(returns, confidence=0.95, method="linear", position_value=None)
```

- Pure calculation: accepts returns, not tickers
- Uses `numpy.percentile` with `method="linear"` (production standard)
- `method="lower"` available for nearest-rank approximation
- Input validation: empty, NaN, confidence bounds
- Position scaling: `position_value` parameter for currency VaR

### Step 3: Tests (17/17 pass)

Calculation tests: hand-worked sample (95% linear = 4.1%, 95% lower = 5.0%, 99% linear = 4.82%), confidence ordering, median at 50%, positive sign convention, position scaling.

Validation tests: empty input, NaN, confidence bounds (0, 1, negative, above 1).

Edge cases: single return, two returns.

### Step 4: SPY results

SPY daily returns, 2020-01-02 to 2026-07-10 (1,637 observations):

| Window | 95% VaR | 99% VaR |
|--------|---------|---------|
| 60-day | 1.26% | 1.99% |
| 252-day | 1.41% | 1.91% |
| 504-day | 1.59% | 2.70% |

£1M SPY, 252d, 95% → **£14,126**

Interesting observation: the 60-day 95% VaR is *lower* than the 252-day — the recent 60 days have been calmer than the full year. But at 99%, the 60-day VaR catches up (1.99% vs 1.91%) — the short window's limited sample makes the 1st percentile land on a bigger day. The 504-day 99% VaR is much higher (2.70%) because a 2-year window captures the 2025 volatility.

## Decisions and assumptions

- Using `numpy.percentile(method="linear")` — matches the project plan's linear interpolation convention
- `method="lower"` approximates nearest-rank but not exactly (numpy's "lower" uses $\lfloor i \rfloor$, not $\lceil P \times n \rceil$)
- Function signature follows the plan exactly: returns-first, no knowledge of data source

## Files and verification

- `src/historical_var.py` — core function (78 lines)
- `tests/test_historical_var.py` — 17 tests, all pass
- `README.md` — project overview
- `data/README.md` — data directory note

## Next step

Session 2: Data preparation function — download adjusted prices, sort, clean, compute returns, with validation checks.