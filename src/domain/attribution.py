from dataclasses import dataclass


@dataclass(frozen=True)
class RiskContribution:
    """Evidence for one asset's contribution to structural portfolio volatility."""

    asset: str
    weight: float
    risk_contribution_pct: float
    cumulative_risk_contribution_pct: float


@dataclass(frozen=True)
class Attribution:
    """Immutable evidence object returned by the attribution engine."""

    portfolio_volatility: float
    risk_contributions: tuple[RiskContribution, ...]
    observation_date: str | None = None


__all__ = ["Attribution", "RiskContribution"]
