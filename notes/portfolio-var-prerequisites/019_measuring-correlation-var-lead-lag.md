# 019 — Measuring the Correlation → VaR Lead: Does Correlation Actually Lead?

**Date:** 2026-07-22
**Topic:** Quantifying the time relationship between correlation shifts and VaR responses

---

## The claim we need to test

We've been saying "correlation leads VaR." The evidence so far is anecdotal: the benefit bottomed in June 2021, months before the 2022 rate hikes. But "anecdotal" isn't "measured." We need to answer:

1. **Does correlation actually lead VaR?** (Or is it simultaneous? Or does VaR lead correlation?)
2. **If it leads, by how many trading days?** (Days? Weeks? Months?)
3. **Is the lead consistent across different regimes?** (Or does it only work sometimes?)

---

## Method 1: Cross-correlation — the direct measurement

For two time series $X_t$ and $Y_t$, the cross-correlation at lag $k$ is:

$$\rho_k = \text{Corr}(X_t, Y_{t+k})$$

- $k > 0$: "Does X today predict Y in the future?" (X leads Y)
- $k = 0$: contemporaneous correlation
- $k < 0$: "Does Y today predict X in the future?" (Y leads X)

**Apply it:** Compute the correlation between the correlation ratio (detector) at time $t$ and portfolio VaR at time $t + k$, for $k$ ranging from, say, −120 to +120 trading days.

**What to look for:**

```
Cross-correlation plot (correlation ratio → VaR)
         |
    peak |     *            ← if peak is at k > 0, ratio leads VaR
         |    / \
         |   /   \
         |  /     \_____
         | /
         +-------------------→ lag (trading days)
        -60   0   +60  +120
```

- **Peak at k ≈ +40 to +80:** Correlation ratio leads VaR by 2-4 months. The mechanism: ratio spikes → correlation regime shifts → VaR window slowly absorbs new data → VaR rises.
- **Peak at k ≈ 0:** No lead — the relationship is contemporaneous. Correlation and VaR move together.
- **Peak at k < 0:** VaR leads correlation. This would be surprising and suggest a different mechanism.

**What to measure with the correlation ratio vs portfolio VaR:**

| $X_t$ (predictor) | $Y_{t+k}$ (outcome) | Expected lead |
|---|---|---|
| Correlation ratio $(ρ_{60}/ρ_{252})$ | Portfolio VaR | +40 to +80 trading days |
| Correlation ratio $(ρ_{60}/ρ_{252})$ | Diversification benefit | Negative correlation at k ≈ 0, fading |
| $ρ_{60}$ (fast correlation alone) | Portfolio VaR | +20 to +60 trading days |
| $ρ_{60}$ (fast correlation alone) | Breach rate (rolling 60d) | +10 to +40 trading days |

**The correlation ratio should lead VaR more than the fast correlation alone** — because the ratio captures the *divergence* between regimes, which is the early warning signal. The fast correlation alone has already partially adapted.

---

## Method 2: Event study — what happens after a correlation spike?

Instead of continuous cross-correlation, define discrete "events" and track what happens afterward.

**Event definition:** A correlation ratio spike — when $ρ_{60} / ρ_{252}$ crosses above some threshold (e.g., 2.0).

**For each event, track:**

| Days after event | Metric | Expected pattern |
|-----------------|--------|-----------------|
| 0 (event day) | Ratio spikes | Trigger |
| 0 to 20 | Fast ρ continues rising | Correlation regime establishing |
| 20 to 60 | Portfolio VaR starts rising | Window begins absorbing new data |
| 60 to 120 | Portfolio VaR converges toward naive sum | Full absorption |
| 120+ | Breach rate spike (if VaR understated during lag) | Consequence |

**Plot:** For all events, compute the average path of VaR, benefit, and breach rate from 60 days before to 180 days after each event. This is an "event study" plot.

**What it reveals:**

```
Event study: Average path after correlation spike
         |
  VaR    |                    ___---"""""
         |               ___--"
         |          ___--"
         |     ___--"
         |____"   ← VaR rising ~40-80 days after event
         |
         +---|----|----|----|----|----→ days
        -60   0   30   60   90   120
              ^
           event
           (ratio > 2)
```

If VaR reliably rises 40-80 days after a ratio spike, the lead is real and measurable.

---

## Method 3: Granger causality — the statistical test

A time series $X_t$ "Granger-causes" $Y_t$ if lagged values of $X$ help predict $Y$ beyond what lagged values of $Y$ alone can predict.

**The test:**

1. **Restricted model:** $\text{VaR}_t = \alpha + \beta_1 \text{VaR}_{t-1} + \beta_2 \text{VaR}_{t-2} + \ldots + \epsilon_t$

2. **Unrestricted model:** $\text{VaR}_t = \alpha + \beta_1 \text{VaR}_{t-1} + \ldots + \gamma_1 \text{Ratio}_{t-1} + \gamma_2 \text{Ratio}_{t-2} + \ldots + \epsilon_t$

3. **Test:** Does adding lagged Ratio significantly improve the model? (F-test on the γ coefficients)

If yes → correlation ratio Granger-causes VaR. If no → the relationship is contemporaneous or VaR contains all the predictive information already.

**Caveat:** Granger causality is about *predictive* causality, not *structural* causality. It tests "does knowing X's past help predict Y's future?" — not "does X cause Y?" But for a risk monitoring system, predictive causality is exactly what we care about.

---

## What to build: a lead-lag diagnostic notebook

A new notebook (or an addition to Notebook 13) that:

1. **Cross-correlation plot** — correlation ratio vs VaR at lags −120 to +120 days. Find the peak.
2. **Cross-correlation plot** — fast ρ vs VaR. Compare lead times.
3. **Event study** — average VaR path after ratio > 2.0 events. Show the ramp.
4. **Rolling cross-correlation** — does the lead time change across regimes? (e.g., is it longer during bull markets, shorter during crises?)

### The key question the analysis answers

> "When the correlation ratio spikes today, should I adjust my VaR now, or wait for evidence?"

If cross-correlation shows a clear peak at +40 to +80 days, the answer is: adjust now. The VaR window won't catch up for 2-4 months. The ratio gives you that lead time.

If cross-correlation shows no clear peak (or peak at 0), the answer is: correlation and VaR move together. The ratio is still useful as a contemporaneous diagnostic ("is my VaR stale right now?") but not as a leading indicator.

---

## How this connects to everything you've built

| What you have | What this adds |
|--------------|---------------|
| Diversification benefit | Quantifies *how much* the gap is worth |
| Correlation ratio | Detects *when* the regime is shifting |
| **Lead-lag measurement** | Quantifies *how long* you have to act |
| Correlation-adjusted VaR | *Uses* the lead to adjust VaR |

The lead-lag measurement closes the loop: it tells you whether the correlation-adjusted VaR experiment (Notebook 15) is built on a real effect or a spurious pattern.

---

## Check-in

1. Does cross-correlation as the measurement tool make intuitive sense — "correlate today's ratio with VaR N days from now, find where it peaks"?
2. Which method would you want to build first: the cross-correlation plot or the event study?
3. Does this feel like the right next step — measuring the claim before acting on it — or would you rather refine the adjustment experiment first?
