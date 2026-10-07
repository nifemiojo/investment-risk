from typing import Protocol

import pandas as pd


class ReturnsProvider(Protocol):
    """Source of daily asset returns."""

    def load(
        self,
        tickers: list[str],
        start: str,
        end: str,
    ) -> pd.DataFrame:
        ...
