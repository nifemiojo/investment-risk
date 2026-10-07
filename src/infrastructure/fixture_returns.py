import pandas as pd


class FixtureReturnsProvider:
    """Phase 3 returns source used to exercise the engine boundary."""

    def load(
        self,
        tickers: list[str],
        start: str,
        end: str,
    ) -> pd.DataFrame:
        """Return an empty fixture frame; Phase 4 supplies real calculations."""
        return pd.DataFrame(columns=tickers)
