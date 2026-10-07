from dataclasses import dataclass


@dataclass(frozen=True)
class RiskContributionDrift:
    """Evidence comparing one asset's contribution with its mandate budget."""

    asset: str
    weight: float
    target_risk_contribution_pct: float
    current_risk_contribution_pct: float
    signed_drift: float
    absolute_drift: float


@dataclass(frozen=True)
class RiskDrift:
    """Immutable risk-contribution drift evidence."""

    portfolio_volatility: float
    observations: tuple[RiskContributionDrift, ...]
    observation_date: str | None = None


__all__ = ["RiskContributionDrift", "RiskDrift"]


