from src.domain.portfolio import Portfolio


class InMemoryPortfolioRepository:
    """V0.3: hardcoded portfolio lookup. Later: file or database."""

    def __init__(self):
        self._portfolios = {
            "60/40 Multi-Asset": Portfolio(
                name="60/40 Multi-Asset",
                assets={'SPY': 0.40, 'EFA': 0.20, 'IEF': 0.25, 'GLD': 0.15},
                nav=10_000_000,
                risk_budget_annual_pct=0.30,
            ),
        }

    def get(self, name: str) -> Portfolio:
        if name not in self._portfolios:
            raise KeyError(f"Portfolio '{name}' not found.")
        return self._portfolios[name]