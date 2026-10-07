import unittest

from src.domain.risk_drift import RiskContributionDrift, RiskDrift
from src.display.rebalance_review_renderer import render_rebalance_review_markdown
from src.engine.rebalance_trigger_engine import RebalanceTriggerEngine


def make_risk_drift(*drifts):
    observations = tuple(
        RiskContributionDrift(
            asset=asset,
            weight=weight,
            target_risk_contribution_pct=target,
            current_risk_contribution_pct=target + drift,
            signed_drift=drift,
            absolute_drift=abs(drift),
        )
        for asset, weight, target, drift in drifts
    )
    return RiskDrift(portfolio_volatility=0.02, observations=observations)


class RebalanceTriggerTests(unittest.TestCase):
    def test_classifies_boundary_as_within_and_breach_directions(self):
        risk_drift = make_risk_drift(
            ("SPY", 0.40, 0.45, 0.05),
            ("IEF", 0.25, 0.20, -0.0501),
            ("GLD", 0.15, 0.15, 0.0),
        )

        result = RebalanceTriggerEngine().evaluate(risk_drift, tolerance=0.05)

        by_asset = {item.asset: item for item in result.observations}
        self.assertFalse(by_asset["SPY"].outside_tolerance)
        self.assertEqual(by_asset["SPY"].suggested_direction, "No suggestion")
        self.assertTrue(by_asset["IEF"].outside_tolerance)
        self.assertEqual(by_asset["IEF"].suggested_direction, "Consider increasing")
        self.assertEqual(by_asset["GLD"].suggested_direction, "No suggestion")
        self.assertTrue(result.triggered)

    def test_positive_breach_suggests_reducing(self):
        result = RebalanceTriggerEngine().evaluate(
            make_risk_drift(("SPY", 0.40, 0.45, 0.06)), tolerance=0.05
        )

        observation = result.observations[0]
        self.assertTrue(observation.outside_tolerance)
        self.assertEqual(observation.suggested_direction, "Consider reducing")

    def test_all_assets_within_tolerance_do_not_trigger_review(self):
        result = RebalanceTriggerEngine().evaluate(
            make_risk_drift(
                ("SPY", 0.40, 0.45, 0.05),
                ("IEF", 0.25, 0.20, -0.05),
            ),
            tolerance=0.05,
        )

        self.assertFalse(result.triggered)
        self.assertTrue(all(not item.outside_tolerance for item in result.observations))

    def test_rejects_negative_tolerance(self):
        with self.assertRaisesRegex(ValueError, "non-negative"):
            RebalanceTriggerEngine().evaluate(make_risk_drift(("SPY", 0.4, 0.45, 0.0)), -0.01)

    def test_observations_preserve_risk_drift_order(self):
        result = RebalanceTriggerEngine().evaluate(
            make_risk_drift(
                ("SPY", 0.40, 0.45, 0.06),
                ("IEF", 0.25, 0.20, -0.01),
            ),
            tolerance=0.05,
        )

        self.assertEqual([item.asset for item in result.observations], ["SPY", "IEF"])

    def test_renderer_shows_review_and_directional_suggestions_without_trade_sizes(self):
        result = RebalanceTriggerEngine().evaluate(
            make_risk_drift(
                ("SPY", 0.40, 0.45, 0.22),
                ("IEF", 0.25, 0.20, -0.10),
                ("EFA", 0.20, 0.20, -0.04),
            ),
            tolerance=0.05,
        )

        rendered = render_rebalance_review_markdown(
            result,
            portfolio_name="60/40 Multi-Asset",
            date="2025-06-21",
        )

        for expected in (
            "RISK DRIFT — REBALANCE REVIEW",
            "60/40 Multi-Asset",
            "21 June 2025",
            "Tolerance band: ±5.00 percentage points",
            "REVIEW REBALANCE",
            "| Asset | Target | Current | Drift | Band | Status | Suggested direction |",
            "| SPY | 45% | 67% | +22.00 pp | ±5.00 pp | Outside | Consider reducing |",
            "| IEF | 20% | 10% | -10.00 pp | ±5.00 pp | Outside | Consider increasing |",
            "| EFA | 20% | 16% | -4.00 pp | ±5.00 pp | Within | No suggestion |",
            "does not determine trade size",
        ):
            self.assertIn(expected, rendered)

        self.assertNotIn("£", rendered)
        self.assertNotIn("Execute", rendered)


if __name__ == "__main__":
    unittest.main()


__all__ = ["make_risk_drift"]
