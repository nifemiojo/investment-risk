import unittest

from src.domain.attribution import Attribution, RiskContribution
from src.domain.mandate import Mandate
from src.domain.portfolio import Portfolio
from src.display.risk_drift_renderer import render_risk_drift_markdown
from src.engine.risk_drift_engine import RiskDriftEngine


def make_portfolio(mandate=None):
    return Portfolio(
        name="60/40 Multi-Asset",
        assets={"SPY": 0.40, "EFA": 0.20, "IEF": 0.25, "GLD": 0.15},
        nav=10_000_000,
        risk_budget_annual_pct=0.30,
        mandate=mandate or Mandate(
            risk_budget_by_asset={"SPY": 0.45, "EFA": 0.20, "IEF": 0.20, "GLD": 0.15}
        ),
    )


def make_attribution():
    return Attribution(
        portfolio_volatility=0.02,
        risk_contributions=(
            RiskContribution("SPY", 0.40, 0.67, 0.67),
            RiskContribution("EFA", 0.20, 0.16, 0.83),
            RiskContribution("IEF", 0.25, 0.10, 0.93),
            RiskContribution("GLD", 0.15, 0.07, 1.00),
        ),
        observation_date="2025-06-21",
    )


class RiskDriftTests(unittest.TestCase):
    def test_mandate_is_immutable_and_validates_risk_budgets(self):
        mandate = Mandate({"SPY": 0.45, "EFA": 0.20, "IEF": 0.20, "GLD": 0.15})

        with self.assertRaises((AttributeError, TypeError)):
            mandate.risk_budget_by_asset["SPY"] = 0.50

        with self.assertRaisesRegex(ValueError, "sum to 100%"):
            Mandate({"SPY": 0.60, "EFA": 0.20})

        with self.assertRaisesRegex(ValueError, "non-negative"):
            Mandate({"SPY": -0.10, "EFA": 1.10})

    def test_portfolio_requires_mandate_assets_to_match_portfolio_assets(self):
        with self.assertRaisesRegex(ValueError, "same assets"):
            make_portfolio(Mandate({"SPY": 0.50, "EFA": 0.20, "IEF": 0.20, "QQQ": 0.10}))

    def test_risk_drift_is_sorted_by_absolute_drift_descending(self):
        drift = RiskDriftEngine().calculate(make_attribution(), make_portfolio())

        self.assertEqual(
            [item.asset for item in drift.observations], ["SPY", "IEF", "GLD", "EFA"]
        )
        self.assertEqual(
            [round(item.signed_drift, 10) for item in drift.observations],
            [0.22, -0.10, -0.08, -0.04],
        )
        self.assertEqual(
            [round(item.absolute_drift, 10) for item in drift.observations],
            [0.22, 0.10, 0.08, 0.04],
        )
        self.assertEqual(
            [round(item.weight, 10) for item in drift.observations],
            [0.40, 0.25, 0.15, 0.20],
        )
        self.assertAlmostEqual(drift.portfolio_volatility, 0.02)

    def test_risk_drift_renderer_contains_minimal_evidence_only(self):
        drift = RiskDriftEngine().calculate(make_attribution(), make_portfolio())

        rendered = render_risk_drift_markdown(
            drift,
            portfolio_name="60/40 Multi-Asset",
            date="2025-06-21",
        )

        for expected in (
            "RISK CONTRIBUTION DRIFT",
            "60/40 Multi-Asset",
            "21 June 2025",
            "| Asset | Weight | Target risk contribution | Current risk contribution | Signed drift | Absolute drift |",
            "| SPY | 40% | 45% | 67% | +22.00 pp | 22.00 pp |",
            "Target risk contribution",
            "Current risk contribution",
            "Signed drift",
            "Absolute drift",
        ):
            self.assertIn(expected, rendered)
        self.assertLess(rendered.index("SPY"), rendered.index("IEF"))
        self.assertIn("21 June 2025<br><br>\n\n| Asset |", rendered)
        self.assertNotIn("REBALANCE", rendered)
        self.assertNotIn("trade", rendered.lower())

    def test_risk_drift_rejects_attribution_for_unknown_asset(self):
        portfolio = make_portfolio()
        attribution = Attribution(
            portfolio_volatility=0.02,
            risk_contributions=(RiskContribution("QQQ", 1.0, 1.0, 1.0),),
        )

        with self.assertRaisesRegex(ValueError, "do not match"):
            RiskDriftEngine().calculate(attribution, portfolio)


if __name__ == "__main__":
    unittest.main()


__all__ = ["make_attribution", "make_portfolio"]
