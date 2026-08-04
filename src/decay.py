"""
Exponentially-weighted historical VaR.

The core primitive is ``weighted_quantile`` — a quantile function that
accepts per-element weights. ``decay_var`` builds on it to compute VaR
with exponential decay weighting (λ), giving more influence to recent
returns and less to older ones. This mitigates the regime-change lag
of equal-weighted historical VaR.
"""

import numpy as np


def weighted_quantile(
    values,
    weights,
    q: float,
) -> float:
    """
    Compute the q-th quantile of values with per-element weights.

    Sorts values, reorders weights to match, computes cumulative
    normalised weights, and linearly interpolates at quantile ``q``.

    Parameters
    ----------
    values : array-like
        Observations (e.g. returns). Any order — the function sorts.
    weights : array-like
        Non-negative weights, same length as values. Need not sum to 1.
    q : float
        Quantile in [0, 1]. For VaR at 95% confidence, q = 0.05.

    Returns
    -------
    float
        The weighted q-th quantile, linearly interpolated.
    """
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)

    if len(values) == 0:
        raise ValueError("Cannot compute quantile from empty array.")
    if len(values) != len(weights):
        raise ValueError(
            f"values and weights must have the same length. "
            f"Got {len(values)} and {len(weights)}."
        )
    if np.any(weights < 0):
        raise ValueError("Weights must be non-negative.")
    if not (0 <= q <= 1):
        raise ValueError(f"q must be in [0, 1], got {q}.")
    if np.all(weights == 0):
        raise ValueError("All weights are zero.")

    # Sort by value
    order = np.argsort(values)
    values = values[order]
    weights = weights[order]

    # Cumulative normalised weights
    cum = np.cumsum(weights)
    cum = cum / cum[-1]

    # Find where cumulative crosses q
    idx = np.searchsorted(cum, q)

    if idx == 0:
        return float(values[0])
    if idx >= len(values):
        return float(values[-1])

    # Linear interpolation between bracketing values
    t = (q - cum[idx - 1]) / (cum[idx] - cum[idx - 1])
    return float(values[idx - 1] + t * (values[idx] - values[idx - 1]))


def decay_var(
    returns,
    lam: float = 0.94,
    confidence: float = 0.95,
    position_value: float | None = None,
) -> float:
    """
    Compute exponentially-weighted historical VaR.

    Each return is weighted by λ^age, where age = 0 for the most
    recent return and n-1 for the oldest. Recent returns dominate;
    old returns fade smoothly to near-zero weight.

    Parameters
    ----------
    returns : array-like
        Decimal returns. Most recent first (index 0 = yesterday).
        Any order is fine — weights are assigned based on the
        order the caller provides (newest first).
    lam : float, default 0.94
        Decay factor. 0.94 means each day further back loses 6% weight.
        λ=1.0 recovers equal-weighted VaR.
    confidence : float, default 0.95
        Confidence level.
    position_value : float, optional
        If provided, returns VaR in currency.

    Returns
    -------
    float
        VaR as a positive decimal (or currency).

    Raises
    ------
    ValueError
        If returns is empty, lam is outside (0, 1], or confidence
        is outside (0, 1).
    """
    returns = np.asarray(returns, dtype=float)

    if returns.size == 0:
        raise ValueError("Cannot compute VaR from an empty return series.")
    if np.any(np.isnan(returns)):
        raise ValueError("Return series contains NaN values.")
    if not (0 < lam <= 1):
        raise ValueError(f"lam must be in (0, 1], got {lam}.")
    if not (0 < confidence < 1):
        raise ValueError(f"Confidence must be between 0 and 1, got {confidence}.")

    n = len(returns)

    # Weights: newest first (index 0) gets weight 1, oldest gets lam^(n-1)
    weights = lam ** np.arange(n, dtype=float)

    tail_q = 1.0 - confidence
    q = weighted_quantile(returns, weights, tail_q)

    var_pct = -q
    if position_value is not None:
        return float(var_pct * position_value)
    return float(var_pct)
