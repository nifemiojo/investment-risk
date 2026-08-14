from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Portfolio:
    """A portfolio definition. Immutable — the engine reads from this, never writes."""

    name: str
    assets: dict[str, float]       # {'SPY': 0.40, 'EFA': 0.20, ...}
    nav: float                     # 10_000_000 — Net Asset Value
    risk_budget_annual_pct: float  # 0.15 — annualised VaR limit at 95% confidence

    @property
    def tickers(self) -> list[str]:
        return list(self.assets.keys())

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