"""
Tests for rolling_var — out-of-sample correctness and window cliff behaviour.
"""

import pytest
import pandas as pd
import numpy as np
from src.rolling import rolling_var, breach_summary


# ── Fixtures ──────────────────────────────────────────────────

@pytest.fixture
def flat_returns():
    """100 days of zero returns — VaR should be zero."""
    dates = pd.date_range("2024-01-01", periods=100, freq="B")
    return pd.Series(np.zeros(100), index=dates)


@pytest.fixture
def synthetic_returns():
    """
    Synthetic series with a known large loss at a specific position.

    500 days of 0% returns, with a single -10% day at index 100.
    """
    dates = pd.date_range("2020-01-01", periods=500, freq="B")
    data = np.zeros(500)
    data[100] = -0.10  # single large loss
    return pd.Series(data, index=dates)


# ── Core behaviour ────────────────────────────────────────────

class TestRollingVar:
    """Out-of-sample correctness."""

    def test_first_estimate_after_window(self, flat_returns):
        """No VaR estimate before the window has been filled."""
        result = rolling_var(flat_returns, window=20)
        # 100 returns, window=20 → first estimate at index 20 (the 21st day)
        assert result.index[0] == flat_returns.index[20]

    def test_output_length(self, flat_returns):
        """n returns, window w → n - w rows."""
        result = rolling_var(flat_returns, window=20)
        assert len(result) == len(flat_returns) - 20

    def test_insufficient_data_raises(self, flat_returns):
        """Need at least window + 1 returns."""
        with pytest.raises(ValueError, match="Need at least"):
            rolling_var(flat_returns.iloc[:10], window=20)

    def test_no_lookahead_bias(self, synthetic_returns):
        """
        The large loss at index 100 must NOT appear in the VaR
        estimate for day 100 itself. It should only affect VaR
        from day 101 onward.
        """
        result = rolling_var(synthetic_returns, window=50, confidence=0.99)

        # Day 100's VaR uses returns[50:100] — all zeros → VaR = 0
        var_at_loss_day = result.loc[synthetic_returns.index[100], "VaR"]
        assert var_at_loss_day == pytest.approx(0.0, abs=1e-10)

        # Day 101's VaR uses returns[51:101] — includes the -10% → VaR > 0
        var_after_loss_day = result.loc[synthetic_returns.index[101], "VaR"]
        assert var_after_loss_day > 0


class TestWindowCliff:
    """The -10% day entering and exiting the window."""

    def test_loss_enters_window(self, synthetic_returns):
        """
        Day 100: -10% loss. Window=50.
        Day 100: VaR uses days 50-99 (all zeros) → VaR = 0.
        Day 101: VaR uses days 51-100 (includes -10%) → VaR > 0.
        Day 150: VaR uses days 100-149 (includes -10%) → VaR still > 0.
        Day 151: VaR uses days 101-150 (all zeros) → VaR = 0.
        """
        result = rolling_var(synthetic_returns, window=50, confidence=0.99)

        # Before loss enters window
        assert result.loc[synthetic_returns.index[100], "VaR"] == pytest.approx(0.0, abs=1e-10)

        # After loss enters window
        assert result.loc[synthetic_returns.index[101], "VaR"] > 0

        # Loss still in window
        assert result.loc[synthetic_returns.index[149], "VaR"] > 0

    def test_loss_exits_window(self, synthetic_returns):
        """
        The -10% at index 100 exits the 50-day window at day 151.
        Day 150: VaR uses days 100-149 (includes -10%) → VaR > 0.
        Day 151: VaR uses days 101-150 (all zeros) → VaR = 0.
        """
        result = rolling_var(synthetic_returns, window=50, confidence=0.99)

        # Last day with loss in window
        assert result.loc[synthetic_returns.index[150], "VaR"] > 0

        # Loss exits — VaR drops back to zero
        assert result.loc[synthetic_returns.index[151], "VaR"] == pytest.approx(0.0, abs=1e-10)


class TestBreachFlagging:
    """Breach detection logic."""

    def test_no_breaches_on_flat_returns(self, flat_returns):
        """Zero returns everywhere → no breaches at any confidence."""
        result = rolling_var(flat_returns, window=20, confidence=0.95)
        assert not result["Breach"].any()

    def test_breach_detected(self, synthetic_returns):
        """The -10% day should be flagged as a breach."""
        result = rolling_var(synthetic_returns, window=50, confidence=0.95)
        # Day 100 has VaR = 0 (from all-zero window), actual return = -10%
        # Loss = 10% > VaR = 0% → breach
        assert result.loc[synthetic_returns.index[100], "Breach"] == True

    def test_breach_columns_match(self, synthetic_returns):
        """Breach should be True exactly when -NextReturn > VaR."""
        result = rolling_var(synthetic_returns, window=50, confidence=0.95)
        manual = (-result["NextReturn"]) > result["VaR"]
        assert (result["Breach"] == manual).all()


class TestBreachSummary:
    """breach_summary reporting."""

    def test_all_zero_returns(self, flat_returns):
        result = rolling_var(flat_returns, window=20, confidence=0.95)
        summary = breach_summary(result, confidence=0.95)
        assert summary["breaches"] == 0
        assert summary["breach_rate"] == 0.0
        assert summary["expected_rate"] == 0.05

    def test_expected_rate_reflects_confidence(self):
        dates = pd.date_range("2024-01-01", periods=300, freq="B")
        returns = pd.Series(np.random.randn(300) * 0.01, index=dates)
        result = rolling_var(returns, window=50, confidence=0.99)
        summary = breach_summary(result, confidence=0.99)
        assert summary["expected_rate"] == 0.01


# ── Rolling decay-weighted VaR ────────────────────────────────

class TestRollingDecayVar:
    """Out-of-sample behaviour matches equal-weighted."""

    def test_same_no_lookahead(self, synthetic_returns):
        """Decay version also excludes current day."""
        from src.rolling import rolling_decay_var

        result = rolling_decay_var(synthetic_returns, window=50, lam=0.94, confidence=0.99)
        # Day 100's VaR uses returns[50:100] — all zeros
        assert result.loc[synthetic_returns.index[100], "VaR"] == pytest.approx(0.0, abs=1e-10)

    def test_decay_reacts_faster_than_equal(self, synthetic_returns):
        """
        After the -10% loss enters, decay VaR should be higher than
        equal-weighted because it gives the recent loss more weight.
        """
        from src.rolling import rolling_decay_var

        result_eq = rolling_var(synthetic_returns, window=50, confidence=0.99)
        result_dc = rolling_decay_var(synthetic_returns, window=50, lam=0.94, confidence=0.99)

        # Day after loss enters: decay should react more strongly
        var_eq = result_eq.loc[synthetic_returns.index[101], "VaR"]
        var_dc = result_dc.loc[synthetic_returns.index[101], "VaR"]
        assert var_dc >= var_eq  # decay at least as high

    def test_lam_one_equals_equal_weighted(self, synthetic_returns):
        """λ=1.0 → same as rolling_var."""
        from src.rolling import rolling_decay_var

        result_eq = rolling_var(synthetic_returns, window=50, confidence=0.95)
        result_dc = rolling_decay_var(synthetic_returns, window=50, lam=1.0, confidence=0.95)

        # Should be close (weighted_quantile vs np.quantile differ slightly)
        assert result_dc["VaR"].mean() == pytest.approx(result_eq["VaR"].mean(), rel=0.01)