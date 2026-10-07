from src.domain.attribution import Attribution
from src.domain.attribution_change import (
    AttributionChange,
    AttributionChangeObservation,
)


class AttributionComparisonEngine:
    """Compare contribution percentages from two attribution states."""

    def compare(
        self,
        reference_attribution: Attribution,
        current_attribution: Attribution,
    ) -> AttributionChange:
        reference_by_asset = {
            item.asset: item.risk_contribution_pct
            for item in reference_attribution.risk_contributions
        }
        current_by_asset = {
            item.asset: item.risk_contribution_pct
            for item in current_attribution.risk_contributions
        }
        if set(reference_by_asset) != set(current_by_asset):
            raise ValueError("Reference and current asset universes must match.")

        observations = [
            AttributionChangeObservation(
                asset=asset,
                reference_contribution_percentage=reference_by_asset[asset],
                current_contribution_percentage=current_by_asset[asset],
                change_percentage_points=(
                    current_by_asset[asset] - reference_by_asset[asset]
                ),
            )
            for asset in reference_by_asset
        ]
        observations.sort(
            key=lambda observation: abs(observation.change_percentage_points),
            reverse=True,
        )

        return AttributionChange(
            reference_date=reference_attribution.observation_date or "",
            current_date=current_attribution.observation_date or "",
            observations=tuple(observations),
        )


__all__ = ["AttributionComparisonEngine"]
