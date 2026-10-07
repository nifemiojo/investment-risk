from src.domain.rebalance_trigger import (
    INCREASE_SUGGESTION,
    NO_SUGGESTION,
    REDUCE_SUGGESTION,
    RebalanceTrigger,
    ToleranceBandObservation,
)
from src.domain.risk_drift import RiskDrift


class RebalanceTriggerEngine:
    """Apply a simple tolerance policy to risk-contribution drift evidence."""

    def evaluate(self, risk_drift: RiskDrift, tolerance: float) -> RebalanceTrigger:
        """Classify drift and produce directional review suggestions."""
        if tolerance < 0:
            raise ValueError("Tolerance must be non-negative.")

        observations = tuple(
            self._classify(observation, tolerance)
            for observation in risk_drift.observations
        )
        return RebalanceTrigger(
            tolerance=tolerance,
            observations=observations,
            triggered=any(item.outside_tolerance for item in observations),
        )

    @staticmethod
    def _classify(observation, tolerance: float) -> ToleranceBandObservation:
        outside_tolerance = observation.absolute_drift > tolerance + 1e-12
        if not outside_tolerance:
            suggested_direction = NO_SUGGESTION
        elif observation.signed_drift > 0:
            suggested_direction = REDUCE_SUGGESTION
        else:
            suggested_direction = INCREASE_SUGGESTION

        return ToleranceBandObservation(
            asset=observation.asset,
            target_risk_contribution_pct=observation.target_risk_contribution_pct,
            current_risk_contribution_pct=observation.current_risk_contribution_pct,
            signed_drift=observation.signed_drift,
            absolute_drift=observation.absolute_drift,
            tolerance=tolerance,
            lower_bound=observation.target_risk_contribution_pct - tolerance,
            upper_bound=observation.target_risk_contribution_pct + tolerance,
            outside_tolerance=outside_tolerance,
            suggested_direction=suggested_direction,
        )


__all__ = ["RebalanceTriggerEngine"]


