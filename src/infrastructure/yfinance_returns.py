import pandas as pd
import yfinance as yf


class YFinanceReturnsProvider:
    """
    Downloads close prices from Yahoo Finance and returns daily percentage
    returns as a DataFrame (dates × tickers).
    """

    def load(
        self,
        tickers: list[str],
        start: str,
        end: str,
    ) -> pd.DataFrame:
        """
        Return a DataFrame of daily decimal returns.

        Index: DatetimeIndex (trading days)
        Columns: one per ticker
        Values: daily percentage returns as decimals (e.g. 0.02 = 2%)
        """
        prices = self._download(tickers, start, end)
        returns = prices.pct_change().dropna()
        return returns

    def _download(
        self,
        tickers: list[str],
        start: str,
        end: str,
    ) -> pd.DataFrame:
        """Download adjusted close prices. Handles single and multi-ticker cases."""
        raw = yf.download(
            tickers,
            start=start,
            end=end,
            auto_adjust=True,
            progress=False,
        )

        if raw is None or raw.empty:
            raise RuntimeError(f"No data returned for {tickers} from {start} to {end}")

        # yfinance returns different column structures:
        # - Single ticker: columns = ['Close', 'High', 'Low', 'Open', 'Volume']
        # - Multi ticker:  columns = MultiIndex with ('Close', 'SPY'), etc.
        if isinstance(raw.columns, pd.MultiIndex):
            prices = raw["Close"].copy()
        else:
            prices = raw[["Close"]].copy()
            prices.columns = tickers

        # Ensure column names are plain strings
        prices.columns = [str(c) for c in prices.columns]
        return prices