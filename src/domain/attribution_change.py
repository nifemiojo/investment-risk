from dataclasses import dataclass


@dataclass(frozen=True)
class AttributionChangeObservation:
    """One asset's change in structural risk contribution percentage."""

    asset: str
    reference_contribution_percentage: float
    current_contribution_percentage: float
    change_percentage_points: float


@dataclass(frozen=True)
class AttributionChange:
    """Evidence comparing two point-in-time attribution states."""

    reference_date: str
    current_date: str
    observations: tuple[AttributionChangeObservation, ...]


__all__ = ["AttributionChange", "AttributionChangeObservation"]
