import numpy as np
import pandas as pd
import pytest

from src.domain.portfolio import Portfolio
from src.display.risk_change_renderer import (
    plot_trailing_portfolio_var,
    render_risk_change_markdown,
)
from src.engine.risk_change_engine import RiskChangeEngine
from src.rolling import rolling_var


class FakePortfolioRepository:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def get(self, name):
        return self.portfolio


class FakeReturnsProvider:
    def __init__(self, returns):
        self.returns = returns

    def load(self, tickers, start, end):
        return self.returns.loc[:end, tickers]


@pytest.fixture
def comparison():
    dates = pd.bdate_range("2024-01-01", periods=8)
    returns = pd.DataFrame(
        {"SPY": [-0.01, 0.02, -0.03, 0.01, -0.04, 0.02, -0.05, 0.01]},
        index=dates,
    )
    portfolio = Portfolio(
        name="Test Portfolio",
        assets={"SPY": 1.0},
        nav=1_000_000,
        risk_budget_annual_pct=0.30,
    )
    engine = RiskChangeEngine(
        FakePortfolioRepository(portfolio),
        FakeReturnsProvider(returns),
        var_window=3,
        var_confidence=0.95,
    )
    return engine.compare(
        "Test Portfolio",
        current_date=dates[-1].date().isoformat(),
        previous_observation_date="2024-01-06",
    ), returns


def test_comparison_calculates_signed_evidence(comparison):
    result, _ = comparison

    assert result.current.timestamp == "2024-01-10"
    assert result.previous_observation.timestamp == "2024-01-05"
    assert result.absolute_var_change_pct_points == pytest.approx(
        result.current.var_pct - result.previous_observation.var_pct
    )
    assert result.absolute_var_change_currency == pytest.approx(
        result.current.var_currency - result.previous_observation.var_currency
    )
    assert result.budget_utilisation_change_pct_points == pytest.approx(
        result.current.budget_utilisation
        - result.previous_observation.budget_utilisation
    )
    assert result.historical_percentile_change_points == pytest.approx(
        result.current.percentile_rank
        - result.previous_observation.percentile_rank
    )



def test_non_trading_reference_date_resolves_to_previous_close(comparison):
    result, _ = comparison
    weekend_result = result

    assert weekend_result.resolved_previous_observation_date == "2024-01-05"
    assert weekend_result.requested_previous_observation_date == "2024-01-06"


def test_history_relabels_forecast_rows_to_input_window_close_and_appends_current(
    comparison,
):
    result, returns = comparison
    history = result.as_of_close_var_history

    assert history.index[-1] == returns.index[-1]
    assert history.index[-2] == returns.index[-2]
    assert history.index[0] == returns.index[2]
    assert history.index.is_monotonic_increasing
    assert history.iloc[-1] == pytest.approx(result.current.var_annualised_pct)

    forecast_history = rolling_var(
        returns["SPY"], window=3, confidence=0.95
    )
    assert history.loc[returns.index[2]] == pytest.approx(
        forecast_history.iloc[0]["VaR"] * np.sqrt(252)
    )


def test_renderer_has_distinct_change_units_and_markers(comparison):
    result, _ = comparison
    markdown = render_risk_change_markdown(result)
    figure, axis = plot_trailing_portfolio_var(
        result.as_of_close_var_history,
        previous_observation_date=result.resolved_previous_observation_date,
        current_date=result.resolved_current_date,
        annualised_risk_budget=result.current.risk_budget_annual_pct,
    )

    assert "Annualised VaR" in markdown
    assert "Relative VaR change" not in markdown
    assert "pp" in markdown
    assert "risk-budget utilisation" in markdown
    assert "Current headroom" not in markdown
    assert "| Measure | Previous observation | Current observation | Change |" in markdown
    assert len(axis.lines) == 4
    assert axis.get_ylabel() == "Annualised VaR (%)"
    figure.clear()


def test_rolling_var_backtesting_contract_is_unchanged(comparison):
    _, returns = comparison
    result = rolling_var(returns["SPY"], window=3)

    assert list(result.columns) == ["VaR", "NextReturn", "Breach"]
    assert len(result) == len(returns) - 3
    assert result.index[0] == returns.index[3]


def test_reference_date_after_current_date_is_rejected(comparison):
    result, _ = comparison
    with pytest.raises(ValueError, match="later than current"):
        # Use the engine behind the result's test fixture through a fresh setup.
        dates = pd.bdate_range("2024-01-01", periods=8)
        returns = pd.DataFrame(
            {"SPY": [-0.01, 0.02, -0.03, 0.01, -0.04, 0.02, -0.05, 0.01]},
            index=dates,
        )
        portfolio = Portfolio("Test Portfolio", {"SPY": 1.0}, 1_000_000, 0.30)
        engine = RiskChangeEngine(
            FakePortfolioRepository(portfolio), FakeReturnsProvider(returns), var_window=3
        )
        engine.compare("Test Portfolio", dates[3].date().isoformat(), dates[4].date().isoformat())


def test_equal_dates_are_rejected(comparison):
    result, _ = comparison
    with pytest.raises(ValueError, match="differ"):
        dates = pd.bdate_range("2024-01-01", periods=8)
        returns = pd.DataFrame(
            {"SPY": [-0.01, 0.02, -0.03, 0.01, -0.04, 0.02, -0.05, 0.01]},
            index=dates,
        )
        portfolio = Portfolio("Test Portfolio", {"SPY": 1.0}, 1_000_000, 0.30)
        engine = RiskChangeEngine(
            FakePortfolioRepository(portfolio), FakeReturnsProvider(returns), var_window=3
        )
        engine.compare("Test Portfolio", dates[-1].date().isoformat(), dates[-1].date().isoformat())


def test_zero_reference_var_has_no_relative_change():
    dates = pd.bdate_range("2024-01-01", periods=8)
    returns = pd.DataFrame({"SPY": [0.0] * 8}, index=dates)
    portfolio = Portfolio("Flat", {"SPY": 1.0}, 1_000_000, 0.30)
    engine = RiskChangeEngine(
        FakePortfolioRepository(portfolio), FakeReturnsProvider(returns), var_window=3
    )

    result = engine.compare("Flat", dates[-1].date().isoformat(), dates[4].date().isoformat())

    assert result.relative_var_change_pct is None
