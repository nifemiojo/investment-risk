# 008 — Why Covariance Can't Be Compared Across Pairs: Scale Contamination

**Date:** 2026-07-22
**Topic:** How the units and scale of individual assets poison covariance as a comparison tool

---

## The problem in one sentence

Covariance mixes two things together: (a) how strongly the assets co-move, and (b) how much each asset moves on its own. You can't tell which is driving the number.

## Concrete example: three asset pairs

| Pair | Asset 1 daily σ | Asset 2 daily σ | True correlation |
|------|----------------|----------------|------------------|
| SPY / BND | 1.2% | 0.4% | −0.3 |
| SPY / GLD | 1.2% | 0.9% | +0.1 |
| XLK / QQQ | 1.5% | 1.4% | +0.9 |

Now compute the covariances:

$$\text{Cov}(\text{SPY}, \text{BND}) = \rho \times \sigma_{\text{SPY}} \times \sigma_{\text{BND}}$$

$$\text{Cov}(\text{SPY}, \text{BND}) = -0.3 \times 1.2\% \times 0.4\% = -0.144 \text{ (in \%²)}$$

$$\text{Cov}(\text{SPY}, \text{GLD}) = +0.1 \times 1.2\% \times 0.9\% = +0.108 \text{ (in \%²)}$$

$$\text{Cov}(\text{XLK}, \text{QQQ}) = +0.9 \times 1.5\% \times 1.4\% = +1.890 \text{ (in \%²)}$$

Now rank them by covariance magnitude:

| Rank | Pair | Covariance | True correlation |
|------|------|-----------|------------------|
| 1 (largest) | XLK/QQQ | +1.890 | +0.9 |
| 2 | SPY/BND | −0.144 | −0.3 |
| 3 (smallest) | SPY/GLD | +0.108 | +0.1 |

The ranking happens to match the true correlation ordering here — but only by accident. Watch what happens if we change just the *scale* of one asset.

## How scale contaminates the comparison

Keep the same true correlations. But now suppose we're comparing SPY/BND (original) against a hypothetical **leveraged SPY** (3× SPY, σ = 3.6%) paired with BND at the same −0.3 correlation:

$$\text{Cov}(\text{3× SPY}, \text{BND}) = -0.3 \times 3.6\% \times 0.4\% = -0.432 \text{ (in \%²)}$$

The co-movement pattern is **identical** to SPY/BND — both have ρ = −0.3. But the covariance is 3× larger purely because one asset's scale tripled.

Now compare across pairs:

| Pair | Covariance | True correlation | "Stronger co-movement"? |
|------|-----------|------------------|------------------------|
| XLK/QQQ | +1.890 | +0.9 | Yes, genuinely strong |
| **3× SPY/BND** | **−0.432** | **−0.3** | Moderate, but covariance is larger than SPY/BND |
| SPY/BND | −0.144 | −0.3 | Moderate |
| SPY/GLD | +0.108 | +0.1 | Weak |

If you scanned only the covariance column, you'd rank 3× SPY/BND as having "stronger co-movement" than SPY/BND — but the relationship is exactly the same. The scale of SPY (1.2% vs 3.6%) contaminated the comparison.

## The decomposition makes it visible

Covariance = correlation × (σ₁ × σ₂). The σ₁ × σ₂ term is pure scale — it grows when either asset gets more volatile, regardless of whether the co-movement pattern changes.

Correlation strips that term out:

$$\rho = \frac{\text{Cov}}{\sigma_1 \sigma_2}$$

You're left with only the co-movement pattern, in units that mean the same thing (−1 to +1) regardless of whether you're comparing stocks/bonds, stocks/gold, or leveraged ETFs.

## The mental model

Think of covariance as a **raw signal** that's been amplified by the volatilities of both assets. Two assets with identical co-movement tendencies but different volatilities will produce different covariances. Correlation is the **gain-normalised** version — it divides out the amplification so you can compare the underlying signal across pairs.

---

## Check-in

1. Does the 3× SPY example make the contamination clear — same ρ, different Cov, purely from scale?
2. Why does the ranking by covariance magnitude sometimes accidentally match the ranking by correlation, and why can't you rely on that?
