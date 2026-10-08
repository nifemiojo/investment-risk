# Portfolio Risk Attribution & Decision Support

A Python diagnostic for understanding portfolio risk and evaluating allocation changes.

**What risk is the portfolio taking, where does it come from, and would a proposed change improve its risk profile?**

## What it does

- **Risk attribution:** decomposes covariance-based portfolio volatility into signed asset contributions, exposing concentration and diversification effects.
- **Risk-budget monitoring:** compares contributions with mandate targets and flags deviations outside tolerance bands.
- **Allocation-change analysis:** evaluates a hypothetical weight transfer through before/after volatility, risk contributions, drift and tolerance breaches.
- **Risk monitoring:** produces historical VaR snapshots and comparisons between observation dates.
- **VaR research:** explores historical and exponentially weighted estimates, rolling out-of-sample forecasts, breach monitoring and volatility scaling.

The implementation separates domain models, calculations, data providers and Markdown renderers. Tests cover mathematical properties, decision logic and edge cases, including contribution reconciliation, negative contributors and zero-weight holdings.

## Start here

| Example | What to look for |
|---|---|
| [Risk attribution](src/notebooks/001-risk-attribution.ipynb) | Which assets drive portfolio volatility? |
| [Risk-budget drift](src/notebooks/002-risk-drift.ipynb) | Where does the portfolio differ from its target risk allocation? |
| [Candidate trade impact](src/notebooks/003-candidate-trade-impact.ipynb) | Does a proposed allocation change improve the measures that matter? |
| [Rolling VaR backtest](notebooks/02_rolling_var_backtest.ipynb) | How do forecasts compare with subsequent realised losses? |
| [Decay weighting](notebooks/05_decay_weighting.ipynb) | How does giving recent returns more weight change VaR? |
| [Diversification research](notebooks/12_portfolio_diversification_benefit.ipynb) | How do asset interactions affect portfolio risk? |

### A decision example

The candidate-trade notebook reviews a four-asset portfolio (SPY, EFA, IEF and GLD), then tests transferring **0.50 percentage points of portfolio weight from SPY to IEF**.

In the saved historical example, volatility and total absolute risk-budget drift fall slightly, but maximum drift increases and all four assets remain outside tolerance. **Reducing volatility and improving risk-budget alignment are different outcomes.** The tool presents the comparison so the decision-maker can assess the trade-off.

The example uses a 252-observation window, a ±5 percentage-point tolerance and an observation date of 21 February 2021. Results depend on the historical data and estimation assumptions; reruns may differ.

## Run locally

From the cloned repository root, use Python 3.10+:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy pandas matplotlib yfinance pytest jupyter
python -m pytest -q -m "not integration"
jupyter notebook
```

On Windows, activate with `.venv\Scripts\activate`. Dependency versions are not pinned; `pyproject.toml` currently configures pytest rather than packaging the project. Yahoo Finance notebooks and integration tests require network access. Run `python -m pytest -q` to include integration tests.

## Code map

- [Domain models](src/domain/) — portfolios, mandates, attribution, drift and candidate impacts.
- [Engines](src/engine/) — risk calculations and decision-support workflows.
- [Data providers](src/infrastructure/) — portfolio fixtures and CSV/Yahoo Finance returns.
- [Renderers](src/display/) — readable risk and comparison reports.
- [Tests](tests/) — calculation and workflow contracts.
- [Architecture](docs/architecture/ARCHITECTURE.md) — calculation and presentation boundaries.

## Scope

This is a research and decision-support project. Candidate generation uses a simple equal-and-opposite weight transfer; it does not optimise allocations or execute trades. Costs, liquidity, taxes and factor attribution are outside the current implementation.

Historical estimates depend on the sample and model assumptions. VaR uses a loss sign convention: a reported value of `0.041` represents a 4.1% estimated loss at the chosen confidence level and horizon, not a maximum possible loss.
