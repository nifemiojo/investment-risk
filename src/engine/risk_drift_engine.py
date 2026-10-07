from src.domain.attribution import Attribution
from src.domain.portfolio import Portfolio
from src.domain.risk_drift import RiskContributionDrift, RiskDrift


class RiskDriftEngine:
    """Compare current structural risk contribution with mandate budgets."""

    def calculate(self, attribution: Attribution, portfolio: Portfolio) -> RiskDrift:
        """Return asset-level drift evidence ranked by absolute drift."""
        current_by_asset = {
            contribution.asset: contribution
            for contribution in attribution.risk_contributions
        }
        mandate_assets = set(portfolio.mandate.risk_budget_by_asset)
        if set(current_by_asset) != mandate_assets:
            raise ValueError("Attribution and mandate assets do not match.")

        observations = []
        for asset, target in portfolio.mandate.risk_budget_by_asset.items():
            contribution = current_by_asset[asset]
            current = contribution.risk_contribution_pct
            signed_drift = current - target
            observations.append(
                RiskContributionDrift(
                    asset=asset,
                    weight=contribution.weight,
                    target_risk_contribution_pct=target,
                    current_risk_contribution_pct=current,
                    signed_drift=signed_drift,
                    absolute_drift=abs(signed_drift),
                )
            )

        observations.sort(key=lambda item: (-item.absolute_drift, item.asset))
        return RiskDrift(
            portfolio_volatility=attribution.portfolio_volatility,
            observations=tuple(observations),
            observation_date=attribution.observation_date,
        )


__all__ = ["RiskDriftEngine"]


