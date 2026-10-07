# Canonical design and implementation plan: rolling portfolio volatility chart

## 1. Purpose

Extend `src/notebooks/001-risk-attribution.ipynb` with a portfolio-risk section that introduces the concept of **change over time** while preserving the existing asset-decomposition section.

The existing notebook answers:

> **Where does the portfolio’s structural volatility come from at a point in time?**

The extension adds:

> **How has the volatility of the current portfolio’s daily returns evolved over the last year?**

This is a narrow extension. It does not attempt to explain why volatility changed, identify a volatility regime, or recommend a rebalance.

The notebook will contain two distinct analytical components:

1. **Portfolio risk** — current portfolio volatility and its rolling daily history;
2. **Asset decomposition** — the existing point-in-time covariance-based contribution analysis.

They share portfolio and return-source dependencies but have separate engine and rendering responsibilities.

---

## 2. PM decision supported

The chart provides context for the PM deciding whether the current risk state warrants further investigation.

It should help the PM observe whether current portfolio volatility appears to be:

- rising;
- falling;
- broadly stable;
- reversing;
- subject to a recent sharp movement.

The chart provides evidence for the decision:

> **“Has the portfolio’s risk environment changed enough that I should investigate further?”**

It does not answer:

> **“Should I rebalance?”**

That remains a human decision requiring target weights, investment views, constraints, transaction costs, liquidity, and candidate trade analysis.

---

## 3. Canonical measure

At each available trading date, calculate:

> **The rolling standard deviation of daily portfolio returns over the trailing 252 trading observations.**

The portfolio return series is constructed using the current portfolio weights:

```python
portfolio_returns = asset_returns @ weights
```

The rolling volatility series is then:

```python
rolling_portfolio_volatility = portfolio_returns.rolling(
    window=252
).std()
```

The output is **not annualised**.

### Units

The chart displays:

> **Daily volatility (%)**

For example:

```text
0.58%
0.61%
0.74%
```

These are the estimated standard deviations of daily portfolio returns, not annualised forecasts.

---

## 4. Why calculate directly from portfolio returns?

For this chart, the covariance matrix is not required.

The direct calculation is the clearest expression of the question:

```text
asset returns
→ current portfolio weights
→ daily portfolio returns
→ rolling daily standard deviation
→ chart
```

The covariance matrix remains necessary for the existing asset-level attribution:

```text
asset returns
→ covariance matrix
→ portfolio volatility
→ asset-level risk contributions
```

For fixed weights and identical observations, the two portfolio-volatility calculations should reconcile:

```python
direct_volatility = portfolio_returns_window.std(ddof=1)

covariance_volatility = np.sqrt(
    weights @ asset_returns_window.cov().to_numpy() @ weights
)
```

That reconciliation should be a test, not a reason to make the chart calculation depend on the covariance implementation.

---

## 5. Historical weighting convention

V1 uses the **current portfolio weights at every historical date**.

The series therefore means:

> **How would the current allocation’s estimated daily volatility have evolved as the historical return environment changed?**

It does not mean:

> **What was the volatility of the portfolio as actually held through history?**

The latter would require historical weights or transactions.

This boundary should be stated below the chart or in a methodology note.

---

## 6. What “last year” means

For V1, define “last year” as:

> **The latest 252 available daily volatility observations ending at the latest available return date on or before the requested observation date.**

There are two windows involved:

### Estimation window

The trailing 252 daily asset or portfolio returns used to calculate each volatility value.

### Display window

The latest 252 calculated volatility values shown in the chart.

Therefore, producing a full one-year chart requires more than 252 raw returns:

```text
252 returns for the first volatility estimate
+ 251 additional returns for the remaining daily estimates
= 503 returns minimum
```

In practice, the data provider should load enough history to support:

```text
display_window + estimation_window - 1
```

return observations.

This distinction should be explicit in the implementation plan because “252-day rolling volatility over the last year” can otherwise be incorrectly implemented using only 252 total returns, which produces only one valid volatility estimate.

---

## 7. Endpoint and date convention

The requested notebook date remains the caller-supplied observation date.

The calculation should use the latest available return observation on or before that date. This handles dates such as weekends and holidays without silently claiming that a non-trading date was observed.

The structured result should therefore preserve:

- requested observation date — supplied by the notebook;
- resolved latest return date — the final trading date used by the series.

However, following the existing DTO convention, caller-owned context such as the requested date does not need to be stored inside the computed result. The renderer can receive display context explicitly.

The important requirement is that the displayed endpoint is not ambiguous.

---

## 8. Chart design

### Title

```text
Rolling Daily Portfolio Volatility — Last Year
```

### X-axis

```text
Date
```

### Y-axis

```text
Daily volatility (%)
```

### Series

One line representing the daily rolling volatility estimate.

### Visual treatment

- one point per available trading date;
- line chart using Matplotlib;
- latest value visually highlighted;
- no target line;
- no warning threshold;
- no regime shading;
- no red/green interpretation;
- no event annotations in V1.

The latest value may be highlighted with a marker so the PM can identify the current state quickly.

### Supporting values

The chart should be accompanied by a small evidence block:

```text
Latest observation: 0.62%
Previous-month observation: 0.54%
Change since previous month: +0.08 percentage points
```

The comparison uses the latest available volatility observation on or before the same calendar date in the previous month. It should use **percentage points**, not an unqualified percentage change.

---

## 9. Artifact relationship

The notebook should remain a single workflow with two separate analytical outputs:

```text
1. Portfolio risk
   What is the current portfolio volatility, and how has it evolved over the last year?

2. Asset decomposition
   Where does structural portfolio volatility come from at the current observation date?
```

The order should be:

1. parameters and dependencies;
2. portfolio-risk calculation and render;
3. asset-decomposition calculation and render;
4. methodology/boundary notes for the relevant component.

The new portfolio-risk section should not replace or redesign the existing ranked asset-contribution table.

---

# Canonical implementation architecture

## 10. Proposed layers

### Pure calculation

Add a small pure calculation function, for example:

```text
src/portfolio_volatility.py
```

Responsibility:

- accept a portfolio return series;
- calculate rolling standard deviation;
- return the rolling series;
- perform no downloading;
- perform no plotting;
- know nothing about notebooks or portfolios.

Possible contract:

```python
def calculate_rolling_portfolio_volatility(
    portfolio_returns: pd.Series,
    *,
    estimation_window: int,
    display_window: int,
) -> pd.Series:
    ...
```

The function should:

1. calculate the rolling standard deviation using `ddof=1`;
2. remove the initial warm-up values;
3. select the latest `display_window` valid observations;
4. preserve the date index.

The public parameter names should describe the domain concept, not pandas implementation details.

### Portfolio-risk domain result

Add immutable result objects for the portfolio-risk component, for example:

```text
src/domain/portfolio_risk.py
```

```python
@dataclass(frozen=True)
class VolatilityObservation:
    date: str
    volatility: float


@dataclass(frozen=True)
class PortfolioRisk:
    current_volatility: float
    volatility_history: tuple[VolatilityObservation, ...]
```

The result contains the calculated current portfolio-volatility level and rolling history. It contains calculated evidence only.

It should not echo:

- portfolio name;
- requested date;
- estimation window;
- display window.

Those are caller-owned context and can be passed separately to the renderer.

### Portfolio-risk engine

Add a `PortfolioRiskEngine` for the portfolio-level risk component. It owns both the current portfolio-volatility level and the rolling volatility history. Do not put this logic into `AttributionEngine`, which remains responsible for asset-level decomposition.

Possible module:

```text
src/engine/portfolio_risk_engine.py
```

Possible API:

```python
portfolio_risk = portfolio_risk_engine.calculate(
    portfolio_name=PORTFOLIO,
    date=DATE,
    estimation_window=ESTIMATION_WINDOW,
    display_window=DISPLAY_WINDOW,
)
```

The portfolio-risk engine should:

1. resolve the portfolio;
2. load enough daily asset returns;
3. align the asset columns;
4. construct the daily portfolio return series using current weights;
5. calculate the current portfolio-volatility level using the current point-in-time return window;
6. call the pure rolling-volatility calculation;
7. convert the current level and rolling history into the immutable portfolio-risk domain object.

It should not:

- estimate the covariance matrix for the chart or portfolio-level calculation;
- calculate asset-level risk contributions;
- render Markdown;
- create a Matplotlib figure;
- generate prose interpretation;
- emit a rebalance recommendation.

The existing `AttributionEngine` remains the asset-decomposition engine. It continues to calculate the point-in-time covariance-based `Attribution` output and is not expanded to own portfolio-risk history.

### Portfolio-risk renderer

Add a renderer module for the portfolio-risk component:

```text
src/display/portfolio_risk_renderer.py
```

Possible API:

```python
render_portfolio_risk_markdown(
    portfolio_risk,
    *,
    portfolio_name: str,
    requested_date: str,
)

plot_rolling_portfolio_volatility(
    portfolio_risk.volatility_history,
    *,
    portfolio_name: str,
    requested_date: str,
)
```

The portfolio-risk renderer should:

- render the current portfolio-volatility level;
- create the Matplotlib figure;
- format dates;
- format the y-axis as percentages;
- label daily volatility clearly;
- highlight the latest point;
- display the chart;
- avoid interpreting the movement.

The renderer should not repeat the portfolio-risk calculation or render asset decomposition.

### Asset-decomposition renderer

Retain the existing renderer as the separate presentation boundary for asset decomposition:

```text
src/display/attribution_renderer.py
    → current asset-level contribution table

src/display/portfolio_risk_renderer.py
    → current portfolio-risk level
    → rolling portfolio-volatility chart
```

Do not merge the two renderers into one combined renderer. The notebook may display both outputs in sequence, but each renderer should consume only its own domain result.

---

# Proposed notebook structure

The notebook currently contains five cells:

1. parameters;
2. imports and composition root;
3. portfolio-risk calculation and render;
4. asset-decomposition calculation and render;
5. methodology notes.

The extension should remain compact. The lesson-statement cell is not needed for this extension and should be removed. The notebook should begin with the parameters cell.

## Cell 1 — Parameters

Retain:

```python
DATE = "2021-02-21"
PORTFOLIO = "60/40 Multi-Asset"
ESTIMATION_WINDOW = 252
```

Add:

```python
VOLATILITY_DISPLAY_WINDOW = 252
```

The distinction between `ESTIMATION_WINDOW` and `VOLATILITY_DISPLAY_WINDOW` should be visible.

- `ESTIMATION_WINDOW`: returns per rolling volatility estimate;
- `VOLATILITY_DISPLAY_WINDOW`: daily volatility observations shown on the chart.

## Cell 2 — Imports and composition root

Retain the existing portfolio and returns provider wiring.

Add:

- `PortfolioRiskEngine` and its portfolio-risk domain result;
- `portfolio_risk_renderer`;
- Matplotlib, if required by the renderer.

Retain `AttributionEngine` and `attribution_renderer` for asset decomposition. Concrete dependencies should continue to be assembled in the notebook composition root.

## Cell 3 — Portfolio-risk calculation and render

Calculate the portfolio-risk result through `PortfolioRiskEngine`. This result contains both the current portfolio-volatility level and the rolling volatility history.

```python
portfolio_risk = portfolio_risk_engine.calculate(
    portfolio_name=PORTFOLIO,
    date=DATE,
    estimation_window=ESTIMATION_WINDOW,
    display_window=VOLATILITY_DISPLAY_WINDOW,
)
```

Render the current level and rolling chart through `portfolio_risk_renderer`:

```python
display(Markdown(render_portfolio_risk_markdown(
    portfolio_risk,
    portfolio_name=PORTFOLIO,
    requested_date=DATE,
)))

plot_rolling_portfolio_volatility(
    portfolio_risk.volatility_history,
    portfolio_name=PORTFOLIO,
    requested_date=DATE,
)
```

The portfolio-risk component owns both the current-level display and the change-over-time display. Do not obtain the current level from `Attribution` or make the chart renderer recalculate it.

## Cell 4 — Asset-decomposition calculation and render

Leave the existing attribution calculation and render conceptually unchanged:

```python
attribution = engine.attribute(
    portfolio_name=PORTFOLIO,
    date=DATE,
    estimation_window=ESTIMATION_WINDOW,
)

display(Markdown(render_attribution_markdown(
    attribution,
    portfolio_name=PORTFOLIO,
    date=DATE,
    estimation_window=ESTIMATION_WINDOW,
)))
```

`AttributionEngine` and `attribution_renderer` remain responsible for the asset-level covariance-based decomposition only. The current output must remain recognizable and separate from the portfolio-risk output.

## Cell 5 — Methodology notes

Display a short Markdown note:

```markdown
The chart shows the rolling standard deviation of daily portfolio returns.
Each estimate uses the trailing 252 daily returns and the current portfolio
weights. The series is not annualised and does not represent the realised
volatility of historical portfolio holdings.
```

---

# Implementation plan

## Phase 1 — Confirm existing contracts

Before coding:

- inspect the existing portfolio return helper;
- confirm return values are daily decimal returns;
- confirm the existing attribution uses current weights;
- confirm the data provider’s `end` date behavior;
- decide how the engine obtains enough warm-up history;
- preserve the existing attribution behavior.

The chart should use the same asset universe, return provider, current weights, and missing-data convention as attribution.

## Phase 2 — Implement pure calculation

Create the rolling-volatility calculation.

Required behavior:

- accept a dated daily portfolio return series;
- use trailing `estimation_window` observations;
- use sample standard deviation, `ddof=1`, matching pandas default and the covariance calculation;
- return only valid rolling observations;
- keep the date index;
- select the trailing `display_window` results;
- avoid annualisation.

Tests should cover:

- expected rolling values on a small deterministic series;
- correct date alignment;
- warm-up behavior;
- display-window truncation;
- `ddof=1` consistency;
- insufficient data behavior;
- no annualisation.

## Phase 3 — Add domain output

Create immutable result objects.

Tests should confirm:

- observations are preserved in chronological order;
- values are accessible by date;
- the result is immutable;
- no caller-owned context is redundantly stored.

## Phase 4 — Add portfolio-risk engine

Create `PortfolioRiskEngine` that owns the portfolio-level risk component:

- resolves the named portfolio;
- requests sufficient return history;
- constructs portfolio returns with current weights;
- calculates the current portfolio-volatility level;
- calculates the rolling portfolio-volatility history;
- returns one portfolio-risk domain result containing both the current level and the change-over-time evidence.

The engine should request enough history for both windows:

```text
estimation_window + display_window - 1
```

The portfolio-risk engine should not use a covariance matrix for the portfolio-level calculation and should not calculate asset-level risk contributions.

A useful test double can record the requested start/end dates and return deterministic fixture data.

The existing `AttributionEngine` remains separate and continues to calculate only the point-in-time asset decomposition using covariance-based contributions.

## Phase 5 — Add portfolio-risk renderer

Implement `portfolio_risk_renderer` for the portfolio-level current-risk display and rolling-volatility chart. Keep `attribution_renderer` responsible for the asset-decomposition table.

Test or verify:

- current portfolio-volatility level is rendered by the portfolio-risk renderer;
- chart title;
- y-axis label includes `Daily volatility (%)`;
- latest observation is visible;
- dates are plotted in chronological order;
- no annualisation is applied;
- renderer does not calculate volatility itself;
- asset-decomposition rendering remains separate.

The renderer should be a presentation component, not another calculation path.

## Phase 6 — Extend the notebook

Remove the lesson-statement cell. Add the parameter, composition-root wiring, portfolio-risk calculation/render cell, existing asset-decomposition calculation/render cell, and methodology notes.

Do not duplicate either calculation in notebook code. Keep the portfolio-risk and asset-decomposition outputs visibly separate.

The notebook cell should remain orchestration only.

## Phase 7 — Reconciliation

For at least one deterministic fixture:

1. construct portfolio returns directly;
2. calculate rolling standard deviation;
3. calculate rolling covariance-based portfolio volatility;
4. compare the two for the same dates and windows.

They should agree within numerical tolerance.

This verifies that direct calculation is consistent with the existing covariance-based risk calculation without coupling the chart implementation to covariance estimation.

## Phase 8 — Notebook verification

Run:

```bash
python3 -m jupyter nbconvert \
  --to notebook \
  --execute \
  --inplace \
  src/notebooks/001-risk-attribution.ipynb
```

Then verify:

- all cells execute;
- the existing attribution output remains present;
- the volatility chart is produced;
- the chart contains 252 or fewer valid daily observations;
- the last plotted date is the latest available return date on or before `DATE`;
- no annualisation appears in the chart label or methodology;
- the notebook contains no notebook-local rolling-volatility business logic.

---

# Acceptance criteria

The implementation is complete when:

1. The notebook starts with the parameters cell; no lesson-statement cell is required.
2. The notebook contains a separate portfolio-risk output and asset-decomposition output.
3. `PortfolioRiskEngine` owns the current portfolio-volatility level and rolling volatility history.
4. `AttributionEngine` continues to own asset-level covariance-based decomposition only.
5. `portfolio_risk_renderer` renders the portfolio-risk level and chart separately from `attribution_renderer`.
6. The existing attribution output remains unchanged and recognizable.
7. The notebook produces a rolling portfolio-volatility chart.
8. The chart covers the latest year of available daily volatility observations.
9. Each volatility observation uses a trailing 252 daily-return estimation window.
10. Current portfolio weights are applied consistently across the historical series.
11. The volatility is displayed on the daily-return scale.
12. No annualisation is performed.
13. The covariance matrix is not required by the chart calculation.
14. The direct calculation reconciles with the covariance-based portfolio volatility for deterministic fixtures.
15. The chart labels its units as daily volatility.
16. The methodology note explains the current-weight convention.
17. The chart does not contain thresholds, regimes, conclusions, or rebalance recommendations.
18. The notebook executes successfully with `nbconvert`.
19. Portfolio-risk and asset-decomposition engine responsibilities remain separate.
20. Portfolio-risk and asset-decomposition renderer responsibilities remain separate.
## Canonical V1 decision

> **Extend `001-risk-attribution.ipynb` with a portfolio-risk component containing the current portfolio-volatility level and a daily rolling-volatility chart covering the latest 252 volatility observations. Calculate portfolio returns from the current portfolio weights and each rolling point as the trailing 252-observation standard deviation of daily portfolio returns, display the result without annualisation, keep `PortfolioRiskEngine`/`portfolio_risk_renderer` separate from `AttributionEngine`/`attribution_renderer`, and retain covariance estimation for the existing asset-level attribution and reconciliation tests.**
