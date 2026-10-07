# Vol scaling's core assumption: standardised return distribution is time-invariant

**Date:** 2026-07-14
**Topic:** The shape-stability assumption — what vol scaling actually assumes
**Turn:** 007d

## User observation

Vol scaling makes an assumption about the consistency of the standardised return distribution over time.

## Response

Yes — that is the central assumption. Everything vol scaling does rests on one claim:

> **The distribution of $z_t = r_t / \sigma_t$ is the same regardless of when you measure it.**

If true, then multiplying $z_t$ by today's volatility $\sigma_{\text{today}}$ gives you a valid distribution for tomorrow's returns. The shape (skew, kurtosis, tail behaviour) is stable — only the scale changes.

### What "consistent over time" actually means

| Property | Must be stable? | What happens if it isn't |
|----------|----------------|-------------------------|
| Variance (σ of z) | Yes — should be ~1.0 always | If >1 during crises, VaR understated |
| Skew | Yes — left-tail fatness constant | If more negative during crises, tail risk underestimated |
| Kurtosis | Yes — extreme event frequency constant | If higher during crises, 99% VaR too low |

### Where it breaks

The assumption partially holds (standardised returns are more similar across regimes than raw returns) but isn't fully true. During crises:

- Standardised returns develop **fatter left tails** (more negative skew) — the worst days are worse than their sigma_t would predict
- **Kurtosis rises** — extreme standardised events are more common
- The KS test in Part E sometimes rejects identical distributions

### The honest summary

Vol scaling replaces "returns are stationary" with "standardised returns are stationary." The second assumption is weaker (you've removed the vol-regime mixing artifact) and partially holds in practice. But it still breaks during crises — and that's when you need VaR to be right.

Every historical VaR enhancement is the same pattern: replace a strong assumption with a weaker one that's still falsifiable. None of them eliminate assumptions.