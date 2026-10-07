from dataclasses import dataclass

import pandas as pd

from src.domain.risk_snapshot import RiskSnapshot


@dataclass(frozen=True)
class RiskChangeResult:
    """Evidence for a portfolio-level risk comparison between two closes."""

    portfolio_name: str
    requested_current_date: str
    resolved_current_date: str
    requested_previous_observation_date: str
    resolved_previous_observation_date: str
    current: RiskSnapshot
    previous_observation: RiskSnapshot
    absolute_var_change_pct_points: float
    relative_var_change_pct: float | None
    absolute_var_change_currency: float
    budget_utilisation_change_pct_points: float
    historical_percentile_change_points: float
    as_of_close_var_history: pd.Series

    @property
    def trailing_annualised_var_history(self) -> pd.Series:
        """Backward-compatible display name for the chart series."""
        return self.as_of_close_var_history
