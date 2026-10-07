# Session 2: Data handling

**Date:** 2026-07-12
**Topic:** Build the data preparation layer — download, clean, validate, compute returns
**Turn:** 003

## User request

Start Session 2: data handling. Build a reusable data-preparation function that downloads adjusted prices, sorts, cleans, computes returns, and validates.

## Work and response

### Design decision: separate download from cleaning

Same layering principle as `historical_var` — the function that cleans data shouldn't know where it came from. Split into two:

- `download_prices(ticker, start, end)` — the only function that knows about yfinance. Swappable if data vendor changes.
- `prepare_returns(prices)` — pure data pipeline. Works with any price DataFrame or Series. Can be tested without network.

### `download_prices` — `src/data.py`

Downloads from Yahoo Finance via yfinance. Handles the MultiIndex column issue (yfinance >= 0.2.x). Returns a plain DataFrame with Close, High, Low, Open, Volume. Raises `ValueError` if no data returned.

### `prepare_returns` — `src/data.py`

Cleaning pipeline:
1. Extract the right column (`price_col`, defaults to "Close")
2. Coerce to numeric (`pd.to_numeric` — strings become NaN)
3. Sort by date
4. Remove duplicate dates (keep last)
5. Drop NaN prices
6. Compute returns via `pct_change()`, drop the first NaN
7. Report: date range, observation count

Validates:
- Price series is not empty after cleaning
- At least 2 observations (need returns)
- Column name exists (if DataFrame input)

Prints informational messages about cleaning actions (duplicates removed, NaN dropped) so the caller knows what happened.

### Tests — 34/34 pass (12 data unit + 3 data integration + 19 VaR)

Unit tests (no network): Series input, DataFrame input, unsorted dates, NaN handling, duplicate dates, empty/NaN/single-price rejection, wrong column name, non-numeric coercion.

Integration tests (network): SPY download produces valid returns, SPY feeds into `historical_var` correctly, bad ticker raises.

### Full chain verification

```
download_prices("SPY", 2020-01-01 → 2026-07-11)
  → 1,638 price observations
prepare_returns()
  → 1,637 daily returns (2020-01-03 → 2026-07-10)
  → Mean: 0.065%  Std: 1.278%  Min: -10.94%  Max: 10.50%
historical_var()
  → 60d: 95% VaR = 1.26%, 99% VaR = 1.99%, £1M = £12,590
  → 252d: 95% VaR = 1.41%, 99% VaR = 1.91%, £1M = £14,126
  → 504d: 95% VaR = 1.59%, 99% VaR = 2.70%, £1M = £15,932
```

### Architecture now

```
download_prices  (yfinance → prices)
    ↓
prepare_returns  (prices → clean returns)
    ↓
historical_var   (returns → VaR)
    ↓
rolling_var      (next session)
```

## Files and verification

- `src/data.py` — download_prices + prepare_returns (121 lines)
- `tests/test_data.py` — 15 tests (12 unit + 3 integration)
- `pyproject.toml` — pytest config with integration marker
- Full suite: 34 passed in 2.77s

## Next step

Session 3: Rolling VaR — produce the table with dates, VaR estimates, next-day returns, and breach flags.