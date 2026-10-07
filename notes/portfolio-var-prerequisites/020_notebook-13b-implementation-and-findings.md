# 020 — Notebook 13b Implementation and Findings

**Date:** 2026-07-24
**Topic:** Lead-lag measurement: does correlation actually lead VaR?
**Turn:** 020

## User request

Implement notebook 13b from the portfolio VaR lesson plan. Review the results, then give a detailed markdown report on the findings, explaining the methods and theory behind them.

## Work and response

### What was built

Notebook `13b_correlation_var_lead_lag.ipynb` at `projects/historical-var/notebooks/`. Three independent methods to quantify whether the correlation ratio (ρ₆₀/ρ₂₅₂) leads portfolio VaR, and by how many trading days.

---

# Notebook 13b Findings: Does Correlation Lead VaR?

## The question we tested

We've been claiming "correlation leads VaR" — that when SPY/BND correlation shifts, the 252-day VaR window takes months to catch up, leaving the reported VaR number stale. The evidence was anecdotal: the diversification benefit bottomed in June 2021, months before the 2022 rate hikes. But anecdote isn't measurement. We needed to answer:

1. **Does correlation actually lead VaR?** Or do they move together?
2. **If it leads, by how many trading days?**
3. **Is the lead stable across regimes?**

---

## The methods and their theory

### Method 1: Cross-correlation of changes (Δseries)

**Theory:** For two time series $X_t$ and $Y_t$, the cross-correlation at lag $k$ is:

$$\rho_k = \text{Corr}(X_t, Y_{t+k})$$

- $k > 0$: $X$ today predicts $Y$ in the future — $X$ leads $Y$
- $k = 0$: contemporaneous — they move together
- $k < 0$: $Y$ leads $X$ — the opposite of what we're testing

By computing $\rho_k$ for every $k$ from $-120$ to $+120$ trading days, we scan for the lag where the correlation is strongest. If the peak sits at $k \approx +40$ to $+80$, the ratio genuinely leads VaR by 2-4 months.

**Critical pitfall and fix:** Both the correlation ratio (autocorrelation 0.97) and VaR (autocorrelation 0.999) are heavily trended — they persist at similar levels for long periods. If you cross-correlate the raw levels, they appear correlated at *every* lag because both are correlated with time, not because one leads the other. The fix: **difference both series first.** We compute $\text{Corr}(\Delta X_t, \Delta Y_{t+k})$ — the relationship between *changes* in ratio today and *changes* in VaR in the future. This isolates the lead-lag in the innovations, which is the signal we actually care about.

We ran this for four predictor-outcome pairs:

| Predictor ($X$) | Outcome ($Y$) | Expected sign | Why |
|---|---|---|---|
| ΔRatio | ΔVaR | + | Ratio up → VaR up |
| ΔRatio | ΔBenefit | − | Ratio up → benefit down |
| ΔFast ρ | ΔVaR | + | Compare lead to ratio's |
| ΔFast ρ | Breach rate | + | Ultimate consequence |

The `find_peak_lag` function searches only $k \ge 0$ (we're testing whether $X$ leads $Y$, not the reverse) and matches the expected sign.

### Method 2: Event study

**Theory:** Cross-correlation gives a continuous average, but it can be dominated by noise. An event study isolates discrete episodes — moments when the ratio clearly spiked — and asks: *what was the average path of VaR, benefit, and breach rate around those events?*

Define an "event" as any day where $\rho_{60}/\rho_{252} > 2.0$, with at least 40 trading days between events to avoid counting the same spike twice. For each event, extract the VaR path from 60 days before to 180 days after. Average across all events.

**Critical pitfall and fix:** VaR naturally trends (it rises during volatile periods, falls during calm ones). If you average raw VaR paths, you'll see a rise regardless of whether correlation caused it — VaR would have risen anyway during those periods. The fix: **normalize each path by its pre-event baseline.** For each event, subtract the average VaR from days $-60$ to $-1$, so the chart shows *change from baseline*, not absolute level. This isolates whether events have a genuine effect beyond the natural VaR drift.

If the ratio leads VaR, the average VaR should be near zero pre-event (by construction) and rise *after* day 0 as the window absorbs the new correlation regime.

### Method 3: Rolling cross-correlation

**Theory:** The cross-correlation in Method 1 gives a single number for the full sample. But the lead time might vary by regime — longer in calm markets (where VaR windows are slow to adapt), shorter during crises (where everything moves fast). We recompute the cross-correlation in rolling 504-day (~2 year) windows, stepping every 21 trading days, and track where the peak sits over time.

Each window differences internally and computes the peak lag. The output is a time series of peak lags — if the lead is stable, the median will be consistent and the fraction of positive-lead windows will be high.

---

## The results

### Autocorrelation — confirming the pitfall was real

| Series | Lag-1 autocorrelation |
|---|---|
| Ratio (levels) | 0.966 |
| Ratio (differenced) | −0.238 |
| VaR (levels) | **0.999** |
| VaR (differenced) | 0.072 |

VaR at 0.999 means today's VaR is almost perfectly predicted by yesterday's — the series is a near-random-walk. Differencing removes this completely (0.072 ≈ white noise). Cross-correlating the raw levels would have produced spurious correlation at every lag. The fix was essential.

### Method 1: Cross-correlation

| Pair | Peak lag | Correlation | Contemporaneous (k=0) |
|---|---|---|---|
| ΔRatio → ΔVaR | **+0 days** | +0.118 | +0.118 |
| ΔRatio → ΔBenefit | **+2 days** | −0.122 | −0.063 |
| ΔFast ρ → ΔVaR | **+6 days** | +0.101 | +0.016 |
| ΔFast ρ → Breach rate | **+15 days** | +0.067 | +0.045 |

**What this says:**

- **ΔRatio → ΔVaR peaks at k=0 with ρ = +0.118.** The relationship is contemporaneous and modest. A change in the ratio today tells you about today's VaR — not tomorrow's. The correlation is correctly signed (ratio up → VaR up) but weak.
- **ΔRatio → ΔBenefit peaks at k=+2 with ρ = −0.122.** Correctly negative — ratio up → benefit down, nearly instantaneously. The benefit is the contemporaneous symptom, exactly as Notebook 12 described.
- **Fast ρ → VaR peaks at k=+6 (ρ=+0.101)** vs the ratio's k=0. Ironically, the fast correlation alone provides a slightly longer lead than the ratio — but both are effectively contemporaneous.
- **Fast ρ → Breach rate peaks at k=+15 (ρ=+0.067).** The weakest correlation of all four pairs, with a modest lead. Breach rates are noisy and the signal barely rises above zero.

### Method 2: Event study

- **19 events** identified (ratio > 2.0)
- **13 valid** (within data bounds — some events near the edges were excluded)

| Horizon | Mean ΔVaR (pp from baseline) | 25th pct | 75th pct |
|---|---|---|---|
| 20 days | +0.004 | −0.118 | +0.132 |
| 40 days | +0.010 | −0.162 | +0.263 |
| 60 days | +0.011 | −0.209 | +0.332 |
| 120 days | +0.003 | −0.191 | +0.332 |

**What this says:**

VaR moves a negligible +0.011 percentage points 60 days after a ratio spike. That's effectively zero — well within noise. The 25th–75th percentile envelope spans from negative to positive at every horizon, meaning the effect is not just small but **directionally inconsistent across events.** In some events VaR went up; in others it went down. There's no systematic post-event VaR rise.

This is the strongest evidence against a lead: if the ratio genuinely predicted VaR increases, the average VaR path around ratio spikes would show a clear upward trajectory. It doesn't.

### Method 3: Rolling cross-correlation

- **61 windows** (504-day, stepped every 21 days)
- **Mean peak lag: +32 days** — pulled up by a few windows with long lags
- **Median peak lag: +5 days** — effectively contemporaneous
- **61% positive lead** — roughly a coin flip

The skew between mean (+32) and median (+5) tells the real story: most windows show no lead (or a very short one), but a handful of windows produce long positive lags that inflate the mean. 61% positive is barely above random — if the lead were real and consistent, we'd expect 80%+.

---

## The bottom line

**No meaningful lead-lag relationship found. Correlation and VaR move contemporaneously.**

All three methods converge:

1. **Cross-correlation:** Peak at k=0. The ratio and VaR shift together.
2. **Event study:** Negligible post-event VaR movement (+0.011 pp). The effect is not just small — it's directionally inconsistent.
3. **Rolling CCF:** Median peak lag of 5 days. The lead direction flips across windows — not a reliable signal.

---

## What this does NOT mean

The correlation ratio is **not useless.** It remains a valuable **contemporaneous diagnostic** — it tells you "my VaR is based on stale correlation assumptions *right now*." When ρ₆₀/ρ₂₅₂ diverges from 1.0, the VaR number you're reporting is using yesterday's correlation regime. The ratio flags this in real time.

It just doesn't predict the future. It's a staleness gauge, not a crystal ball.

## What it means for the correlation-adjusted VaR (Notebook 15)

The adjustment in Notebook 15 doesn't "get ahead" of VaR — it **corrects VaR in real time** as the regime shifts. The breach improvement (6.36% → 4.89%) comes from catching staleness as it occurs, not from a predictive lead. This is still valuable — it means:

- The adjusted VaR is a **now-casting tool**, not a forecasting tool
- You adjust VaR when the ratio tells you it's stale *today*, not because it tells you VaR will rise next month
- The naive sum (ρ = +1) is your stress ceiling — use it when the ratio says correlation has already shifted, not because the ratio predicts it will shift

## At Spreadex

The ratio is your morning dashboard check. It won't tell you what VaR will be next month, but it will tell you whether today's VaR number is trustworthy. When ρ₆₀/ρ₂₅₂ diverges, the VaR you're showing traders is based on yesterday's correlation regime. Adjust it now.

## What we learned about the methods

The real intellectual contribution of this notebook may be the **methodological guardrails**:

1. **Always check autocorrelation before cross-correlation.** Trending series create spurious correlation at every lag. Differencing is not optional — it's the difference between measuring a genuine lead and measuring a common trend.
2. **Always normalize event studies by pre-event baseline.** Raw VaR paths trend, and averaging them will show a rise regardless of whether the event caused it. Subtract the pre-event average to isolate the event's effect.
3. **A null result is a useful result.** We set out to quantify a lead and found none. That's not a failure — it's a measurement that tells us the correlation-adjusted VaR works through a different mechanism than we assumed. Knowing *how* a tool works (real-time correction vs prediction) is essential for using it correctly.

## Files

- **Notebook:** `projects/historical-var/notebooks/13b_correlation_var_lead_lag.ipynb` — 16 cells, all executed, verified
- **Data pipeline:** Reuses the same SPY/BND 60/40 setup from Notebooks 12/13/15
- **New functions:** `cross_correlation()`, `find_peak_lag()`, `find_events()`, `event_study_paths()`, `rolling_peak_lag()` — all defined in-notebook, no new `src/` modules

## Next step

User review of notebook 13b. After approval: Notebook 14 (Portfolio VaR dashboard), then Notebook 15b (asymmetric blend refinement), per the lesson plan.
