import numpy as np
import pandas as pd

from src.domain.risk_change import RiskChangeResult
from src.engine.risk_snapshot_engine import RiskSnapshotEngine
from src.rolling import rolling_var


class RiskChangeEngine:
    """Calculate evidence for a two-date portfolio risk comparison."""

    def __init__(
        self,
        portfolios,
        returns_provider,
        var_window: int = 252,
        var_confidence: float = 0.95,
    ):
        self.portfolios = portfolios
        self.returns_provider = returns_provider
        self.var_window = var_window
        self.var_confidence = var_confidence

    def compare(
        self,
        portfolio_name: str,
        current_date: str,
        previous_observation_date: str,
    ) -> RiskChangeResult:
        requested_current_timestamp = pd.Timestamp(current_date)
        requested_previous_timestamp = pd.Timestamp(previous_observation_date)
        if requested_previous_timestamp > requested_current_timestamp:
            raise ValueError(
                "Previous observation date must not be later than current date."
            )

        portfolio = self.portfolios.get(portfolio_name)
        asset_returns = self.returns_provider.load(
            portfolio.tickers,
            start="2018-01-01",
            end=current_date,
        )
        portfolio_returns = portfolio.returns(asset_returns)
        available_dates = pd.DatetimeIndex(portfolio_returns.index).sort_values()

        resolved_current = self._resolve_date(current_date, available_dates)
        resolved_previous = self._resolve_date(
            previous_observation_date, available_dates
        )
        if resolved_previous > resolved_current:
            raise ValueError(
                "Previous observation date must not be later than current date."
            )
        if resolved_previous == resolved_current:
            raise ValueError(
                "Previous observation date must differ from current date."
            )

        snapshot_engine = RiskSnapshotEngine(
            self.portfolios,
            _BoundReturnsProvider(asset_returns),
            var_window=self.var_window,
            var_confidence=self.var_confidence,
        )
        current_snapshot = snapshot_engine.snapshot(
            portfolio_name, resolved_current.date().isoformat()
        )
        previous_observation_snapshot = snapshot_engine.snapshot(
            portfolio_name, resolved_previous.date().isoformat()
        )

        rolling_forecast_var = rolling_var(
            portfolio_returns.loc[:resolved_current],
            window=self.var_window,
            confidence=self.var_confidence,
        )
        # rolling_var() labels a VaR forecast with the day being tested. Move
        # each value back to the close through which its input window runs.
        as_of_close_var_history = rolling_forecast_var["VaR"].copy()
        as_of_close_var_history.index = portfolio_returns.index[
            self.var_window - 1 : len(rolling_forecast_var) + self.var_window - 1
        ]
        as_of_close_var_history = as_of_close_var_history * np.sqrt(252)
        as_of_close_var_history.name = "Annualised VaR"
        as_of_close_var_history.loc[resolved_current] = current_snapshot.var_annualised_pct
        as_of_close_var_history = as_of_close_var_history.sort_index()

        absolute_var_change = (
            current_snapshot.var_pct - previous_observation_snapshot.var_pct
        )
        relative_var_change = (
            absolute_var_change / previous_observation_snapshot.var_pct
            if previous_observation_snapshot.var_pct != 0
            else None
        )

        return RiskChangeResult(
            portfolio_name=portfolio.name,
            requested_current_date=current_date,
            resolved_current_date=current_snapshot.timestamp,
            requested_previous_observation_date=previous_observation_date,
            resolved_previous_observation_date=previous_observation_snapshot.timestamp,
            current=current_snapshot,
            previous_observation=previous_observation_snapshot,
            absolute_var_change_pct_points=absolute_var_change,
            relative_var_change_pct=relative_var_change,
            absolute_var_change_currency=(
                current_snapshot.var_currency
                - previous_observation_snapshot.var_currency
            ),
            budget_utilisation_change_pct_points=(
                current_snapshot.budget_utilisation
                - previous_observation_snapshot.budget_utilisation
            ),
            historical_percentile_change_points=(
                current_snapshot.percentile_rank
                - previous_observation_snapshot.percentile_rank
            ),
            as_of_close_var_history=as_of_close_var_history,
        )

    @staticmethod
    def _resolve_date(date_value: str, available_dates: pd.DatetimeIndex) -> pd.Timestamp:
        requested = pd.Timestamp(date_value)
        eligible_dates = available_dates[available_dates <= requested]
        if len(eligible_dates) == 0:
            raise ValueError(f"No available close on or before {date_value}.")
        return eligible_dates[-1]


class _BoundReturnsProvider:
    """Return one already-loaded frame while preserving the provider contract."""

    def __init__(self, asset_returns: pd.DataFrame):
        self.asset_returns = asset_returns

    def load(self, tickers: list[str], start: str, end: str) -> pd.DataFrame:
        return self.asset_returns.loc[:end, tickers]
