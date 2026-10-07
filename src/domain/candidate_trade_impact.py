from dataclasses import dataclass

from src.domain.portfolio import Portfolio
from src.domain.risk_drift import RiskContributionDrift, RiskDrift
from src.domain.candidate_trade import CandidateTrade


@dataclass(frozen=True)
class AssetTradeImpact:
    """Before/after risk evidence for one asset."""

    asset: str
    current_risk_contribution_pct: float
    proposed_risk_contribution_pct: float
    risk_contribution_change: float
    current_drift: float
    proposed_drift: float
    drift_change: float


@dataclass(frozen=True)
class CandidateTradeImpact:
    """Measured hypothetical impact of one candidate trade."""

    candidate: CandidateTrade
    current_risk: RiskDrift
    proposed_risk: RiskDrift
    proposed_portfolio: Portfolio
    portfolio_volatility_change: float
    maximum_absolute_drift_change: float
    total_absolute_drift_change: float
    breached_asset_count_change: int
    asset_impacts: tuple[AssetTradeImpact, ...]
    current_breached_asset_count: int = 0
    proposed_breached_asset_count: int = 0


def build_asset_impacts(
    current_risk: RiskDrift,
    proposed_risk: RiskDrift,
) -> tuple[AssetTradeImpact, ...]:
    current_by_asset = {item.asset: item for item in current_risk.observations}
    proposed_by_asset = {item.asset: item for item in proposed_risk.observations}
    if set(current_by_asset) != set(proposed_by_asset):
        raise ValueError("Current and proposed risk states must contain the same assets.")

    return tuple(
        AssetTradeImpact(
            asset=asset,
            current_risk_contribution_pct=current_by_asset[asset].current_risk_contribution_pct,
            proposed_risk_contribution_pct=proposed_by_asset[asset].current_risk_contribution_pct,
            risk_contribution_change=(
                proposed_by_asset[asset].current_risk_contribution_pct
                - current_by_asset[asset].current_risk_contribution_pct
            ),
            current_drift=current_by_asset[asset].signed_drift,
            proposed_drift=proposed_by_asset[asset].signed_drift,
            drift_change=proposed_by_asset[asset].signed_drift - current_by_asset[asset].signed_drift,
        )
        for asset in (item.asset for item in current_risk.observations)
    )


__all__ = ["AssetTradeImpact", "CandidateTradeImpact", "build_asset_impacts"]
