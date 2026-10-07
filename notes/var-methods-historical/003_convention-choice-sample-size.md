# Convention Choice and the Real Question: Sample Size

**Date:** 2026-07-06
**Topic:** Choosing a convention, then focusing on what actually matters

---

## Convention: Interpolation Wins (But It's Not Close)

For implementation, use **linear interpolation**. Three reasons:

1. **Production standard.** numpy's `np.percentile(method='linear')`, pandas' `df.quantile()`, and every risk engine you'll encounter use interpolation. Using nearest rank would diverge from system VaR at Spreadex.

2. **Coherence across confidence levels.** If you calculate 95% VaR and 99% VaR, interpolation gives you different values that move smoothly with the confidence level. Nearest rank can give you the *same* value for 95% and 99% with small samples — which makes no economic sense.

3. **The difference is small enough to not be an argument.** With 252+ observations, the gap between the two methods is a fraction of one day's return. It's not where your error budget lives.

---

## Now: Sample Size — The Real Bet

This is where the method lives or dies. The historical VaR method assumes:

> The distribution of the next day's return is drawn from the same distribution as the last $n$ days.

That's the stationarity assumption you already know from Component 4. The choice of $n$ is a **bias-variance trade-off**:

| $n$ (sample size) | More data | Fewer data |
|---|---|---|
| **Bias** | Lower risk of sample-specific anomalies | Sample may not represent current regime |
| **Variance** | More stable estimate, less jumpy day-to-day | VaR jumps around, noisy signal |
| **Adaptation speed** | Slow to reflect new volatility regime | Fast to adapt, but overreacts to noise |
| **Tail coverage** | Better estimation of extreme percentiles | 99% VaR from 100 days = 1 observation |

### The Two Standard Choices

**1-year window ($n = 252$ trading days):**
- Industry baseline. Regulators accept it.
- 95% VaR uses the ~13th worst day. Reasonable.
- 99% VaR uses the ~3rd worst day. Thin.
- Covers one annual cycle of earnings, seasonality.

**2-year window ($n = 504$ trading days):**
- Better tail estimation (99% VaR uses ~5th worst day vs ~3rd).
- More stable — doesn't swing on a single bad week dropping out of the window.
- Risk: slow to reflect a new high-vol regime. After a volatility spike, old calm days are still in the window, pulling VaR down.

### What Happens at Regime Changes

Imagine you're using $n = 252$ days. It's March 2020. COVID hits.

- **Day 1 of crisis:** Your VaR is based on Feb 2019–Feb 2020 — a calm, low-vol period. VaR says your 95% daily loss threshold is maybe −2%. Market moves −8%. VaR is wrong by 4×.
- **Day 10 of crisis:** The window now contains 10 crisis days and 242 calm days. VaR drifts up slowly — still mostly calm.
- **Day 60 of crisis:** The window has 60 crisis days. VaR has risen substantially.
- **Day 253 of crisis (if it lasted that long):** All calm days have dropped out. VaR fully reflects the new regime. But the crisis is probably over by now.

**This is the fundamental limitation of historical VaR:** It's always looking backward. The window is either too slow to adapt or too noisy to trust.

---

## What Production Systems Actually Do

Most real risk systems don't use a single fixed window. They use one or more of:

1. **Exponentially weighted / decay-weighted historical VaR:** Recent days get more weight than distant days. This speeds up adaptation without the cliff effect of a hard window cutoff.

2. **Multiple windows side-by-side:** Run 60-day, 252-day, and 504-day VaR simultaneously. If the 60-day VaR crosses above the 252-day, that's a warning signal.

3. **Volatility-scaled returns:** Adjust historical returns to current volatility levels. This partially addresses the regime-change problem.

But those are enhancements. The core method is: pick a window, sort, read the percentile.

---

## For Your Implementation

Start with $n = 252$ (1 year). It's the baseline you can explain to anyone. Once it's working, we can add the enhancements.

---

## Before We Code — One Check

You now understand:
- How to sort returns and pick a percentile (interpolation)
- What sample size to use and the bias-variance trade-off
- The stationarity assumption and what happens when it breaks
- That historical VaR is "the $p$th worst day in the last $n$ days"

**Before I throw you into a notebook — is there anything hazy about the method itself, or are you ready to implement?**
