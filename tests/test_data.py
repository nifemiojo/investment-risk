"""
Integration tests: yfinance_helpers → historical_var chain.
"""

import pytest


class TestVaRChain:

    @pytest.mark.integration
    def test_spy_full_chain(self):
        from yfinance_helpers import download_close_prices, prepare_returns
        from src.historical_var import historical_var

        prices = download_close_prices("SPY", start="2023-01-01", end="2024-12-31")
        returns = prepare_returns(prices)

        var_95 = historical_var(returns, confidence=0.95)
        var_99 = historical_var(returns, confidence=0.99)

        assert 0.005 < var_95 < 0.05
        assert 0.005 < var_99 < 0.08
        assert var_99 > var_95
