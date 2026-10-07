# Session 3: Rolling VaR implementation

**Date:** 2026-07-12
**Topic:** rolling_var() + breach_summary() + window cliff tests
**Turn:** 005

## User request

Implement rolling VaR and breach monitoring.

## Work and response

### `rolling_var()` — `src/rolling.py`

```python
rolling_var(returns, window=252, confidence=0.95) -> pd.DataFrame
```

For each day t after the warm-up window, computes VaR using `returns[t-window : t]` (exclusive upper bound — no look-ahead). Returns a DataFrame with columns `VaR`, `NextReturn`, `Breach`, indexed by Date.

Design decisions:
- Python loop (not `.rolling().apply()`) — identical performance, more debuggable. The loop body calls `historical_var()` which uses vectorised `np.quantile()` internally.
- Returns a `pd.DataFrame` with DatetimeIndex — `.plot()`, `.describe()`, `.loc["2020-03"]` all work directly.
- `Breach` column is `-NextReturn > VaR` — actual loss exceeds forecast.

### `breach_summary()` — `src/rolling.py`

```python
breach_summary(df, confidence=0.95) -> dict
```

Pure reporting on the rolling_var output. Returns `{total_observations, breaches, breach_rate, expected_rate}`.

### Tests — 11/11 pass

| Test | What it verifies |
|------|-----------------|
| `test_first_estimate_after_window` | No VaR estimate before day `window` |
| `test_output_length` | `n - window` rows for `n` returns |
| `test_insufficient_data_raises` | Rejects when `len(returns) < window + 1` |
| `test_no_lookahead_bias` | Day 100's VaR uses days 50-99 (excludes the -10% at index 100) |
| `test_loss_enters_window` | -10% at index 100 enters 50-day window at day 101 → VaR > 0 |
| `test_loss_exits_window` | -10% exits at day 151 → VaR drops back to 0 |
| `test_no_breaches_on_flat_returns` | Zero returns → zero VaR → zero breaches |
| `test_breach_detected` | -10% loss against zero VaR → flagged as breach |
| `test_breach_columns_match` | `Breach` column matches manual `-NextReturn > VaR` |
| `test_all_zero_returns` (summary) | breach_count = 0, expected_rate = 0.05 |
| `test_expected_rate_reflects_confidence` | 99% → expected_rate = 0.01 |

### Windows cliff tests use 99% confidence

With 49 zeros + 1 loss of -10% in a 50-element window, the 5th percentile (95% confidence) still falls in the zero region. The 1st percentile (99% confidence) reaches the -10% day. The test uses 99% so the single loss visibly affects VaR. This also tests that `rolling_var` correctly passes confidence through to `historical_var`.

### SPY verification

2018-01-01 → 2026-07-13: 2,141 returns, 1,889 rolling estimates.

| Metric | Value |
|--------|-------|
| First VaR (2019-01-04) | 2.14% |
| Last VaR (2026-07-13) | 1.41% |
| Mean VaR | 1.87% |
| Breaches | 90 / 1,889 |
| Breach rate | 4.76% |
| Expected rate | 5.00% |

Calibration is spot on — the model produces roughly the expected number of breaches over the full period.

### Architecture now

```
download_close_prices → prepare_returns → historical_var
                                         ↓
                                    rolling_var → breach_summary
```

## Files and verification

- `src/rolling.py` — rolling_var + breach_summary (104 lines)
- `tests/test_rolling.py` — 11 tests, all pass
- Full suite: 31/31

## Next step

Notebook: plot rolling VaR, compare windows, annotate market episodes, investigate breach clustering.