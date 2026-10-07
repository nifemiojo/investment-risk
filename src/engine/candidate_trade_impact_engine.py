from src.domain.attribution import Attribution
from src.domain.candidate_trade import CandidateTrade
from src.domain.candidate_trade_impact import (
    CandidateTradeImpact,
    build_asset_impacts,
)
from src.domain.portfolio import Portfolio
from src.domain.risk_drift import RiskDrift
from src.engine.rebalance_trigger_engine import RebalanceTriggerEngine
from src.engine.risk_drift_engine import RiskDriftEngine


class CandidateTradeImpactEngine:
    """Evaluate one candidate through the existing attribution and drift engines."""

    def __init__(
        self,
        attribution_engine,
        risk_drift_engine: RiskDriftEngine,
        rebalance_trigger_engine: RebalanceTriggerEngine | None = None,
    ):
        self._attribution_engine = attribution_engine
        self._risk_drift_engine = risk_drift_engine
        self._rebalance_trigger_engine = rebalance_trigger_engine or RebalanceTriggerEngine()

    def evaluate(
        self,
        portfolio: Portfolio,
        candidate: CandidateTrade,
        *,
        date: str,
        estimation_window: int,
        tolerance: float,
        current_attribution: Attribution,
    ) -> CandidateTradeImpact:
        proposed_weights = dict(portfolio.assets)
        for asset, change in candidate.weight_changes().items():
            proposed_weights[asset] += change
        proposed_portfolio = portfolio.with_weights(proposed_weights)

        current_risk = self._risk_drift_engine.calculate(current_attribution, portfolio)
        proposed_attribution = self._attribute_portfolio(
            proposed_portfolio, date, estimation_window
        )
        proposed_risk = self._risk_drift_engine.calculate(
            proposed_attribution, proposed_portfolio
        )

        current_maximum = max(item.absolute_drift for item in current_risk.observations)
        proposed_maximum = max(item.absolute_drift for item in proposed_risk.observations)
        current_total = sum(item.absolute_drift for item in current_risk.observations)
        proposed_total = sum(item.absolute_drift for item in proposed_risk.observations)
        current_review = self._rebalance_trigger_engine.evaluate(current_risk, tolerance)
        proposed_review = self._rebalance_trigger_engine.evaluate(proposed_risk, tolerance)
        current_breaches = sum(
            item.outside_tolerance for item in current_review.observations
        )
        proposed_breaches = sum(
            item.outside_tolerance for item in proposed_review.observations
        )

        return CandidateTradeImpact(
            candidate=candidate,
            current_risk=current_risk,
            proposed_risk=proposed_risk,
            proposed_portfolio=proposed_portfolio,
            portfolio_volatility_change=(
                proposed_risk.portfolio_volatility - current_risk.portfolio_volatility
            ),
            maximum_absolute_drift_change=proposed_maximum - current_maximum,
            total_absolute_drift_change=proposed_total - current_total,
            breached_asset_count_change=proposed_breaches - current_breaches,
            asset_impacts=build_asset_impacts(current_risk, proposed_risk),
            current_breached_asset_count=current_breaches,
            proposed_breached_asset_count=proposed_breaches,
        )

    def _attribute_portfolio(
        self,
        portfolio: Portfolio,
        date: str,
        estimation_window: int,
    ) -> Attribution:
        if hasattr(self._attribution_engine, "attribute_portfolio"):
            return self._attribution_engine.attribute_portfolio(
                portfolio, date, estimation_window
            )
        return self._attribution_engine.attribute(
            portfolio.name,
            date,
            estimation_window,
            portfolio_override=portfolio,
        )


__all__ = ["CandidateTradeImpactEngine"]
