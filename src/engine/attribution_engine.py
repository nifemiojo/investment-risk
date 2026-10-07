import pandas as pd

from src.attribution_calculation import calculate_component_contributions
from src.boundaries.portfolio_repository import PortfolioRepository
from src.boundaries.returns_provider import ReturnsProvider
from src.domain.attribution import Attribution, RiskContribution


class AttributionEngine:
    """Produce covariance-based structural risk attribution evidence."""

    def __init__(
        self,
        portfolios: PortfolioRepository,
        returns_provider: ReturnsProvider,
    ):
        self._portfolios = portfolios
        self._returns_provider = returns_provider

    def attribute(
        self,
        portfolio_name: str,
        date: str,
        estimation_window: int,
        portfolio_override=None,
    ) -> Attribution:
        """Calculate ranked asset contributions for a named portfolio."""
        portfolio = portfolio_override or self._portfolios.get(portfolio_name)
        asset_returns = self._returns_provider.load(
            portfolio.tickers,
            start="2018-01-01",
            end=date,
        )
        aligned_returns = asset_returns[portfolio.tickers].dropna()
        available_dates = pd.DatetimeIndex(aligned_returns.index)
        eligible_dates = available_dates[available_dates <= pd.Timestamp(date)]
        if len(eligible_dates) == 0:
            raise ValueError(f"No available close on or before {date}.")
        resolved_date = eligible_dates[-1]
        calculation = calculate_component_contributions(
            aligned_returns.tail(estimation_window),
            [portfolio.assets[asset] for asset in portfolio.tickers],
        )

        contribution_by_asset = dict(
            zip(portfolio.tickers, calculation.risk_contribution_pct)
        )
        ranked_assets = sorted(
            portfolio.tickers,
            key=lambda asset: contribution_by_asset[asset],
            reverse=True,
        )

        cumulative_contribution = 0.0
        contributions = []
        for asset in ranked_assets:
            contribution_pct = contribution_by_asset[asset]
            cumulative_contribution += contribution_pct
            contributions.append(
                RiskContribution(
                    asset=asset,
                    weight=portfolio.assets[asset],
                    risk_contribution_pct=contribution_pct,
                    cumulative_risk_contribution_pct=cumulative_contribution,
                )
            )

        return Attribution(
            portfolio_volatility=calculation.portfolio_volatility,
            risk_contributions=tuple(contributions),
            observation_date=resolved_date.date().isoformat(),
        )

    def attribute_portfolio(
        self,
        portfolio,
        date: str,
        estimation_window: int,
    ) -> Attribution:
        """Calculate attribution for a supplied hypothetical portfolio."""
        return self.attribute(
            portfolio.name,
            date,
            estimation_window,
            portfolio_override=portfolio,
        )
