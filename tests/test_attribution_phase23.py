import unittest

import pandas as pd

from src.domain.attribution import Attribution, RiskContribution
from src.domain.portfolio import Portfolio
from src.display.attribution_renderer import render_attribution_markdown
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


class AttributionPhase23Tests(unittest.TestCase):
    def setUp(self):
        self.portfolio = Portfolio(
            name="60/40 Multi-Asset",
            assets={"SPY": 0.40, "EFA": 0.20, "IEF": 0.25, "GLD": 0.15},
            nav=10_000_000,
            risk_budget_annual_pct=0.30,
        )
        self.portfolios = RecordingPortfolioRepository(self.portfolio)
        self.returns_provider = RecordingReturnsProvider(make_returns())
        self.engine = AttributionEngine(self.portfolios, self.returns_provider)

    def test_domain_objects_are_immutable(self):
        contribution = RiskContribution("SPY", 0.40, 0.62, 0.62)
        attribution = Attribution(0.018, (contribution,))

        with self.assertRaises(AttributeError):
            contribution.weight = 0.50
        with self.assertRaises(AttributeError):
            attribution.portfolio_volatility = 0.02

    def test_engine_resolves_portfolio_and_requests_returns(self):
        attribution = self.engine.attribute(
            "60/40 Multi-Asset", "2025-06-21", 4
        )

        self.assertEqual(self.portfolios.requested_names, ["60/40 Multi-Asset"])
        self.assertEqual(
            self.returns_provider.calls,
            [(["SPY", "EFA", "IEF", "GLD"], "2018-01-01", "2025-06-21")],
        )
        self.assertIsInstance(attribution, Attribution)

    def test_engine_returns_signed_ranked_cumulative_evidence(self):
        attribution = self.engine.attribute(
            "60/40 Multi-Asset", "2025-06-21", 4
        )
        contributions = attribution.risk_contributions

        self.assertEqual(
            [item.asset for item in contributions],
            sorted(
                ["SPY", "EFA", "IEF", "GLD"],
                key=lambda asset: next(
                    item.risk_contribution_pct
                    for item in contributions
                    if item.asset == asset
                ),
                reverse=True,
            ),
        )
        self.assertAlmostEqual(
            sum(item.risk_contribution_pct for item in contributions), 1.0
        )
        self.assertAlmostEqual(
            contributions[-1].cumulative_risk_contribution_pct, 1.0
        )

    def test_renderer_consumes_contract_and_contains_boundary(self):
        attribution = self.engine.attribute(
            "60/40 Multi-Asset", "2025-06-21", 4
        )
        rendered = render_attribution_markdown(
            attribution,
            portfolio_name="60/40 Multi-Asset",
            date="2025-06-21",
            estimation_window=4,
        )

        for expected in (
            "60/40 Multi-Asset",
            "21 June 2025",
            "SPY",
            "IEF",
            "Cumulative risk contribution",
        ):
            self.assertIn(expected, rendered)
        self.assertNotIn("##", rendered)
        self.assertNotIn("Component contributions describe", rendered)
        self.assertNotIn("Volatility:", rendered)
        self.assertNotIn("decision", rendered.lower())


if __name__ == "__main__":
    unittest.main()


# Kept as a named module-level fixture for the phase 5 tests that reuse it.
__all__ = ["make_returns"]
