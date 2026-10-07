# Sample Size Trade-Offs: Concrete Examples

**Date:** 2026-07-06
**Topic:** How different window sizes produce different VaR estimates — and why it matters

---

## Setup: A Regime Change Scenario

You're calculating 1-day 95% historical VaR today. Here's the history you're looking back on:

```
Days 1–400:  Calm regime. Daily returns ~ N(0, 1%²). Typical day: ±0.5–1.5%.
             The worst day in this period: about −2.5%.

Day 401:     Regime shift. Volatility triples.
Days 401–500: Volatile regime. Daily returns ~ N(0, 3%²). Typical day: ±2–4%.
             Several days at −5%, −6%, −7%.
```

You're standing at day 500. What VaR do you get?

---

## Three Windows, Three Answers

### Short Window: 60 Days (Days 441–500)

You only see the volatile regime. Your sorted worst days:

```
−7.2%, −6.1%, −5.4%, −4.8%, −4.1%, −3.7%, −3.2%, ...
```

95% VaR (5th percentile of 60 ≈ 3rd worst): roughly **−6.1%**

**Verdict:** VaR is high, reflecting current reality. But it's jumpy — if that −7.2% day drops out of the window tomorrow, VaR could fall from −6.1% to −5.4% overnight, even though nothing about the world changed. The window is so short that a single extreme day has outsized influence.

---

### Standard Window: 252 Days (Days 249–500)

Your window contains:

```
Days 249–400: 152 calm days (most between −1.5% and +1.5%)
Days 401–500: 100 volatile days (several at −5% to −7%)
```

The sorted worst days are a mix of volatile-regime tail events:

```
−7.2%, −6.1%, −5.4%, −4.8%, −4.1%, −3.7%, −3.2%, −2.8%, −2.5%, −2.3%, ...
```

95% VaR (5th percentile of 252 ≈ 13th worst): roughly **−3.7%**

**Verdict:** The 152 calm days pull the percentile *up* (less extreme). VaR is lower than short-window — it's saying your risk is smaller than it actually is right now. The calm regime is a ghost haunting your estimate.

---

### Long Window: 504 Days (Days −3 to 500, hypothetical)

Even more calm days dilute the volatile tail. The 5th percentile moves further up. VaR drifts even lower — maybe **−2.8%** — even though today's actual volatility is 3× what it was.

**Verdict:** Maximum stability, minimum relevance. The estimate is precise but wrong.

---

## Visual Summary

```
Regime shift
    ↓
    |══════════ calm ══════════|═══ volatile ═══|
    Days 1–400                401              500
                                                    ↑ today

60-day VaR:   ████████████████████████████████████  −6.1%  (reactive, noisy)
252-day VaR:  ████████████████████████████████████  −3.7%  (lagged, smoother)
504-day VaR:  ████████████████████████████████████  −2.8%  (stable, stale)
```

---

## The Trade-Off, Quantified

| Property | Short (60d) | Standard (252d) | Long (504d+) |
|---|---|---|---|
| **Reactivity** | Fast to reflect new vol | Moderate lag | Slow — drags old data |
| **Stability** | Jumps day-to-day | Moderate stability | Very stable |
| **Tail accuracy** | Poor — 3 data points for 95% VaR | Adequate — 13 data points | Good — 25+ data points |
| **Regime-change performance** | Best during crisis | Mediocre during crisis | Worst during crisis |
| **Regime-change false alarms** | Worst (noise mistaken for shift) | Moderate | Rare |
| **99% VaR feasibility** | Meaningless (0.6 observations) | Barely (2.5 observations) | Acceptable (5 observations) |

---

## The Real Question Isn't "Which is Right?"

It's: **What are you using VaR for?**

| Use Case | Preferred Window | Reasoning |
|---|---|---|
| **Regulatory capital** | 252d (or longer) | Stability matters. Regulators don't want capital requirements jumping day-to-day. |
| **Intraday risk monitoring** | 60d or shorter | You need to know what's happening *now*, not what happened last year. |
| **Position limit setting** | 252d | Limits shouldn't swing on noise. Stability > reactivity. |
| **Crisis detection** | Compare 60d vs 252d | When short-window VaR crosses above long-window VaR, that's your signal. |
| **Backtesting** | Match your production window | You can only validate the model you're actually using. |

---

## What Production Systems Actually Do

The most common pattern is not a single window — it's a dashboard:

```
 60-day VaR:  −6.1%  ← what's happening now
252-day VaR:  −3.7%  ← baseline for limits/capital
504-day VaR:  −2.8%  ← long-term reference

When 60d < 252d (more negative): regime shift warning
When 60d > 252d (less negative): regime calming — was it a false alarm?
```

---

## For Your Implementation

Start with 252-day as the primary output. But structure your code so the window size is a parameter — not hardcoded. That way you can run multiple windows side by side and build the dashboard pattern later without rewriting anything.

---

## Check-In

Does this trade-off feel clear? Specifically: can you articulate *why* a risk manager might want a 504-day VaR even though it's "stale" during a crisis, and *why* a trader might want a 60-day VaR even though it's noisy?
