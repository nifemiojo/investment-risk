from collections.abc import Mapping

from src.domain.mandate import Mandate
from src.domain.portfolio import Portfolio


def _default_portfolios() -> dict[str, Portfolio]:
    """Build the portfolio definitions used by the default application path."""
    return {
        "60/40 Multi-Asset": Portfolio(
            name="60/40 Multi-Asset",
            assets={"SPY": 0.40, "EFA": 0.20, "IEF": 0.25, "GLD": 0.15},
            nav=10_000_000,
            risk_budget_annual_pct=0.30,
            mandate=Mandate(
                risk_budget_by_asset={
                    "SPY": 0.45,
                    "EFA": 0.20,
                    "IEF": 0.20,
                    "GLD": 0.15,
                }
            ),
        ),
    }


class InMemoryPortfolioRepository:
    """Name-based in-memory portfolio lookup.

    When no portfolios are supplied, the repository preserves the default
    hardcoded portfolio used by the original application path. Callers can
    instead provide their own name-to-portfolio mapping at composition time.
    """

    def __init__(self, portfolios: Mapping[str, Portfolio] | None = None):
        self._portfolios = dict(_default_portfolios() if portfolios is None else portfolios)

    def get(self, name: str) -> Portfolio:
        if name not in self._portfolios:
            raise KeyError(f"Portfolio '{name}' not found.")
        return self._portfolios[name]