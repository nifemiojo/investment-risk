from dataclasses import dataclass


@dataclass(frozen=True)
class RiskSnapshot:
    """Point-in-time risk measurement with distributional context."""

    portfolio_name: str
    timestamp: str

    var_currency: float
    var_pct: float
    var_annualised_pct: float
    nav: float

    risk_budget_annual_pct: float
    budget_utilisation: float
    is_breach: bool

    percentile_rank: float
    percentile_meaning: str
    distribution_lookback_start: str

    decision: str
