import numpy as np
import pandas as pd

from src.domain.attribution import Attribution
from src.domain.portfolio import Portfolio
from src.engine.attribution_engine import AttributionEngine


class RecordingReturnsProvider:
    def __init__(self, returns):
        self.returns = returns
        self.calls = []

    def load(self, tickers, start, end):
        self.calls.append((tickers, start, end))
        return self.returns


class RecordingPortfolioRepository:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.requested_names = []

    def get(self, portfolio_name):
        self.requested_names.append(portfolio_name)
        return self.portfolio


def make_returns():
    return pd.DataFrame(
        {
            "SPY": [0.01, 0.02, -0.01, 0.03, 0.015],
            "EFA": [0.005, 0.01, -0.005, 0.015, 0.0075],
            "IEF": [-0.002, -0.004, 0.002, -0.006, -0.003],
            "GLD": [0.004, -0.002, 0.003, -0.001, 0.002],
        }
    )


def make_engine(returns):
    portfolio = Portfolio(
        name="60/40 Multi-Asset",
        assets={"SPY": 0.40, "EFA": 0.20, "IEF": 0.25, "GLD": 0.15},
        nav=10_000_000,
        risk_budget_annual_pct=0.30,
    )
    provider = RecordingReturnsProvider(returns)
    repository = RecordingPortfolioRepository(portfolio)
    return AttributionEngine(repository, provider), provider


def test_engine_uses_real_covariance_calculation_and_returns_attribution():
    engine, provider = make_engine(make_returns())

    attribution = engine.attribute(
        portfolio_name="60/40 Multi-Asset",
        date="2025-06-21",
        estimation_window=4,
    )

    assert isinstance(attribution, Attribution)
    assert attribution.portfolio_volatility != 0.018
    assert sum(item.risk_contribution_pct for item in attribution.risk_contributions) == pytest.approx(1.0)
    assert attribution.risk_contributions[-1].cumulative_risk_contribution_pct == pytest.approx(1.0)
    assert provider.calls == [
        (["SPY", "EFA", "IEF", "GLD"], "2018-01-01", "2025-06-21")
    ]


def test_engine_uses_only_requested_estimation_window():
    returns = make_returns()
    engine, _ = make_engine(returns)

    attribution = engine.attribute("60/40 Multi-Asset", "2025-06-21", 4)

    expected_covariance = returns.tail(4).cov().to_numpy()
    weights = np.array([0.40, 0.20, 0.25, 0.15])
    expected_variance = weights @ expected_covariance @ weights
    expected_volatility = np.sqrt(expected_variance)

    assert attribution.portfolio_volatility == pytest.approx(expected_volatility)


# Imported here to keep the test's numeric tolerance explicit at the assertion site.
import pytest


if __name__ == "__main__":
    pytest.main([__file__])
