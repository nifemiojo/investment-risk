from typing import Protocol

from src.domain.portfolio import Portfolio


class PortfolioRepository(Protocol):
    """Source of portfolio definitions for application services."""

    def get(self, portfolio_name: str) -> Portfolio:
        ...
