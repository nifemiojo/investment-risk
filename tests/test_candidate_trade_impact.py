import unittest

from src.domain.attribution import Attribution, RiskContribution
from src.domain.candidate_trade import CandidateTrade
from src.domain.candidate_trade_impact import CandidateTradeImpact
from src.domain.mandate import Mandate
from src.domain.portfolio import Portfolio
from src.domain.rebalance_trigger import RebalanceTrigger, ToleranceBandObservation
from src.domain.risk_drift import RiskContributionDrift, RiskDrift
from src.display.candidate_trade_impact_renderer import render_candidate_trade_impact_markdown
from src.engine.candidate_trade_engine import CandidateTradeEngine
from src.engine.candidate_trade_impact_engine import CandidateTradeImpactEngine
from src.engine.rebalance_trigger_engine import RebalanceTriggerEngine
from src.engine.risk_drift_engine import RiskDriftEngine


class StubAttributionEngine:
    def __init__(self, attribution_by_weights):
        self._attribution_by_weights = attribution_by_weights

    def attribute_portfolio(self, portfolio, date, estimation_window):
        return self._attribution_by_weights[tuple(portfolio.assets.values())]


def make_risk_drift(*items):
    observations = tuple(
        RiskContributionDrift(
            asset=asset,
            weight=weight,
            target_risk_contribution_pct=target,
            current_risk_contribution_pct=target + drift,
            signed_drift=drift,
            absolute_drift=abs(drift),
        )
        for asset, weight, target, drift in items
    )
    return RiskDrift(portfolio_volatility=0.02, observations=observations)


def make_review(*items, tolerance=0.05):
    risk_drift = make_risk_drift(*items)
    return RebalanceTriggerEngine().evaluate(risk_drift, tolerance=tolerance)


class CandidateTradeEngineTests(unittest.TestCase):
    def test_selects_largest_positive_and_most_negative_outside_band(self):
        review = make_review(
            ("SPY", 0.40, 0.45, 0.12),
            ("IEF", 0.25, 0.20, -0.13),
            ("EFA", 0.20, 0.20, -0.08),
            ("GLD", 0.15, 0.15, 0.02),
        )

        result = CandidateTradeEngine().generate(review, transfer_weight=0.005)

        self.assertIsNotNone(result.candidate)
        self.assertEqual(result.candidate.donor_asset, "SPY")
        self.assertEqual(result.candidate.receiver_asset, "IEF")
        self.assertEqual(result.candidate.weight_changes(), {"SPY": -0.005, "IEF": 0.005})
        self.assertIsNone(result.reason)

    def test_returns_no_candidate_when_one_direction_is_missing(self):
        review = make_review(
            ("SPY", 0.40, 0.45, 0.12),
            ("IEF", 0.25, 0.20, -0.02),
        )

        result = CandidateTradeEngine().generate(review, transfer_weight=0.005)

        self.assertIsNone(result.candidate)
        self.assertEqual(result.reason, "No eligible donor and receiver were available.")

    def test_rejects_non_positive_transfer(self):
        review = make_review(("SPY", 0.40, 0.45, 0.12), ("IEF", 0.25, 0.20, -0.13))

        with self.assertRaisesRegex(ValueError, "positive"):
            CandidateTradeEngine().generate(review, transfer_weight=0.0)


class CandidateTradeImpactEngineTests(unittest.TestCase):
    def test_applies_candidate_and_calculates_before_after_metrics(self):
        portfolio = Portfolio(
            name="Test",
            assets={"SPY": 0.40, "IEF": 0.60},
            nav=100.0,
            risk_budget_annual_pct=0.30,
            mandate=Mandate({"SPY": 0.50, "IEF": 0.50}),
        )
        current_attribution = Attribution(
            portfolio_volatility=0.020,
            risk_contributions=(
                RiskContribution("SPY", 0.40, 0.60, 0.60),
                RiskContribution("IEF", 0.60, 0.40, 1.00),
            ),
            observation_date="2025-06-21",
        )
        proposed_attribution = Attribution(
            portfolio_volatility=0.018,
            risk_contributions=(
                RiskContribution("SPY", 0.35, 0.55, 0.55),
                RiskContribution("IEF", 0.65, 0.45, 1.00),
            ),
            observation_date="2025-06-21",
        )
        attribution_engine = StubAttributionEngine(
            {
                (0.40, 0.60): current_attribution,
                (0.35, 0.65): proposed_attribution,
            }
        )
        candidate = CandidateTrade("SPY", "IEF", 0.05)

        impact = CandidateTradeImpactEngine(
            attribution_engine=attribution_engine,
            risk_drift_engine=RiskDriftEngine(),
            rebalance_trigger_engine=RebalanceTriggerEngine(),
        ).evaluate(
            portfolio,
            candidate,
            date="2025-06-21",
            estimation_window=20,
            tolerance=0.05,
            current_attribution=current_attribution,
        )

        self.assertEqual(impact.proposed_portfolio.assets, {"SPY": 0.35, "IEF": 0.65})
        self.assertEqual(portfolio.assets, {"SPY": 0.40, "IEF": 0.60})
        self.assertAlmostEqual(impact.portfolio_volatility_change, -0.002)
        self.assertAlmostEqual(impact.maximum_absolute_drift_change, -0.05)
        self.assertAlmostEqual(impact.total_absolute_drift_change, -0.10)
        self.assertEqual(impact.breached_asset_count_change, -2)
        impact_by_asset = {item.asset: item for item in impact.asset_impacts}
        self.assertAlmostEqual(impact_by_asset["SPY"].risk_contribution_change, -0.05)


class CandidateTradeImpactRendererTests(unittest.TestCase):
    def test_render_contains_candidate_and_plain_evidence_sections(self):
        candidate = CandidateTrade("SPY", "IEF", 0.005)
        current = RiskDrift(
            0.020,
            (
                RiskContributionDrift("SPY", 0.40, 0.45, 0.57, 0.12, 0.12),
                RiskContributionDrift("IEF", 0.60, 0.55, 0.43, -0.12, 0.12),
            ),
            "2025-06-21",
        )
        proposed = RiskDrift(
            0.018,
            (
                RiskContributionDrift("SPY", 0.35, 0.45, 0.55, 0.10, 0.10),
                RiskContributionDrift("IEF", 0.65, 0.55, 0.45, -0.10, 0.10),
            ),
            "2025-06-21",
        )
        impact = CandidateTradeImpact(
            candidate=candidate,
            current_risk=current,
            proposed_risk=proposed,
            proposed_portfolio=Portfolio(
                "Test",
                {"SPY": 0.395, "IEF": 0.605},
                100.0,
                0.30,
                Mandate({"SPY": 0.45, "IEF": 0.55}),
            ),
            portfolio_volatility_change=-0.002,
            maximum_absolute_drift_change=-0.02,
            total_absolute_drift_change=-0.04,
            breached_asset_count_change=0,
            asset_impacts=(),
        )

        rendered = render_candidate_trade_impact_markdown(
            impact, portfolio_name="Test", date="2025-06-21"
        )

        for expected in (
            "CANDIDATE TRADE IMPACT",
            "Sell SPY / Buy IEF",
            "Weight transfer: 0.50 percentage points",
            "Portfolio volatility",
            "Maximum absolute RC drift",
            "Current",
            "Proposed",
            "hypothetical equal-and-opposite weight transfer",
            "not an optimised rebalance",
        ):
            self.assertIn(expected, rendered)


if __name__ == "__main__":
    unittest.main()
