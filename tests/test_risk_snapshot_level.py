"""
Tests for the "Is This Normal?" section — percentile_meaning bands and
distribution_lookback_start capture.

The percentile_meaning field replaces the old level_label. It maps today's
VaR percentile rank (within the portfolio's own history) to a prose
interpretation carrying both the level and the action cue.
"""

import numpy as np
import pandas as pd
import pytest

from src.domain.portfolio import Portfolio
from src.engine.risk_snapshot_engine import RiskSnapshotEngine
from src.display.snapshot_renderer import _ordinal, _format_lookback


# ── percentile_meaning bands ───────────────────────────────────

class TestPercentileMeaningBands:
    """The five bands, pinned at their boundaries (>= semantics)."""

    @pytest.mark.parametrize(
        ("percentile", "expected"),
        [
            (0.00, "lighter than usual for this portfolio"),
            (0.49, "lighter than usual for this portfolio"),
            (0.50, "about average for this portfolio"),
            (0.79, "about average for this portfolio"),
            (0.80, "notably above this portfolio's norm, worth a look"),
            (0.89, "notably above this portfolio's norm, worth a look"),
            (0.90, "unusually high for this portfolio, investigate"),
            (0.94, "unusually high for this portfolio, investigate"),
            (0.95, "far beyond this portfolio's norm, escalate"),
            (1.00, "far beyond this portfolio's norm, escalate"),
        ],
    )
    def test_band(self, percentile, expected):
        assert RiskSnapshotEngine._percentile_meaning(percentile) == expected

    def test_53rd_percentile_is_about_average(self):
        """The motivating case: 53% is at the median, not 'above typical'."""
        assert (
            RiskSnapshotEngine._percentile_meaning(0.53)
            == "about average for this portfolio"
        )


# ── decision (investigate / no action) ─────────────────────────

class TestDecide:
    """The snapshot's single routing decision."""

    @pytest.mark.parametrize(
        ("is_breach", "percentile", "expected"),
        [
            (False, 0.20, "no action"),
            (False, 0.50, "no action"),
            (False, 0.80, "no action"),
            (False, 0.81, "investigate"),
            (False, 0.95, "investigate"),
            (True, 0.20, "investigate"),
            (True, 0.95, "investigate"),
        ],
    )
    def test_decide(self, is_breach, percentile, expected):
        assert RiskSnapshotEngine._decide(is_breach, percentile) == expected

    def test_breach_triggers_investigate_even_at_low_percentile(self):
        """A breach overrides the percentile — it's still 'investigate'."""
        assert RiskSnapshotEngine._decide(True, 0.20) == "investigate"


# ── distribution_lookback_start capture ────────────────────────

class _FakeReturnsProvider:
    """Returns a fixed synthetic DataFrame (dates × tickers)."""

    def __init__(self, returns: pd.DataFrame):
        self._returns = returns

    def load(self, tickers, start, end):
        return self._returns


def _make_returns(n_days: int, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2019-01-02", periods=n_days)
    return pd.DataFrame(
        {"SPY": rng.normal(0.0004, 0.01, n_days)},
        index=dates,
    )


def test_distribution_lookback_start_captured():
    """lookback_start == first date with a valid rolling VaR (window=5)."""
    n_days = 20
    portfolio = Portfolio(
        name="Test",
        assets={"SPY": 1.0},
        nav=1_000_000,
        risk_budget_annual_pct=0.15,
    )

    class _Repo:
        def get(self, name):
            return portfolio

    returns = _make_returns(n_days)
    engine = RiskSnapshotEngine(
        _Repo(),
        _FakeReturnsProvider(returns),
        var_window=5,
    )

    snapshot = engine.snapshot("Test", date=returns.index[-1].date().isoformat())

    # rolling_var(window=5) produces its first value at index 5
    expected_start = returns.index[5].date().isoformat()
    assert snapshot.distribution_lookback_start == expected_start


# ── renderer helpers ───────────────────────────────────────────

class TestOrdinal:
    @pytest.mark.parametrize(
        ("rank", "expected"),
        [
            (0.01, "1st"),
            (0.02, "2nd"),
            (0.03, "3rd"),
            (0.11, "11th"),
            (0.21, "21st"),
            (0.22, "22nd"),
            (0.23, "23rd"),
            (0.53, "53rd"),
            (0.99, "99th"),
        ],
    )
    def test_ordinal(self, rank, expected):
        assert _ordinal(rank) == expected


class TestFormatLookback:
    def test_jan_2019(self):
        assert _format_lookback("2019-01-02") == "Jan 2019"

    def test_dec_2021(self):
        assert _format_lookback("2021-12-15") == "Dec 2021"
