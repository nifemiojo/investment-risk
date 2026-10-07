# Combining Vol Scaling with Decay Weighting

**Date:** 2026-07-21
**Topic:** What happens when you combine the two mitigations — theoretical analysis
**Turn:** 008b

## The motivation

Each mitigation attacks a different aspect of the equal-weighting problem:

| Mitigation | Fixes | Doesn't fix | Free parameter |
|------------|-------|-------------|----------------|
| Decay weighting | Ordering (old returns matter less) | Magnitudes (old returns keep their original size) | λ |
| Vol scaling | Magnitudes (returns rescaled to current vol) | Ordering (old returns still get equal weight after scaling) | vol window |

The natural next step: **use both.** Scale returns to current vol, then decay-weight the scaled returns. This attacks both the stale-ordering problem AND the stale-magnitude problem simultaneously.

## How it would work

For each day in the rolling window:

1. Compute σ_today and σ_t for each historical return (as in vol scaling)
2. Compute $r_t^{\text{scaled}} = r_t \times (\sigma_{\text{today}} / \sigma_t)$
3. Assign decay weights $w_t = \lambda^{\text{age}}$ to the scaled returns
4. Compute weighted quantile on the decay-weighted, vol-scaled returns

Or equivalently: decay-weight the standardised returns, then scale the resulting quantile by σ_today. The operations commute because the scaling factor σ_today is a constant multiplier on all returns.

## What it buys you

### During a crisis onset

- **Vol scaling** rescales the pre-crisis returns downward (they happened at lower vol) and crisis returns upward → the entire distribution shifts to reflect current vol
- **Decay weighting** then gives crisis returns MORE weight (they're recent) and pre-crisis returns LESS weight (they're old) → the VaR is dominated by the recent, correctly-scaled crisis returns

The combination should produce the FASTEST reaction to a regime change: decay weighting makes it react quickly to new data, and vol scaling ensures that the new data is measured in the right units.

### During a calm period after a crisis

- **Vol scaling** rescales old crisis returns to current (calm) vol — they become less extreme
- **Decay weighting** further downweights them because they're old
- The combined effect: old crisis returns have minimal influence on current VaR

## The new assumptions (both methods stacked)

Each method adds its own assumption. When combined, you assume:

1. **Decay assumption:** Recent standardised returns are more relevant than old ones (controlled by λ)
2. **Vol scaling assumption:** The distribution of standardised returns is stable over time (shape doesn't change with regime)
3. **Independence assumption:** The two effects are separable — you can fix ordering and magnitude independently

Assumption 3 is probably the weakest link. If crisis standardised returns are both *more relevant* AND *differently shaped*, then decay weighting and vol scaling interact — the decay weights amplify whatever shape differences exist between recent and old standardised returns.

## The parameter problem gets worse

You now have THREE free parameters:

| Parameter | What it controls | Typical range |
|-----------|-----------------|---------------|
| VaR window | How much history to draw from | 252 or 504 days |
| λ | How aggressively to favour recent data | 0.90–0.99 |
| Vol window | How fast vol estimates adapt | 10–60 days |

Each one trades off speed vs stability. With three parameters, you can fit almost anything to historical data. This is a real risk — the combination may look great in backtests because you have enough degrees of freedom to find a combination that worked historically, not because the model is genuinely better.

## Would it actually help on SPY?

Based on what we've seen:

- **Decay alone** already gives fast reactions (6 days to double during COVID) and the most consistent regime-conditional breach rates
- **Vol scaling alone** gives the MOST consistent regime-conditional breach rates but slower reactions (9 days)
- **Combining them** would likely produce breach rates somewhere between the two, with reaction speed closer to decay

The marginal benefit might be small. Decay weighting already achieves most of what you'd want from the combination — it naturally downweights old crisis returns during calm periods. Adding vol scaling on top would further compress those old crisis returns, but since they're already heavily downweighted, the incremental effect is modest.

## The honest assessment

| Aspect | Verdict |
|--------|---------|
| Theoretically sound? | Yes — the two fixes address orthogonal problems |
| Practically useful? | Probably marginal — decay already does most of the work |
| New risks? | Parameter proliferation (3 degrees of freedom), interaction effects |
| When would it shine? | Long windows (504d) with aggressive decay (λ=0.90) — vol scaling keeps old returns relevant by rescaling them, decay keeps the emphasis on recent data |

The combination is most interesting for long VaR windows. With a 504-day window and λ=0.94, old returns from 400+ days ago have near-zero decay weight anyway, so vol scaling them doesn't change much. But with a 504-day window and λ=0.99 (near-equal), vol scaling would make those old returns properly scaled while decay would still give them roughly equal weight — a more interesting combination.

## The meta-point

Every time you combine mitigations, you're doing the same thing the original methods did: replacing a strong assumption with a weaker one. But you're also adding parameters and interaction complexity. At some point, the marginal improvement stops justifying the added complexity.

The right question is not "can I combine these?" but "does the combination produce a meaningfully different — and better — answer than either method alone?" On SPY with a 252-day window, the answer is probably: marginally, not enough to justify the extra complexity.