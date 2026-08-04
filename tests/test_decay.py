"""
Tests for decay-weighted historical VaR — weighted_quantile and decay_var.
"""

import pytest
import numpy as np
from src.decay import weighted_quantile, decay_var
from src.historical_var import historical_var


# ── weighted_quantile tests ───────────────────────────────────

class TestWeightedQuantile:
    """
    Note: weighted_quantile uses cumulative normalised weights to find
    the quantile. When q is less than the weight of the smallest value,
    it returns the smallest value (no data below to interpolate against).
    This is a "lower-like" convention, not numpy's "linear" method which
    uses an equal-weight-specific index formula.
    """

    def test_uniform_weights(self):
        """
        Equal weights → cumulative has n equal steps.
        q=0.05 < 1/10=0.1 → returns smallest value (-5%).
        """
        values = [-0.05, -0.03, -0.02, -0.01, 0.00, 0.01, 0.02, 0.03, 0.04, 0.05]
        weights = np.ones(len(values))
        result = weighted_quantile(values, weights, 0.05)
        # q=0.05 falls inside the first weight block → smallest value
        assert result == pytest.approx(-0.05)

    def test_single_value(self):
        assert weighted_quantile([0.03], [1.0], 0.05) == pytest.approx(0.03)
        assert weighted_quantile([0.03], [1.0], 0.95) == pytest.approx(0.03)

    def test_dominant_weight(self):
        values = [-0.10, 0.01, 0.02, 0.03, 0.04, 0.05]
        weights = [99.0, 0.25, 0.25, 0.25, 0.25, 0.0]
        result = weighted_quantile(values, weights, 0.05)
        assert result == pytest.approx(-0.10, abs=1e-4)

    def test_interpolation_between_weights(self):
        """q=0.75 with two equal weights → interpolate between the two."""
        values = [-0.05, 0.05]
        weights = [1.0, 1.0]
        # Cumulative: 0.5 at -5%, 1.0 at 5%. q=0.75 → between them
        result = weighted_quantile(values, weights, 0.75)
        # 50% of the way from -5% to 5%: 0%
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_q_at_boundaries(self):
        values = [-0.05, -0.03, -0.02, -0.01, 0.00]
        weights = np.ones(5)
        assert weighted_quantile(values, weights, 0.0) == pytest.approx(-0.05)
        assert weighted_quantile(values, weights, 1.0) == pytest.approx(0.00)

    def test_weights_sorted_correctly(self):
        """Weights must follow values during sorting."""
        values = [0.05, -0.05, 0.01, -0.01, 0.00]
        weights = [0.1, 0.5, 0.1, 0.2, 0.1]
        # Sorted: -5%(0.5), -1%(0.2), 0%(0.1), 1%(0.1), 5%(0.1)
        # Cum: 0.5, 0.7, 0.8, 0.9, 1.0
        # q=0.05 < 0.5 → -5%
        result = weighted_quantile(values, weights, 0.05)
        assert result == pytest.approx(-0.05)
        # q=0.6 → between -5% (0.5) and -1% (0.7)
        result2 = weighted_quantile(values, weights, 0.6)
        assert result2 == pytest.approx(-0.03)  # halfway = -3%


# ── Validation ────────────────────────────────────────────────

class TestWeightedQuantileValidation:

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="empty"):
            weighted_quantile([], [], 0.05)

    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError, match="same length"):
            weighted_quantile([1.0, 2.0], [1.0], 0.05)

    def test_negative_weights_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            weighted_quantile([1.0, 2.0], [1.0, -0.5], 0.05)

    def test_all_zero_weights_raises(self):
        with pytest.raises(ValueError, match="zero"):
            weighted_quantile([1.0, 2.0], [0.0, 0.0], 0.05)

    def test_q_out_of_range_raises(self):
        with pytest.raises(ValueError, match="0, 1"):
            weighted_quantile([1.0, 2.0], [1.0, 1.0], 1.5)


# ── decay_var tests ───────────────────────────────────────────

class TestDecayVar:
    """
    Note: decay_var uses weighted_quantile internally. Even with
    λ=1.0 (equal weights), the result differs slightly from
    historical_var's np.quantile because weighted_quantile uses
    cumulative weights rather than numpy's (n-1) index formula.
    The difference is a fraction of one observation's weight.
    """

    def test_lam_one_approximates_equal_weighted(self):
        """λ=1.0 → uniform weights → close to historical_var."""
        returns = [-0.05, -0.03, -0.02, -0.01, 0.00, 0.01, 0.02, 0.03, 0.04, 0.05]
        result = decay_var(returns, lam=1.0, confidence=0.95)
        # With 10 equal weights, q=0.05 < 0.1 → returns -5% → VaR = 5%
        assert result == pytest.approx(0.05)

    def test_decay_gives_recent_more_weight(self):
        """
        Recent negative returns should dominate over older positive ones.
        Put a large negative return first (newest) → decay VaR > equal VaR.
        """
        # -10% yesterday, then mostly +2% for 99 days
        returns = [-0.10] + [0.02] * 99
        # With λ=0.94, yesterday gets weight 1.0, day 99 gets lam^99 ≈ 0.002
        # The -10% dominates → quantile near -10% → VaR near 10%
        result = decay_var(returns, lam=0.94, confidence=0.95)
        # The -10% has significant weight → VaR should be substantial
        assert result > 0.05  # well above equal-weighted

    def test_low_lam_favours_recent_extreme(self):
        """λ near 0 → only the most recent return matters."""
        returns = [-0.05, -0.03, 0.01, 0.02, 0.04]  # newest first
        result = decay_var(returns, lam=1e-10, confidence=0.95)
        # Most recent (index 0) = -5% gets weight 1.0, others ~0
        assert result == pytest.approx(0.05)

    def test_position_scaling(self):
        returns = [-0.05, -0.03, -0.02, -0.01, 0.00, 0.01, 0.02, 0.03, 0.04, 0.05]
        var_pct = decay_var(returns, lam=0.94, confidence=0.95)
        var_gbp = decay_var(returns, lam=0.94, confidence=0.95, position_value=1_000_000)
        assert var_gbp == pytest.approx(var_pct * 1_000_000)

    def test_positive_sign_convention(self):
        returns = [-0.05, -0.03, -0.02, -0.01, 0.01, 0.02]
        result = decay_var(returns, lam=0.94, confidence=0.95)
        assert result >= 0


# ── Validation ────────────────────────────────────────────────

class TestDecayVarValidation:

    def test_empty_returns_raises(self):
        with pytest.raises(ValueError, match="empty"):
            decay_var([])

    def test_nan_raises(self):
        with pytest.raises(ValueError, match="NaN"):
            decay_var([0.01, np.nan])

    def test_lam_zero_raises(self):
        with pytest.raises(ValueError, match="lam"):
            decay_var([0.01, -0.01], lam=0)

    def test_lam_above_one_raises(self):
        with pytest.raises(ValueError, match="lam"):
            decay_var([0.01, -0.01], lam=1.5)

    def test_confidence_out_of_range_raises(self):
        with pytest.raises(ValueError, match="Confidence"):
            decay_var([0.01, -0.01], confidence=0)
