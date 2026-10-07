import unittest

import numpy as np
import pandas as pd

from src.portfolio_volatility import calculate_rolling_portfolio_volatility
from src.domain.portfolio_risk import PortfolioRisk
from src.domain.portfolio import Portfolio
from src.engine.portfolio_risk_engine import PortfolioRiskEngine
from src.display.portfolio_risk_renderer import (
    plot_rolling_portfolio_volatility,
    render_portfolio_risk_markdown,
)


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

    def get(self, portfolio_name):
        return self.portfolio


def make_returns(count=45):
    dates = pd.date_range("2025-01-01", periods=count, freq="D")
    return pd.DataFrame(
        {"SPY": np.arange(1, count + 1) / 1000},
        index=dates,
    )


class PortfolioRiskTests(unittest.TestCase):
    def test_rolling_volatility_uses_trailing_sample_standard_deviation(self):
        returns = pd.Series(
            [0.01, 0.02, 0.04, 0.03],
            index=pd.date_range("2025-01-01", periods=4),
        )

        result = calculate_rolling_portfolio_volatility(
            returns, estimation_window=3, display_window=2
        )

        expected = returns.rolling(3).std().dropna().tail(2)
        pd.testing.assert_series_equal(result, expected)

    def test_portfolio_risk_result_contains_current_level_and_history(self):
        observation = PortfolioRisk(
            current_volatility=0.02,
            volatility_history=(),
        )

        with self.assertRaises(AttributeError):
            observation.current_volatility = 0.03

    def test_engine_builds_current_level_and_rolling_history_from_current_weights(self):
        portfolio = Portfolio(
            name="One Asset",
            assets={"SPY": 1.0},
            nav=1_000_000,
            risk_budget_annual_pct=0.30,
        )
        returns = make_returns()
        provider = RecordingReturnsProvider(returns)
        engine = PortfolioRiskEngine(
            RecordingPortfolioRepository(portfolio), provider
        )

        result = engine.calculate(
            "One Asset", "2025-02-14", estimation_window=3, display_window=45
        )

        expected_history = returns["SPY"].rolling(3).std().dropna().tail(45)
        self.assertIsInstance(result, PortfolioRisk)
        self.assertEqual(len(result.volatility_history), 43)
        self.assertEqual(
            [item.date for item in result.volatility_history],
            [date.isoformat() for date in expected_history.index],
        )
        self.assertEqual(result.current_volatility, expected_history.iloc[-1])
        self.assertEqual(result.previous_month_observation_date, "2025-01-14T00:00:00")
        self.assertEqual(
            result.previous_month_volatility,
            expected_history.loc["2025-01-14"],
        )
        self.assertEqual(
            provider.calls,
            [(["SPY"], "2018-01-01", "2025-02-14")],
        )

    def test_portfolio_risk_renderer_produces_level_markdown_and_figure(self):
        history = (
            ("2025-01-07", 0.01),
            ("2025-01-08", 0.02),
        )
        risk = PortfolioRisk(
            current_volatility=0.02,
            volatility_history=tuple(
                type("Observation", (), {"date": date, "volatility": value})()
                for date, value in history
            ),
        )

        markdown = render_portfolio_risk_markdown(
            risk, portfolio_name="One Asset", requested_date="2025-01-08"
        )
        figure = plot_rolling_portfolio_volatility(
            risk.volatility_history,
            portfolio_name="One Asset",
            requested_date="2025-01-08",
        )

        self.assertIn("Portfolio risk", markdown)
        self.assertIn("0.02%", markdown)
        self.assertEqual(figure.axes[0].get_ylabel(), "Daily volatility (%)")
        self.assertEqual(len(figure.axes[0].lines[0].get_xdata()), 2)


if __name__ == "__main__":
    unittest.main()
