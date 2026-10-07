from dataclasses import dataclass


@dataclass(frozen=True)
class ToleranceBandObservation:
    """Risk-drift evidence classified against a symmetric tolerance band."""

    asset: str
    target_risk_contribution_pct: float
    current_risk_contribution_pct: float
    signed_drift: float
    absolute_drift: float
    tolerance: float
    lower_bound: float
    upper_bound: float
    outside_tolerance: bool
    suggested_direction: str


@dataclass(frozen=True)
class RebalanceTrigger:
    """Immutable review trigger derived from risk-contribution drift."""

    tolerance: float
    observations: tuple[ToleranceBandObservation, ...]
    triggered: bool


__all__ = ["ToleranceBandObservation", "RebalanceTrigger"]


# Direction strings are intentionally short display values for the V1 artifact.
REDUCE_SUGGESTION = "Consider reducing"
INCREASE_SUGGESTION = "Consider increasing"
NO_SUGGESTION = "No suggestion"

__all__ += ["REDUCE_SUGGESTION", "INCREASE_SUGGESTION", "NO_SUGGESTION"]


