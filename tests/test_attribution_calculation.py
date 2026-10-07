import unittest

import numpy as np

from src.attribution_calculation import calculate_component_contributions


class AttributionCalculationTests(unittest.TestCase):
    def test_one_asset_contributes_one_hundred_percent(self):
        returns = np.array([
            [0.01],
            [0.02],
            [-0.01],
            [0.03],
        ])

        result = calculate_component_contributions(returns, np.array([1.0]))

        self.assertGreater(result.portfolio_volatility, 0.0)
        np.testing.assert_allclose(result.risk_contribution_pct, [1.0])

    def test_percentage_contributions_reconcile_to_one(self):
        returns = np.array([
            [0.01, 0.005, -0.002],
            [0.02, 0.010, -0.004],
            [-0.01, -0.005, 0.002],
            [0.03, 0.015, -0.006],
        ])
        weights = np.array([0.5, 0.3, 0.2])

        result = calculate_component_contributions(returns, weights)

        self.assertAlmostEqual(sum(result.risk_contribution_pct), 1.0)

    def test_negative_correlation_can_create_negative_contribution(self):
        returns = np.array([
            [0.01, -0.008],
            [0.02, -0.015],
            [-0.01, 0.012],
            [0.03, -0.020],
        ])
        weights = np.array([0.5, 0.5])

        result = calculate_component_contributions(returns, weights)

        self.assertLess(result.risk_contribution_pct[1], 0.0)
        self.assertAlmostEqual(sum(result.risk_contribution_pct), 1.0)

    def test_zero_weight_asset_contributes_zero(self):
        returns = np.array([
            [0.01, 0.20],
            [0.02, -0.10],
            [-0.01, 0.15],
            [0.03, -0.05],
        ])
        weights = np.array([1.0, 0.0])

        result = calculate_component_contributions(returns, weights)

        self.assertAlmostEqual(result.risk_contribution_pct[1], 0.0)

    def test_asset_ordering_preserves_contribution_assignment(self):
        returns = np.array([
            [0.01, 0.005],
            [0.02, 0.010],
            [-0.01, -0.005],
            [0.03, 0.015],
        ])
        weights = np.array([0.6, 0.4])

        original = calculate_component_contributions(returns, weights)
        reversed_result = calculate_component_contributions(
            returns[:, ::-1], weights[::-1]
        )

        np.testing.assert_allclose(
            original.risk_contribution_pct,
            reversed_result.risk_contribution_pct[::-1],
        )

    def test_zero_portfolio_volatility_is_rejected(self):
        returns = np.zeros((4, 2))

        with self.assertRaises(ValueError):
            calculate_component_contributions(returns, np.array([0.5, 0.5]))


if __name__ == "__main__":
    unittest.main()


class AttributionCalculationContractTests(unittest.TestCase):
    def test_result_does_not_expose_intermediate_volatility_contributions(self):
        returns = np.array([
            [0.01, 0.005],
            [0.02, 0.010],
            [-0.01, -0.005],
            [0.03, 0.015],
        ])

        result = calculate_component_contributions(returns, np.array([0.6, 0.4]))

        self.assertFalse(hasattr(result, "risk_contribution"))
        self.assertFalse(hasattr(result, "covariance_with_portfolio"))


if __name__ == "__main__":
    unittest.main()
