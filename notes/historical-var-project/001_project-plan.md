# Historical VaR Calculator — Project Plan

**Date:** 2026-07-11  
**Status:** Ready to implement  
**Project:** First practical project in the VaR toolkit

## The purpose

Build a single-asset historical VaR toolkit that answers:

> Given a position, a historical window, and a confidence level, what loss would we expect not to exceed on most days—and how reliable has that estimate been?

For example:

> A £1 million SPY position, using the previous 252 trading days and 95% confidence, has a one-day historical VaR of £31,800.

Interpretation:

> On approximately 95% of comparable days, the loss should be no greater than £31,800. This is not a guarantee; the remaining 5% contains larger losses.

The project should produce four outputs:

1. A clean historical VaR function.
2. A rolling VaR time series.
3. A chart showing VaR alongside realised losses.
4. A short analysis of when the model works and when it fails.

The fourth output is what turns this from a basic percentile calculator into useful risk analysis.

## Why it matters for the wider direction

This project connects directly to current Spreadex work and the longer-term goal of working in systematic multi-asset investing, portfolio analytics, and risk infrastructure.

| Goal | What this project demonstrates |
|---|---|
| Spreadex risk work | Market-risk measurement and monitoring |
| Risk analytics engineering | Separation of data, calculation, validation, and reporting |
| Systematic investing | Out-of-sample measurement and model discipline |
| Portfolio construction | A foundation for portfolio-level VaR |
| Macro awareness | Visibility into volatility regimes and regime-change lag |
| Career portability | A public, reproducible risk-system artifact |

The useful career narrative is not:

> I built a VaR calculator.

It is:

> I implemented and validated a historical VaR model, examined how window choice affected responsiveness during changing volatility regimes, and built monitoring outputs to identify when the model became stale.

## Version 1 scope

### Core MVP

- One asset initially: SPY.
- Daily adjusted prices.
- Simple percentage returns.
- One-day VaR.
- 252-day historical window.
- 95% and 99% confidence levels.
- Linear percentile interpolation.
- Positive loss convention.
- Position value in currency.
- Rolling VaR series.
- Tests using manually calculated examples.

### Useful extensions

Add these only after the core works:

- 60-day and 504-day windows.
- 95% versus 99% comparison.
- Nearest-rank versus linear interpolation.
- Volatility-regime annotations.
- Simple breach counting.
- A second asset such as GLD or BND.

### Leave out initially

- Portfolio VaR.
- Monte Carlo.
- GARCH.
- A dashboard application.
- Production database infrastructure.
- Multiple data vendors.
- Complex derivative exposures.
- Expected Shortfall.
- Deployment.

These can follow once the single-asset calculation and interpretation are correct.

## Key design decision: positive loss convention

The underlying historical return quantile is negative. Operational risk systems usually report VaR as a positive loss amount.

For returns (r) and confidence (c):

$$
q = \operatorname{Quantile}(r, 1-c)
$$

Define percentage VaR as:

$$
\operatorname{VaR}_{c} = -q
$$

If the 5th percentile return is (-3.2\%), then:

$$
\operatorname{VaR}_{95\%} = 3.2\%
$$

For a position worth (V):

$$
\operatorname{VaR}_{£} = V \times \operatorname{VaR}_{\%}
$$

This avoids reporting a loss as a negative VaR amount while preserving the correct underlying return calculation.

## Architecture

Keep the project in four layers:

```text
Price data
    ↓
Return preparation
    ↓
Historical VaR calculation
    ↓
Rolling monitoring and validation
```

### 1. Data preparation

Input:

- Ticker.
- Start and end dates.
- Price field.

Output:

- Clean, sorted daily price series.
- Daily return series.
- No duplicate dates.
- No missing prices.
- Documented treatment of non-trading days.

Use adjusted prices where available so dividends and corporate actions do not distort long-run equity returns.

Download more history than the VaR window. To calculate a 252-day rolling VaR across several years, several years of data are required—not merely 252 days.

### 2. Pure VaR calculation

The central function should accept returns, not tickers or downloaded data:

```text
historical_var(
    returns,
    confidence=0.95,
    method="linear",
    position_value=None
)
```

The VaR function should not know where the data came from. This allows the same calculation to be reused with market returns, portfolio returns, Spreadex P&L returns, or simulated returns.

### 3. Rolling VaR

For every date (t), calculate VaR using the preceding (W) observations:

$$
\operatorname{VaR}_{t}
=
-\operatorname{Quantile}
\left(
r_{t-W}, \ldots, r_{t-1};
1-c
\right)
$$

The current day’s return must be excluded from its own forecast. The model should estimate risk before observing the next day’s outcome; otherwise the evaluation contains look-ahead bias.

### 4. Monitoring and validation

For each day after the initial window, record:

- VaR estimate.
- Actual next-day return.
- Actual loss.
- Whether a breach occurred.

A breach occurs when:

$$
\text{Actual loss}_{t+1} > \operatorname{VaR}_{t}
$$

At 95% confidence, approximately 5% of observations should breach over a sufficiently large sample. This is a calibration reference, not a requirement that every short sample contain exactly 5% breaches.

## Implementation sequence

### Session 1: Smallest correct calculator

Start with a hand-created sample:

```text
[-5%, -3%, -2%, -1%, 0%, 1%, 2%, 3%, 4%, 5%]
```

Calculate the 95% VaR manually, then compare it with the percentile calculation. This forces clarity about:

- Which tail is being used.
- Why confidence becomes (1-c).
- What interpolation does.
- Why the result is reported as a positive loss.

Then run the same function on SPY.

### Session 2: Data handling

Build a reusable data-preparation function that:

- Downloads adjusted prices.
- Sorts by date.
- Removes missing observations.
- Computes returns.
- Reports the date range and number of observations.

Add checks for:

- At least `window` observations.
- Confidence between 0 and 1.
- Numeric returns.
- No remaining missing values.

### Session 3: Rolling VaR

Produce a table containing:

| Date | VaR 95% | VaR 99% | Next-day return | Breach |
|---|---:|---:|---:|---|
| 2024-01-03 | 2.1% | 3.4% | -0.8% | No |
| 2024-01-04 | 2.1% | 3.4% | -2.7% | Yes |

Plot:

- Rolling VaR.
- Absolute realised losses.
- Breach points.
- Major market episodes.

The chart should explain the model’s behaviour rather than merely decorate the notebook.

### Session 4: First investigation

Compare 60-day, 252-day, and 504-day VaR estimates. Ask:

1. Which window reacts fastest after a volatility spike?
2. Which window is most stable?
3. When does the short window generate noisy signals?
4. How long does the 252-day window take to reflect a crisis?
5. Does the long window remain elevated after the crisis has passed?

Do not assume one window is best. Investigate the trade-off:

| Window | Likely behaviour |
|---|---|
| 60 days | Fast, but noisy and sample-sensitive |
| 252 days | More stable, but slow during regime changes |
| 504 days | Very stable, but potentially stale |

A potentially valuable conclusion is:

> The 60-day estimator responded more quickly to rising volatility but produced noisier estimates. The 252-day estimator was more stable but understated risk during the early part of the volatility shock. This suggests that a monitoring system should expose multiple windows rather than rely on a single VaR number.

## Testing plan

### Calculation tests

- Known percentile on a small hand-worked sample.
- Confidence-level validation.
- Empty-input rejection.
- Missing-value handling.
- Insufficient-window rejection.
- Positive loss sign convention.
- Position-value scaling.

### Data tests

- Dates are sorted.
- Returns exclude the first missing percentage change.
- No duplicate dates.
- Adjusted price field is used where appropriate.
- Asset and return lengths are consistent.

### Rolling tests

- The first VaR estimate appears only after the required window.
- The current day’s return is not included in its own forecast.
- A synthetic large loss enters the window when expected.
- A synthetic large loss exits the window when expected.

The final two tests make the “window cliff” visible and reproducible.

## Final artifact structure

```text
historical-var/
├── README.md
├── notebooks/
│   └── historical_var_analysis.ipynb
├── src/
│   └── historical_var.py
├── tests/
│   └── test_historical_var.py
├── data/
│   └── README.md
└── figures/
    ├── rolling_var_windows.png
    └── var_breaches.png
```

The README should explain:

- The problem.
- The historical VaR method.
- The data source.
- The sign convention.
- The window and confidence choices.
- The main result.
- The model’s limitations.
- How to reproduce the analysis.

The notebook should be exploratory and readable. The reusable function should live separately from the notebook.

## Definition of done

Version 1 is complete when you can:

- Explain historical VaR in one minute.
- Calculate it by hand for a small sample.
- Explain why the lower return percentile represents loss risk.
- Explain the interpolation convention.
- Produce a correct rolling, out-of-sample VaR series.
- Identify breaches without look-ahead bias.
- Explain the effect of 60-, 252-, and 504-day windows.
- State at least three limitations.
- Describe what you would build next for a real portfolio.

The project is not finished merely because the code runs.

## Recommended sequence after version 1

```text
Correct single-day calculator
    ↓
Rolling out-of-sample VaR
    ↓
Window and regime analysis
    ↓
Simple breach monitoring
    ↓
Portfolio VaR
    ↓
Comparison with parametric and Monte Carlo methods
```

The immediate next action is to create the smallest hand-worked example, verify the percentile and sign convention, and then run the same calculation on several years of SPY adjusted-price data.
