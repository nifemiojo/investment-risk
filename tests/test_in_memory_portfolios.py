import unittest

from src.domain.mandate import Mandate
from src.domain.portfolio import Portfolio
from src.infrastructure.in_memory_portfolios import InMemoryPortfolioRepository


class InMemoryPortfolioRepositoryTests(unittest.TestCase):
    def test_default_repository_still_provides_the_default_portfolio(self):
        repository = InMemoryPortfolioRepository()

        portfolio = repository.get("60/40 Multi-Asset")

        self.assertEqual(portfolio.name, "60/40 Multi-Asset")
        self.assertEqual(portfolio.assets, {"SPY": 0.40, "EFA": 0.20, "IEF": 0.25, "GLD": 0.15})

    def test_repository_returns_a_supplied_portfolio(self):
        supplied = Portfolio(
            name="2021 Case Study",
            assets={"SPY": 0.50, "IEF": 0.50},
            nav=1_000_000,
            risk_budget_annual_pct=0.20,
            mandate=Mandate({"SPY": 0.60, "IEF": 0.40}),
        )

        repository = InMemoryPortfolioRepository(
            portfolios={supplied.name: supplied}
        )

        self.assertIs(repository.get("2021 Case Study"), supplied)

    def test_supplied_portfolios_replace_the_default_mapping(self):
        supplied = Portfolio(
            name="2021 Case Study",
            assets={"SPY": 0.50, "IEF": 0.50},
            nav=1_000_000,
            risk_budget_annual_pct=0.20,
            mandate=Mandate({"SPY": 0.60, "IEF": 0.40}),
        )

        repository = InMemoryPortfolioRepository(
            portfolios={supplied.name: supplied}
        )

        with self.assertRaises(KeyError):
            repository.get("60/40 Multi-Asset")

    def test_unknown_portfolio_still_raises_key_error(self):
        with self.assertRaisesRegex(KeyError, "Missing"):
            InMemoryPortfolioRepository().get("Missing")


if __name__ == "__main__":
    unittest.main()
