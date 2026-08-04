"""
Rolling historical VaR — compute out-of-sample VaR estimates
and monitor breaches over time.

Note: ``rolling_var`` is a backtesting tool. It produces historical
VaR estimates and checks them against realised returns. For a
forward-looking VaR (tomorrow's risk), use ``historical_var`` directly
on the most recent window.
"""

import pandas as pd
from src.historical_var import historical_var
from src.decay import decay_var


def rolling_var(
    returns: pd.Series,
    window: int = 252,
    confidence: float = 0.95,
) -> pd.DataFrame:
    """
    Compute rolling out-of-sample historical VaR.

    For each day after the initial warm-up window, computes VaR using
    the preceding ``window`` returns. The current day's return is
    excluded — no look-ahead bias.

    Parameters
    ----------
    returns : pd.Series
        Daily percentage returns as decimals, with a DatetimeIndex.
    window : int, default 252
        Number of historical observations used for each VaR estimate.
    confidence : float, default 0.95
        Confidence level for VaR.

    Returns
    -------
    pd.DataFrame
        DataFrame with a DatetimeIndex and columns:

        - ``VaR`` — VaR estimate (positive, as decimal).
        - ``NextReturn`` — the actual return on the forecast day.
        - ``Breach`` — True if the actual loss exceeded VaR.

    Raises
    ------
    ValueError
        If ``returns`` has fewer than ``window + 1`` observations.
    """
    if len(returns) < window + 1:
        raise ValueError(
            f"Need at least {window + 1} observations for a {window}-day "
            f"rolling VaR. Got {len(returns)}."
        )

    var_values = []
    next_returns = []
    breaches = []
    dates = []

    for day in range(window, len(returns)):
        window_returns = returns.iloc[day - window : day]
        var = historical_var(window_returns, confidence=confidence)

        next_return = returns.iloc[day]
        # Breach: actual loss (-return) exceeds VaR
        breach = -next_return > var

        dates.append(returns.index[day])
        var_values.append(var)
        next_returns.append(next_return)
        breaches.append(breach)

    return pd.DataFrame(
        {
            "VaR": var_values,
            "NextReturn": next_returns,
            "Breach": breaches,
        },
        index=pd.DatetimeIndex(dates, name="Date"),
    )


def breach_summary(
    df: pd.DataFrame,
    confidence: float = 0.95,
) -> dict:
    """
    Summarise breach performance against expected rate.

    Parameters
    ----------
    df : pd.DataFrame
        Output from ``rolling_var``. Must have a ``Breach`` column.
    confidence : float, default 0.95
        Confidence level used to compute the expected breach rate.

    Returns
    -------
    dict
        Keys: ``total_observations``, ``breaches``, ``breach_rate``,
        ``expected_rate``.
    """
    total = len(df)
    breaches = int(df["Breach"].sum())
    breach_rate = breaches / total
    expected_rate = 1.0 - confidence

    return {
        "total_observations": total,
        "breaches": breaches,
        "breach_rate": round(breach_rate, 4),
        "expected_rate": round(expected_rate, 4),
    }


def rolling_decay_var(
    returns: pd.Series,
    window: int = 252,
    lam: float = 0.94,
    confidence: float = 0.95,
) -> pd.DataFrame:
    """
    Compute rolling out-of-sample exponentially-weighted VaR.

    Same out-of-sample structure as ``rolling_var``, but each window
    uses decay weighting (λ) rather than equal weighting. Recent
    returns get more influence; old returns fade smoothly.

    Parameters
    ----------
    returns : pd.Series
        Daily percentage returns with a DatetimeIndex.
    window : int, default 252
        Look-back window in trading days.
    lam : float, default 0.94
        Decay factor. 0.94 means each day further back loses 6% weight.
        λ=1.0 recovers equal-weighted VaR.
    confidence : float, default 0.95
        Confidence level for VaR.

    Returns
    -------
    pd.DataFrame
        Same columns as ``rolling_var``: VaR, NextReturn, Breach.
    """
    if len(returns) < window + 1:
        raise ValueError(
            f"Need at least {window + 1} observations for a {window}-day "
            f"rolling VaR. Got {len(returns)}."
        )

    var_values = []
    next_returns = []
    breaches = []
    dates = []

    for day in range(window, len(returns)):
        window_returns = returns.iloc[day - window : day]
        # decay_var expects newest first — iloc gives oldest first, so reverse
        var = decay_var(window_returns[::-1], lam=lam, confidence=confidence)

        next_return = returns.iloc[day]
        breach = -next_return > var

        dates.append(returns.index[day])
        var_values.append(var)
        next_returns.append(next_return)
        breaches.append(breach)

    return pd.DataFrame(
        {
            "VaR": var_values,
            "NextReturn": next_returns,
            "Breach": breaches,
        },
        index=pd.DatetimeIndex(dates, name="Date"),
    )