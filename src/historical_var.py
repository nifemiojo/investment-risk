"""
Historical VaR calculator — single asset.

Pure calculation: accepts returns, not tickers or download logic.
The function should not know where the data came from.
"""

import numpy as np

# Map domain names to numpy percentile methods — internal detail.
_PERCENTILE_METHOD = {
    "interpolation": "linear",   # smooth estimate between adjacent returns
    "nearest-rank": "lower",     # discrete: "the Nth worst day"
}


def historical_var(
    returns,
    confidence: float = 0.95,
    method: str = "interpolation",
    position_value: float | None = None,
    window: int | None = None,
) -> float:
    """
    Compute historical Value-at-Risk for a series of returns.

    Parameters
    ----------
    returns : array-like
        Decimal returns (e.g. 0.02 for 2%). Sorting is not required;
        the function handles it internally.
    confidence : float, default 0.95
        Confidence level. 0.95 → 95% VaR, 0.99 → 99% VaR.
    method : str, default "interpolation"
        Percentile convention.
        ``"interpolation"`` — smooth estimate between adjacent returns
        (production standard).
        ``"nearest-rank"`` — discrete, maps to a specific day.
    position_value : float, optional
        If provided, returns VaR in currency rather than percentage.
    window : int, optional
        If provided, only the last ``window`` returns are used.
        Useful when the caller has a long history but only wants
        VaR from the most recent window.

    Returns
    -------
    float
        VaR as a positive number. If position_value is None, returns
        percentage VaR (e.g. 0.032 for 3.2%). If position_value is
        provided, returns currency VaR (e.g. 32_000 for £32,000).

    Raises
    ------
    ValueError
        If returns is empty, contains NaN, confidence is outside
        (0, 1), method is unrecognised, or the provided window
        exceeds the number of available returns.

    Examples
    --------
    >>> historical_var([-0.05, -0.03, -0.02, -0.01, 0.00, 0.01, 0.02, 0.03, 0.04, 0.05])
    0.041

    >>> historical_var([-0.05, -0.03, -0.02, -0.01, 0.00, 0.01, 0.02, 0.03, 0.04, 0.05],
    ...                 confidence=0.95, position_value=1_000_000)
    41000.0

    >>> historical_var([-0.05, -0.03, -0.02, -0.01, 0.00, 0.01, 0.02, 0.03, 0.04, 0.05],
    ...                 window=5)
    0.01
    """
    if method not in _PERCENTILE_METHOD:
        raise ValueError(
            f"Unknown method '{method}'. "
            f"Expected one of: {', '.join(_PERCENTILE_METHOD)}."
        )

    returns = np.asarray(returns, dtype=float)

    if returns.size == 0:
        raise ValueError("Cannot compute VaR from an empty return series.")

    if np.any(np.isnan(returns)):
        raise ValueError("Return series contains NaN values. "
                         "Clean the data before computing VaR.")

    if not (0 < confidence < 1):
        raise ValueError(f"Confidence must be between 0 and 1, got {confidence}.")

    if window is not None:
        if window > returns.size:
            raise ValueError(
                f"Window ({window}) exceeds available returns "
                f"({returns.size})."
            )
        returns = returns[-window:]

    # VaR uses the left tail e.g. 0.95 confidence → 0.05 percentile
    tail_quantile = 1.0 - confidence

    percentile = np.quantile(returns,
                             tail_quantile,
                             method=_PERCENTILE_METHOD[method])

    # Positive loss convention: negate the (negative) quantile
    var_pct = -percentile

    if position_value is not None:
        return float(var_pct * position_value)

    return float(var_pct)
