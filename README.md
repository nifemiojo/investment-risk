# Investment Risk

A Python portfolio-risk diagnostic and decision-support system for multi-asset investment portfolios.

The project focuses on a practical portfolio-management question:

> **What risk is the portfolio taking, where does it come from, what has changed, and what would happen if the allocation changed?**

It combines historical Value-at-Risk research with covariance-based volatility attribution, risk-budget drift monitoring, and hypothetical trade-impact analysis. The emphasis is not on producing a single risk number or an automated optimiser; it is on connecting risk measurement to an allocation decision while keeping the evidence and limitations explicit.

## What this project demonstrates

- Translating an investment-management workflow into a focused software vertical slice.
- Modelling portfolios, mandates, risk contributions, drift observations, candidate trades, and impact results as domain concepts.
- Implementing quantitative risk calculations with NumPy and pandas.
- Separating calculations, domain models, decision logic, data providers, and presentation.
- Using tests to validate mathematical properties and decision-support behaviour.
- Investigating model behaviour through reproducible notebooks rather than treating model output as unquestionable.

## Implemented capabilities

### Portfolio risk and attribution

- Calculates covariance-based portfolio volatility from historical asset returns.
- Decomposes portfolio volatility into signed asset-level component contributions.
- Ranks contributions and reports cumulative contribution to reveal concentration.
- Preserves negative contributions, making diversification effects visible rather than treating them as errors.
- Tests contribution reconciliation, negative contributors, zero-weight holdings, and input validation.

The attribution is a structural answer to **where portfolio risk lives**. It is distinct from a single-day historical VaR loss decomposition: the former describes persistent covariance relationships, while the latter explains one realised scenario.

### Risk-budget drift monitoring

- Compares current asset risk contributions with target risk budgets from a mandate.
- Calculates signed and absolute drift for each asset.
- Applies configurable tolerance bands to identify assets requiring review.
- Produces review-oriented output without claiming that a tolerance breach automatically determines a trade.

### Hypothetical trade impact

- Selects a simple candidate transfer from the largest positive drift to the most negative drift among assets outside the configured tolerance band.
- Recalculates the proposed portfolio’s volatility, asset risk contributions, risk-budget drift, and tolerance-band breaches.
- Compares current and proposed states at both portfolio and asset level.
- Keeps the distinction between **reducing total volatility** and **improving risk-budget alignment** explicit.

The candidate trade is deliberately limited: it is a hypothetical equal-and-opposite weight transfer, not an optimiser, an executable order, or an investment recommendation. Transaction costs, liquidity, constraints, and execution are outside the current scope.

### Historical VaR research

- Historical VaR with configurable confidence levels and positive-loss reporting.
- Rolling out-of-sample VaR forecasts and breach monitoring.
- Exponentially weighted VaR using decay weighting.
- Research into volatility scaling and combined model approaches.
- Notebook-based investigation of forecast responsiveness and model behaviour.

The VaR work is research-oriented. It is used to examine estimation choices and forecast behaviour, not to imply that one backtest establishes a production model.

### Diversification research

- Examines changing correlations across assets and through time.
- Investigates the diversification benefit of the multi-asset portfolio.
- Studies the effect of removing individual assets from the portfolio.
- Uses portfolio-level evidence to distinguish standalone asset volatility from interaction and diversification effects.

## Worked example: from risk diagnosis to candidate trade

The examples below are produced by the project’s notebooks using a four-asset multi-asset portfolio: SPY, EFA, IEF, and GLD. The portfolio is labelled `60/40 Multi-Asset`; the risk-budget targets are 45% SPY, 20% EFA, 20% IEF, and 15% GLD. Results shown are illustrative historical observations from the notebook run, not live market data.

### 1. Current portfolio risk

The calculated current daily portfolio volatility is **1.22%**. Covariance-based attribution gives the following ranked view:

| Asset | Portfolio weight | Risk contribution | Cumulative contribution |
|---|---:|---:|---:|
| SPY | 40% | 67% | 67% |
| EFA | 20% | 31% | 98% |
| GLD | 15% | 5% | 103% |
| IEF | 25% | -3% | 100% |

The cumulative total temporarily exceeds 100% because IEF has a negative contribution and offsets risk elsewhere. That is a meaningful diversification result, not a calculation error. The table shows that most current structural risk is concentrated in SPY and EFA despite the portfolio weights being distributed across four assets.

### 2. Risk-budget drift

Comparing current risk contributions with the mandate gives:

| Asset | Target risk contribution | Current risk contribution | Signed drift | Absolute drift |
|---|---:|---:|---:|---:|
| IEF | 20% | -3% | -23.35 pp | 23.35 pp |
| SPY | 45% | 67% | +22.27 pp | 22.27 pp |
| EFA | 20% | 31% | +10.65 pp | 10.65 pp |
| GLD | 15% | 5% | -9.57 pp | 9.57 pp |

With a tolerance band of **±5 percentage points**, all four assets are outside tolerance. The system therefore produces a rebalance review, with directional review suggestions, but does not decide trade size or whether the portfolio should actually be rebalanced.

### 3. Candidate allocation change

The simple candidate-generation rule identifies the largest positive drift and most negative drift among assets outside the tolerance band:

> **Sell 0.50 percentage points of SPY and buy 0.50 percentage points of IEF.**

The impact engine then evaluates the proposed weights against the current state:

| Measure | Current | Proposed | Change |
|---|---:|---:|---:|
| Portfolio volatility | 0.0122 | 0.0121 | -0.0001 |
| Maximum absolute risk-budget drift | 23.35 pp | 23.42 pp | +0.07 pp |
| Total absolute risk-budget drift | 65.84 pp | 65.82 pp | -0.02 pp |
| Assets outside tolerance | 4 | 4 | 0 |

This is the key decision-support distinction in the project: the candidate **slightly reduces portfolio volatility** and **slightly reduces total absolute drift**, but it does not improve every measure. Maximum drift increases marginally and the number of tolerance breaches is unchanged. The system therefore provides evidence for a PM’s decision rather than presenting a lower-volatility trade as automatically better.

The full worked example is in [`src/notebooks/003-candidate-trade-impact.ipynb`](src/notebooks/003-candidate-trade-impact.ipynb). It uses Yahoo Finance historical data, an observation date of `2021-02-21`, a 252-observation estimation window, a ±5 percentage-point tolerance, and a 0.50 percentage-point candidate transfer. The displayed figures are therefore historical, data-provider-dependent notebook results rather than live values; rerunning the notebook requires network access and may produce small changes if the provider revises its history.

Related notebooks cover attribution, drift monitoring, risk snapshots, and the VaR research programme. Risk-change behaviour is covered by the corresponding engine and tests.

## Architecture

The code is organised around explicit boundaries:

```text
Data providers → Portfolio and mandate models → Risk engines → Decision logic → Renderers
```

Key areas include:

- `src/domain/` — portfolio, mandate, attribution, drift, candidate trade, and impact models.
- `src/engine/` — portfolio risk, attribution, drift, rebalance-trigger, snapshot, and candidate-impact engines.
- `src/infrastructure/` — in-memory portfolios, CSV/Yahoo Finance return providers, and fixtures.
- `src/display/` — Markdown renderers for risk and decision-support artifacts.
- `src/historical_var.py`, `src/rolling.py`, and `src/decay.py` — VaR and backtesting calculations.
- `tests/` — unit tests for calculations, domain behaviour, rendering contracts, and edge cases.
- `src/notebooks/` — research and worked workflow artifacts.

The calculation layer is kept separate from presentation so the same engines can support notebooks, rendered Markdown artifacts, and future interfaces.

## Research and design documents

| Material | Focus |
|---|---|
| [`src/notebooks/001-risk-attribution.ipynb`](src/notebooks/001-risk-attribution.ipynb) | Portfolio volatility, risk attribution, and contribution change |
| [`src/notebooks/002-risk-drift.ipynb`](src/notebooks/002-risk-drift.ipynb) | Risk-budget drift and tolerance-band review |
| [`src/notebooks/003-candidate-trade-impact.ipynb`](src/notebooks/003-candidate-trade-impact.ipynb) | Before/after assessment of a hypothetical allocation change |
| [`notebooks/02_rolling_var_backtest.ipynb`](notebooks/02_rolling_var_backtest.ipynb) | Rolling historical VaR forecasts and breaches |
| [`notebooks/05_decay_weighting.ipynb`](notebooks/05_decay_weighting.ipynb) | Exponentially weighted VaR research |
| [`notebooks/12_portfolio_diversification_benefit.ipynb`](notebooks/12_portfolio_diversification_benefit.ipynb) | Portfolio diversification investigation |
| [`ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md) | Engine and display separation |
| [`ARCHITECTURE-BOUNDARIES-AND-IOC.md`](docs/architecture/ARCHITECTURE-BOUNDARIES-AND-IOC.md) | Protocol boundaries and dependency direction |
| [`ARTIFACT-TAXONOMY.md`](docs/ARTIFACT-TAXONOMY.md) | Decision-support output model |
| [`PLAN-v1-vertical-slice.md`](docs/PLAN-v1-vertical-slice.md) | Scope and workflow definition |

## Running the project
The repository does not yet declare a packaged dependency set: `pyproject.toml` currently contains pytest configuration only. From the repository root, create an environment and install the libraries used by the calculations, data providers, notebooks, and tests:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install numpy pandas matplotlib yfinance pytest jupyter
.venv/bin/python -m pytest -q
```

The test suite uses `pytest`; network-dependent tests and notebook workflows require Yahoo Finance access. The notebooks can be opened with:

```bash
.venv/bin/jupyter notebook
```

## Scope and limitations

This is a research and portfolio-risk diagnostic project, not a production trading system. It does not currently provide:

- portfolio optimisation or executable, production-ready, or automatically approved rebalance recommendations;
- transaction-cost, liquidity, tax, or market-impact modelling;
- trade execution or order management;
- factor-risk attribution;
- a claim that historical VaR forecasts are reliable in all regimes.

Those boundaries are intentional. The project demonstrates how to build quantitative tools that connect portfolio risk evidence to an investment decision while making uncertainty, assumptions, and unsupported conclusions visible.

## VaR sign convention

VaR is reported using a positive-loss convention: the underlying return quantile is negative and is negated for presentation. For example, a 95% VaR of `0.041` represents a loss estimate of 4.1% of the position value over the configured horizon.
