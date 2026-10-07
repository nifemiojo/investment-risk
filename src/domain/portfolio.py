from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from src.domain.mandate import Mandate


@dataclass(frozen=True)
class Portfolio:
    """A portfolio definition with an immutable investment mandate."""

    name: str
    assets: dict[str, float]       # {'SPY': 0.40, 'EFA': 0.20, ...}
    nav: float                     # 10_000_000 — Net Asset Value
    risk_budget_annual_pct: float  # 0.15 — annualised VaR limit at 95% confidence
    mandate: Mandate | None = field(default=None)

    def __post_init__(self) -> None:
        mandate = self.mandate or Mandate(self.assets)
        if set(mandate.risk_budget_by_asset) != set(self.assets):
            raise ValueError("Mandate and portfolio must contain the same assets.")
        object.__setattr__(self, "mandate", mandate)

    @property
    def tickers(self) -> list[str]:
        return list(self.assets.keys())

    def with_weights(self, weights: dict[str, float]) -> "Portfolio":
        """Return an immutable portfolio copy with validated weights."""
        if set(weights) != set(self.assets):
            raise ValueError("Proposed weights must contain the same assets.")
        if any(weight < 0 for weight in weights.values()):
            raise ValueError("Portfolio weights cannot be negative.")
        if not np.isclose(sum(weights.values()), 1.0):
            raise ValueError("Portfolio weights must sum to one.")
        normalized_weights = {
            asset: round(weight, 12) for asset, weight in weights.items()
        }
        return Portfolio(
            name=self.name,
            assets=normalized_weights,
            nav=self.nav,
            risk_budget_annual_pct=self.risk_budget_annual_pct,
            mandate=self.mandate,
        )

    def returns(self, asset_returns: pd.DataFrame) -> pd.Series:
        """
        Compute the portfolio's daily return series from asset-level returns.

        Parameters
        ----------
        asset_returns : pd.DataFrame
            Daily returns, index = dates, columns = tickers.

        Returns
        -------
        pd.Series
            Weighted portfolio returns, index = dates.
        """
        tickers = list(self.assets.keys())
        weights = np.array([self.assets[t] for t in tickers])
        aligned = asset_returns[tickers].dropna()
        return (aligned * weights).sum(axis=1)