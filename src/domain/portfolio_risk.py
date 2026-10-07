from dataclasses import dataclass


@dataclass(frozen=True)
class VolatilityObservation:
    date: str
    volatility: float


@dataclass(frozen=True)
class PortfolioRisk:
    current_volatility: float
    volatility_history: tuple[VolatilityObservation, ...]
    previous_month_volatility: float | None = None
    previous_month_observation_date: str | None = None


__all__ = ["PortfolioRisk", "VolatilityObservation"]
