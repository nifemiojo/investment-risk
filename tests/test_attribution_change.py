import unittest

from src.domain.attribution import Attribution, RiskContribution
from src.domain.attribution_change import AttributionChange
from src.display.attribution_change_renderer import render_attribution_change_markdown
from src.engine.attribution_comparison_engine import AttributionComparisonEngine


class AttributionChangeTests(unittest.TestCase):
    def setUp(self):
        self.engine = AttributionComparisonEngine()

    @staticmethod
    def attribution(date, values):
        return Attribution(
            portfolio_volatility=0.01,
            risk_contributions=tuple(
                RiskContribution(asset, 0.25, value, value)
                for asset, value in values
            ),
            observation_date=date,
        )

    def test_compares_and_orders_by_absolute_change(self):
        reference = self.attribution("2020-01-03", [("SPY", 0.40), ("IEF", 0.60)])
        current = self.attribution("2021-01-04", [("SPY", 0.45), ("IEF", 0.50)])

        result = self.engine.compare(reference, current)

        self.assertIsInstance(result, AttributionChange)
        self.assertEqual([item.asset for item in result.observations], ["IEF", "SPY"])
        self.assertAlmostEqual(result.observations[0].change_percentage_points, -0.10)
        self.assertAlmostEqual(result.observations[1].change_percentage_points, 0.05)

    def test_matches_assets_independent_of_input_order(self):
        reference = self.attribution("2020-01-03", [("SPY", 0.40), ("IEF", 0.60)])
        current = self.attribution("2021-01-04", [("IEF", 0.50), ("SPY", 0.42)])

        result = self.engine.compare(reference, current)

        self.assertEqual(result.observations[0].asset, "IEF")
        self.assertAlmostEqual(result.observations[0].change_percentage_points, -0.10)

    def test_rejects_incompatible_asset_universes(self):
        reference = self.attribution("2020-01-03", [("SPY", 1.0)])
        current = self.attribution("2021-01-04", [("IEF", 1.0)])

        with self.assertRaisesRegex(ValueError, "asset universes"):
            self.engine.compare(reference, current)

    def test_renderer_uses_compact_style_and_resolved_dates(self):
        change = self.engine.compare(
            self.attribution("2020-01-03", [("SPY", 0.40)]),
            self.attribution("2021-01-04", [("SPY", 0.55)]),
        )

        rendered = render_attribution_change_markdown(
            change,
            portfolio_name="Test Portfolio",
        )

        self.assertIn("**CONTRIBUTION CHANGE**<br><br>", rendered)
        self.assertIn("Reference as of 03 January 2020", rendered)
        self.assertIn("Current as of 04 January 2021", rendered)
        self.assertIn("Change, percentage points", rendered)
        self.assertIn("+15.00 pp", rendered)
        self.assertNotIn("##", rendered)
        self.assertNotIn("reconciliation", rendered.lower())


if __name__ == "__main__":
    unittest.main()
