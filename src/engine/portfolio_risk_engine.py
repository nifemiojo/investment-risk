import calendar
from datetime import date as date_type

from src.boundaries.portfolio_repository import PortfolioRepository
from src.boundaries.returns_provider import ReturnsProvider
from src.domain.portfolio_risk import PortfolioRisk, VolatilityObservation
from src.portfolio_volatility import calculate_rolling_portfolio_volatility


class PortfolioRiskEngine:
    """Produce current and rolling portfolio-level volatility evidence."""

    def __init__(
        self,
        portfolios: PortfolioRepository,
        returns_provider: ReturnsProvider,
    ):
        self._portfolios = portfolios
        self._returns_provider = returns_provider

    def calculate(
        self,
        portfolio_name: str,
        date: str,
        *,
        estimation_window: int,
        display_window: int,
    ) -> PortfolioRisk:
        """Calculate current and trailing daily portfolio volatility."""
        portfolio = self._portfolios.get(portfolio_name)
        asset_returns = self._returns_provider.load(
            portfolio.tickers,
            start="2018-01-01",
            end=date,
        )
        aligned_returns = asset_returns[portfolio.tickers].dropna()
        portfolio_returns = portfolio.returns(aligned_returns)
        volatility_history = calculate_rolling_portfolio_volatility(
            portfolio_returns,
            estimation_window=estimation_window,
            display_window=display_window,
        )

        observations = tuple(
            VolatilityObservation(
                date=observation_date.isoformat(),
                volatility=float(volatility),
            )
            for observation_date, volatility in volatility_history.items()
        )
        current_observation_date = volatility_history.index[-1]
        month = current_observation_date.month - 1
        year = current_observation_date.year
        if month == 0:
            month = 12
            year -= 1
        month_ago_date = date_type(
            year,
            month,
            min(current_observation_date.day, calendar.monthrange(year, month)[1]),
        )
        month_ago_candidates = volatility_history[
            volatility_history.index.date <= month_ago_date
        ]
        if month_ago_candidates.empty:
            previous_month_volatility = None
            previous_month_observation_date = None
        else:
            previous_month_volatility = float(month_ago_candidates.iloc[-1])
            previous_month_observation_date = month_ago_candidates.index[-1].isoformat()

        return PortfolioRisk(
            current_volatility=float(volatility_history.iloc[-1]),
            volatility_history=observations,
            previous_month_volatility=previous_month_volatility,
            previous_month_observation_date=previous_month_observation_date,
        )


__all__ = ["PortfolioRiskEngine"]
