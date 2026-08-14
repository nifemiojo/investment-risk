import numpy as np

from src.domain.risk_snapshot import RiskSnapshot
from src.rolling import rolling_var
from src.historical_var import historical_var


class RiskSnapshotEngine:
    """
    Produces RiskSnapshot dataclasses.

    V0.3: real VaR computation from market data.
    The engine resolves portfolio attributes internally;
    the caller only supplies portfolio_name and date.
    """

    def __init__(
        self,
        portfolios,
        returns_provider,
        var_window: int = 252,
        var_confidence: float = 0.95,
        calculator=None,
    ):
        self.portfolios = portfolios
        self.returns_provider = returns_provider
        self.var_window = var_window
        self.var_confidence = var_confidence
        self.calculator = calculator  # unused in V0.3, wired for future IoC

    def snapshot(
        self,
        portfolio_name: str,
        date: str,
    ) -> RiskSnapshot:
        """
        Produce a Risk Snapshot.

        The caller supplies what a PM thinks in: a portfolio name and a date.
        Everything else is resolved internally.
        """
        portfolio = self.portfolios.get(portfolio_name)

        # 1. Load returns up to the requested date
        asset_returns = self.returns_provider.load(
            portfolio.tickers,
            start="2018-01-01",
            end=date,
        )

        # 2. Compute portfolio returns
        portfolio_returns = portfolio.returns(asset_returns)

        # 3. Compute VaR (historical_var extracts the window internally)
        var_pct = historical_var(
            portfolio_returns.values,
            confidence=self.var_confidence,
            window=self.var_window,
        )

        # 4. Compute percentile rank from rolling VaR history
        var_history = rolling_var(
            portfolio_returns,
            window=self.var_window,
            confidence=self.var_confidence,
        )
        historical_vars = var_history["VaR"].dropna()

        percentile_rank = (historical_vars < var_pct).mean()
        distribution_lookback_start = historical_vars.index[0].date().isoformat()
        percentile_meaning = self._percentile_meaning(percentile_rank)

        # 5. Annualise VaR and compare to budget
        annualised_var = var_pct * np.sqrt(252)
        budget_utilisation = annualised_var / portfolio.risk_budget_annual_pct
        is_breach = budget_utilisation >= 1.0

        # 6. Decision
        decision = self._decide(is_breach, percentile_rank)

        return RiskSnapshot(
            portfolio_name=portfolio.name,
            timestamp=date,
            var_currency=var_pct * portfolio.nav,
            var_pct=var_pct,
            var_annualised_pct=annualised_var,
            nav=portfolio.nav,
            risk_budget_annual_pct=portfolio.risk_budget_annual_pct,
            budget_utilisation=budget_utilisation,
            is_breach=is_breach,
            percentile_rank=percentile_rank,
            percentile_meaning=percentile_meaning,
            distribution_lookback_start=distribution_lookback_start,
            decision=decision,
        )

    # ── Internal helpers ──

    @staticmethod
    def _percentile_meaning(percentile_rank: float) -> str:
        if percentile_rank >= 0.95:
            return "far beyond this portfolio's norm, escalate"
        if percentile_rank >= 0.90:
            return "unusually high for this portfolio, investigate"
        if percentile_rank >= 0.80:
            return "notably above this portfolio's norm, worth a look"
        if percentile_rank >= 0.50:
            return "about average for this portfolio"
        return "lighter than usual for this portfolio"

    @staticmethod
    def _decide(is_breach: bool, percentile_rank: float) -> str:
        if is_breach or percentile_rank > 0.80:
            return "investigate"
        return "no action"