# Beyond Fixed Windows: Production Mitigations

**Date:** 2026-07-06
**Topic:** How real risk systems address the stationarity problem without abandoning the historical method

---

## The Problem, Restated

You nailed it. The stationarity assumption — "tomorrow will look like the last $n$ days" — breaks at exactly the moment you most need VaR to be right: when volatility spikes. A shorter window helps (more reflective), but introduces noise. A longer window is stable, but drags stale calm-regime data into a crisis.

The fixed window treats every day in the sample as equally relevant. That's the core assumption that every production enhancement attacks.

---

## Mitigation 1: Exponential Decay Weighting

**The idea:** Instead of a hard cutoff ("days 1–252 are in, day 253 is out"), give every day a weight that decays as you go further back in time. Yesterday matters most. A day 252 days ago barely matters.

### How It Works

Pick a decay factor $\lambda$ (lambda) between 0 and 1. Typically $\lambda \approx 0.94$ to 0.99.

The weight for a return that happened $t$ days ago is:

$$w_t = \lambda^t$$

And then you normalize so all weights sum to 1:

$$\tilde{w}_t = \frac{\lambda^t}{\sum_{i=0}^{n-1} \lambda^i}$$

**Terms:**
- $\lambda$ — decay factor (0.94 means each day loses 6% of its weight)
- $t$ — how many days ago the return occurred ($t=0$ = today/yesterday)
- $w_t$ — raw weight before normalization
- $\tilde{w}_t$ — normalized weight (sums to 1 across all days)
- $n$ — total number of days in the sample

### Concrete Example with $\lambda = 0.94$

```
Day t=0 (yesterday):     weight = 0.94⁰ = 1.000  →  ~3.5% of total
Day t=10 (10 days ago):   weight = 0.94¹⁰ = 0.539 →  ~1.9% of total
Day t=50 (50 days ago):   weight = 0.94⁵⁰ = 0.045 →  ~0.16% of total
Day t=100 (100 days ago): weight = 0.94¹⁰⁰ = 0.002 → negligible
Day t=252 (1 year ago):   weight = 0.94²⁵² ≈ 0.0000002 → essentially zero
```

The effective lookback is much shorter than 252 days. With $\lambda = 0.94$, days beyond about 75 trading days contribute almost nothing. But there's no cliff — old data fades smoothly rather than dropping out abruptly.

### How VaR Changes Under Decay Weighting

Instead of "the 5th percentile of equally-weighted returns," it's: **find the return level such that the cumulative weight of all worse returns equals 5%.**

**Same regime-change scenario from before (day 500, 100 days into volatile regime):**

| Method | 95% VaR | Why |
|---|---|---|
| Fixed 60-day | −6.1% | Only sees volatile regime, jumpy |
| Fixed 252-day | −3.7% | 152 calm days still pulling estimate up |
| **Decay-weighted 252-day, $\lambda = 0.94$** | **~−5.2%** | Calm days from 150+ days ago have near-zero weight; volatile days dominate |

The decay-weighted estimate sits between short and long windows — reactive like a short window but smoother because there's no hard cutoff where a single extreme day suddenly enters or leaves.

### The Trade-off

You've introduced a new parameter ($\lambda$) that you now have to choose. RiskMetrics (the industry standard for this approach) recommends $\lambda = 0.94$ for daily data and $\lambda = 0.97$ for monthly. But the choice is just as consequential as the window size was.

---

## Mitigation 2: Volatility Scaling (Filtered Historical Simulation)

**The idea:** Don't throw away old data. Instead, rescale old returns so they reflect *today's* volatility level.

### How It Works

For each historical return $r_t$ from $t$ days ago, compute:

$$r_t^{\text{scaled}} = r_t \times \frac{\sigma_{\text{today}}}{\sigma_t}$$

**Terms:**
- $r_t$ — the actual return $t$ days ago
- $\sigma_{\text{today}}$ — current estimated volatility (e.g., 20-day realized vol)
- $\sigma_t$ — the volatility at the time of that historical return (estimated from the period around it)
- $r_t^{\text{scaled}}$ — the volatility-adjusted return

### Concrete Example

```
Historical day: April 2024. Return was -2.1%. Vol at the time was 0.8%.
Today: July 2026. Current vol is 2.4%.

Scaled return = -2.1% × (2.4% / 0.8%) = -2.1% × 3 = -6.3%
```

That −2.1% day from a calm period, when rescaled to today's volatility, represents a −6.3% event. It was a 2.6-sigma day then; it's a 2.6-sigma day now.

### Why This Helps

- You can use all 252 (or 504) days without dragging stale calm-regime magnitudes into your VaR.
- A 3-sigma day from a calm regime becomes a 3-sigma day at current vol — the *relative* extremeness is preserved.
- The stationarity problem shifts from "returns are stationary" to "standardized returns are stationary" — a weaker, more defensible assumption.

### The Real Assumption

Volatility scaling assumes that the *shape* of the return distribution is stable over time (the relative ordering of good vs bad days), even though the *scale* changes. Fat tails stay fat. Skew stays skew. Only the width changes.

This is falsifiable — and often false. Crisis returns aren't just bigger; they're differently shaped (fatter left tail, higher correlation across assets). But it's a better assumption than "nothing changes."

---

## Mitigation 3: Multi-Window Dashboard (The Pragmatic Approach)

Already touched on in the previous file, but to make it concrete:

```
┌─────────────────────────────────────────────┐
│ RISK DASHBOARD                   2026-07-06 │
├─────────────────────────────────────────────┤
│                                             │
│  60-day HVaR:   −5.8%  ▲ (rising)          │
│ 252-day HVaR:   −3.2%  — (stable)          │
│ 504-day HVaR:   −2.7%  — (stable)          │
│                                             │
│  ⚠ 60d/252d ratio: 1.81                     │
│    (ratio > 1.5 → regime shift warning)     │
│                                             │
│  Decay-weighted (λ=0.94): −4.9%             │
│  Vol-scaled (252d):       −4.1%             │
│                                             │
└─────────────────────────────────────────────┘
```

No single number is "the" VaR. You read the dashboard as a system:

- **60d rising while 252d is flat:** volatility spike. Investigate.
- **60d crossing above 252d:** regime shift. Tighten limits.
- **Decay-weighted near 60d:** the shift is persistent (not just one bad day).
- **Vol-scaled near decay-weighted:** the shape of returns is similar, just scaled up — less concerning than if vol-scaled VaR is much lower (suggesting a shape change, not just a scale change).

---

## Putting It Together: What "Good" Historical VaR Looks Like in Production

```
Raw returns (252 days)
    │
    ├──→ Fixed-window HVaR (baseline)
    │
    ├──→ Decay-weighted HVaR (λ = 0.94)
    │       │
    │       └──→ Compare to fixed: is recent data telling a different story?
    │
    ├──→ Volatility-scaled HVaR
    │       │
    │       └──→ Compare to decay-weighted: is it just vol, or is shape changing?
    │
    └──→ Multi-window dashboard (60d, 252d, 504d)
            │
            └──→ Ratios as early-warning signals
```

---

## One Clarification Before We Code

These three mitigations attack different aspects of the same problem:

| Mitigation | What It Fixes | What It Assumes |
|---|---|---|
| Decay weighting | Old data shouldn't matter as much | $\lambda$ is correctly chosen |
| Vol scaling | Old data's magnitude should be adjusted | Distribution shape is stable |
| Multi-window | No single window is sufficient | You can interpret the ratios |

They're complementary — production systems often use all three.

---

## Check-In

Which of these three mitigations feels most natural or defensible to you? And — thinking about your work at Spreadex — which one would be most valuable for someone monitoring intraday risk vs someone setting overnight position limits?
