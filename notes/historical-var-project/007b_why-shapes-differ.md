# Why standardised and scaled distributions look different from original returns

**Date:** 2026-07-14
**Topic:** Understanding why vol scaling produces a tighter shape than the original distribution
**Turn:** 007b

## User observation

The standardised and vol-scaled distributions have the same shape as each other but look different from the original returns distribution — narrower, more concentrated.

## Explanation

### The original returns mix two volatility regimes

The 252-day window (March 2020 to March 2021) spans a period where volatility changed dramatically:

- **March 2020:** daily σ ≈ 5%. Returns of ±5% to ±10% were common.
- **March 2021:** daily σ ≈ 1%. Returns of ±1% to ±2% are typical.

The original return distribution shows the **mixture** of these two regimes. It has fat tails because the high-vol returns from March 2020 sit far out in the tails, pulling the distribution wide. But it also has a tall peak because the low-vol returns from 2021 cluster tightly around zero.

This mixture produces a distribution that looks like two distributions superimposed — which is exactly what it is. The "shape" of the original returns isn't a single shape at all: it's a superposition of two shapes with different widths.

### What standardisation does

When you compute $z_t = r_t / \sigma_t$, you divide each return by the volatility *at its own time*. A -5% return from March 2020 (σ=5%) becomes $z = -1\sigma$. A -1% return from March 2021 (σ=1%) becomes $z = -1\sigma$. Same extremeness, different raw magnitudes.

Standardisation strips out the time-varying volatility and leaves only the *relative* extremeness of each return. The resulting distribution:

- Has σ ≈ 1.0 (by construction — you divided by σ)
- Shows the **underlying shape** of returns independent of the vol regime
- Is narrower than the original because the high-vol returns are no longer stretched out

### What vol-scaling does

$r_t^{\text{scaled}} = z_t \times \sigma_{\text{today}}$ takes the standardised shape and stretches it to today's vol. So the vol-scaled distribution has:

- The **same shape** as standardised returns (they differ only by a constant multiplier σ_today)
- A width that reflects **current** volatility rather than the historical mixture

### Why this matters

This is actually the core insight of vol scaling made visible. The original return distribution's fat tails are partly real (the underlying shape has fat tails) and partly an artifact of mixing different volatility regimes. Standardisation separates the two effects:

- **How much of the tail fatness is vol-regime mixing?** The difference between the original and standardised distributions.
- **How much is inherent non-normality?** The residual fatness in the standardised distribution itself.

On SPY, you can see that a meaningful portion of the fat tails is indeed vol clustering, not inherent. The standardised distribution is visibly tighter — meaning vol scaling genuinely helps by removing the regime-mixing artifact from the VaR calculation.