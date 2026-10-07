# Interpreting decay-weighted breach rates

**Date:** 2026-07-14
**Topic:** Why equal-weighted VaR has fewer breaches than decay-weighted
**Turn:** 005e

## User observation

Equal-weighted rolling VaR has the lowest number of breaches (90, 4.76%). As decay becomes more aggressive (lower λ), breaches increase: λ=0.94 → 113 (5.97%), λ=0.90 → 139 (7.35%).

It seems like the "better" model (faster reaction) is performing worse. What's going on?

## Analysis

### The model drops as fast as it rises

Decay weighting is symmetric — it weights recent returns more heavily in BOTH directions. During a crisis, recent returns are negative → VaR rises faster (good). During a calm period, recent returns are small → VaR drops faster (also correct, but produces more breaches).

The 252-day equal-weighted VaR during a calm period carries old volatile returns from years ago. This inflates VaR, making it conservative → fewer breaches. The decay-weighted VaR sheds old volatility quickly, producing a lower, more accurate VaR during calm periods → more breaches during calm.

### Breach decomposition (approximate)

| Period | Equal-weighted VaR | Decay VaR (λ=0.94) | Effect on breaches |
|--------|-------------------|---------------------|--------------------|
| Calm (2018-2019, 2021, 2023+) | Higher (stale vol) | Lower (fresh calm) | Decay breaches MORE during calm |
| Crisis (COVID, 2022) | Lower (slow to react) | Higher (fast to react) | Decay breaches LESS during crises |
| **Net** | 90 breaches | 113 breaches | Decay has more calm-period breaches |

### This is not a failure of decay weighting

The higher breach count doesn't mean decay is worse. It means:

1. **Equal-weighted is systematically conservative during calm periods** — it overstates risk because old volatile days haven't dropped out yet. This makes breach rates look good, but it's a miscalibration in the conservative direction.

2. **The total breach count is not the right metric.** What matters is whether breaches are evenly distributed (calibrated across regimes) or clustered (appearing only when risk is low, missing when risk is high). Decay weighting produces breaches more evenly across time, which is arguably better calibration.

3. **The right evaluation is conditional breach rates by regime** (like notebook 04 Part C). A model with 5% breaches overall but 20% during crises and 2% during calm is worse than a model with 6% overall but 7% during crises and 5% during calm.

### The deeper point

Every VaR enhancement (shorter window, decay weighting, volatility scaling) increases breach counts during calm periods because the model becomes more responsive and drops its guard faster. This looks like worse performance but is actually better calibration — it reflects the true current risk rather than stale historical risk.

The only way to have consistently low breach counts is to use a long window that inflates VaR with old crisis data. That's not accuracy — it's conservatism masquerading as calibration.