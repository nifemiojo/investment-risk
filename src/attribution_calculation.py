from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ComponentContributionResult:
    """Computed portfolio volatility and signed percentage contributions."""

    portfolio_volatility: float
    risk_contribution_pct: tuple[float, ...]


def calculate_component_contributions(
    returns,
    weights,
) -> ComponentContributionResult:
    """Calculate covariance-based component contributions to portfolio volatility.

    Parameters
    ----------
    returns : array-like
        Daily decimal asset returns with observations in rows and assets in
        columns.
    weights : array-like
        Portfolio weights in the same asset order as the return columns.

    Returns
    -------
    ComponentContributionResult
        Portfolio volatility and signed percentage contributions. The returned
        result does not expose covariance or volatility-unit intermediates.
    """
    returns = np.asarray(returns, dtype=float)
    weights = np.asarray(weights, dtype=float)

    if returns.ndim != 2:
        raise ValueError("Returns must be a two-dimensional observation matrix.")
    if weights.ndim != 1 or weights.size != returns.shape[1]:
        raise ValueError("Weights must contain one value for each return column.")

    covariance_matrix = np.cov(returns, rowvar=False)
    covariance_matrix = np.atleast_2d(covariance_matrix)
    portfolio_variance = weights @ covariance_matrix @ weights
    portfolio_volatility = float(np.sqrt(portfolio_variance))

    if portfolio_volatility == 0.0:
        raise ValueError("Portfolio volatility must be positive.")

    covariance_with_portfolio = covariance_matrix @ weights
    risk_contribution_pct = (
        weights * covariance_with_portfolio / portfolio_variance
    )

    return ComponentContributionResult(
        portfolio_volatility=portfolio_volatility,
        risk_contribution_pct=tuple(
            float(contribution) for contribution in risk_contribution_pct
        ),
    )


__all__ = [
    "ComponentContributionResult",
    "calculate_component_contributions",
]

