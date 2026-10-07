import pandas as pd


def calculate_rolling_portfolio_volatility(
    portfolio_returns: pd.Series,
    *,
    estimation_window: int,
    display_window: int,
) -> pd.Series:
    """Calculate trailing sample standard deviation of daily portfolio returns."""
    if estimation_window <= 1:
        raise ValueError("Estimation window must be greater than one.")
    if display_window <= 0:
        raise ValueError("Display window must be positive.")

    volatility = portfolio_returns.rolling(estimation_window).std(ddof=1).dropna()
    return volatility.tail(display_window)


__all__ = ["calculate_rolling_portfolio_volatility"]
