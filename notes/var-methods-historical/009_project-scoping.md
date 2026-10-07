# Project Scoping: From Theory to Practice

**Date:** 2026-07-06
**Topic:** Concrete projects to force real understanding of historical VaR

---

## Design Principles

Each project below is:

- **Relevant:** Connects to your Spreadex work (risk monitoring, position limits, regime detection)
- **Contextual:** Uses real market data, not synthetic examples
- **Useful:** Produces something you could actually show or use
- **Realistic:** Scoped for a notebook, not a production system
- **Learning-forcing:** You can't complete it without understanding the concepts

---

## Project 1: Historical VaR Calculator — Single Asset

**What you build:** A clean function/notebook that takes a ticker and returns 1-day VaR at any confidence level with any window.

**Input:** SPY daily returns (from yfinance, 2020–present)

**Features:**
- Sort returns, pick percentile using interpolation
- Parametrized window size (60d, 252d, 504d — not hardcoded)
- Parametrized confidence level (95%, 99%)
- Output: "Your 1-day 95% VaR with a 252-day window is −3.2%"

**What it forces you to learn:**
- Actually handling real return data (dividend adjustments, missing days, weekends)
- Implementing percentile interpolation correctly (or using numpy and knowing which method you picked)
- Seeing how VaR changes day-to-day as the window rolls forward

**Output artifact:** One clean notebook, ~50 lines of Python

**Time:** 1–2 hours

**Relevance to Spreadex:** This is the building block. Everything else builds on it.

---

## Project 2: Multi-Window Regime Dashboard

**What you build:** Side-by-side VaR estimates across multiple windows with visual regime shift signals.

**Input:** SPY + one other asset (BND or GLD for diversification contrast)

**Features:**
- Rolling 60d, 252d, and 504d VaR plotted over time
- Ratio indicator: 60d VaR / 252d VaR — spikes = regime shift warning
- Mark known crisis periods (COVID March 2020, 2022 rate hikes) on the chart
- Show: "When did the dashboard warn? How much lead time?"

**What it forces you to learn:**
- The bias-variance trade-off is no longer abstract — you see it in the chart
- How much lag does 252d VaR have at a real regime change? (Spoiler: a lot)
- When does the 60d/252d ratio fire false alarms?

**Output artifact:** Notebook with annotated chart, ~100 lines

**Time:** 2–3 hours

**Relevance to Spreadex:** This IS what a risk monitoring dashboard looks like. The only difference is data source.

---

## Project 3: Backtesting Framework

**What you build:** A systematic backtest that answers: "Did the VaR model work?"

**Input:** SPY data, rolling historical VaR estimates from Project 1

**Features:**
- For each day, compute VaR from prior 252 days
- Compare to actual next-day return — is it a breach?
- Count breaches, compare to expected rate (5% for 95% VaR)
- Kupiec test (binomial test: is the breach rate statistically different from expected?)
- Christoffersen test (are breaches clustered, or independent?)
- Plot: breaches over time with regime markers

**What it forces you to learn:**
- VaR is only as good as its backtest
- Breaches cluster — they're not independent (Christoffersen catches this)
- The 2008 and COVID breaches aren't random — they're concentrated in crisis periods
- "5% breach rate" can hold on average while still being useless (all breaches in one month)

**Output artifact:** Notebook with statistical tests + breach visualization

**Time:** 2–3 hours

**Relevance to Spreadex:** You're validating the model you'd actually use. This is operational risk discipline.

---

## Project 4: Method Comparison — Historical vs Parametric vs Decay-Weighted

**What you build:** Three VaR methods on the same data, side by side, showing where and why they diverge.

**Input:** SPY returns

**Features:**
- Historical VaR (from Project 1)
- Parametric VaR (normal assumption: $\text{VaR}_{95\%} $≈$ \mu - 1.645\sigma$)
- Decay-weighted historical VaR ($\lambda = 0.94$)
- Plot all three over time
- Highlight divergence periods: when does parametric say "safe" while historical says "dangerous"?

**What it forces you to learn:**
- Fat tails in action: parametric consistently underestimates tail risk
- Decay-weighted is a middle ground — faster than fixed-window, less noisy than short-window
- Where do the three methods disagree most? (Answer: after volatility spikes — parametric adapts instantly via $\sigma$, historical lags, decay-weighted is between)

**Output artifact:** Notebook with 3-method comparison chart

**Time:** 2–3 hours

**Relevance to Spreadex:** Understanding which method your firm uses — and what it's missing.

---

## Project 5: Portfolio VaR — Multi-Asset

**What you build:** Historical VaR for a simple portfolio, showing the gap between "sum of individual VaRs" and "portfolio VaR."

**Input:** SPY (60%), BND (40%) — classic 60/40; or customize to match Spreadex's mix

**Features:**
- Compute portfolio daily returns from weighted individual returns
- Historical VaR on portfolio-level returns (correct method)
- Compare to: sum of individual VaRs (overestimates — assumes correlation = 1)
- Compare to: parametric portfolio VaR using estimated covariance matrix
- Show diversification benefit: "Portfolio VaR is X% lower than the sum of individual VaRs"

**What it forces you to learn:**
- Portfolio VaR ≠ sum of individual VaRs (unless everything is perfectly correlated)
- Historical VaR on portfolio returns implicitly captures diversification
- Parametric portfolio VaR requires estimating a covariance matrix — and that estimate can be wrong

**Output artifact:** Notebook with portfolio VaR + diversification analysis

**Time:** 2–3 hours

**Relevance to Spreadex:** Directly applicable. Your room holds multi-asset exposure. This is how you'd measure overall risk.

---

## Project 6 (Stretch): Volatility-Scaled Historical VaR

**What you build:** Implement the vol-scaling mitigation from file 006 and test whether the shape-stability assumption holds.

**Input:** SPY returns, with known regime changes

**Features:**
- Compute rolling realized vol (e.g., 20-day)
- Scale all historical returns to current vol level
- Compare vol-scaled VaR to raw historical VaR
- Test: before/after COVID, does the shape actually stay stable?
  - Compute skew and kurtosis in the pre-COVID and post-COVID samples
  - Are they different? If so, vol-scaling assumption is violated.

**What it forces you to learn:**
- Whether the vol-scaling mitigation actually works on real data
- How to test the shape-stability assumption empirically
- The limits of mitigation — you can't fix a structural break by rescaling

**Output artifact:** Notebook with shape-stability analysis

**Time:** 2–3 hours

---

## Recommended Sequence

```
Project 1 (Calculator) → foundation, 1-2 hrs
    ↓
Project 4 (Method Comparison) → see divergence, 2-3 hrs
    ↓
Project 2 (Multi-Window Dashboard) → production monitoring pattern, 2-3 hrs
    ↓
Project 3 (Backtesting) → validate what you built, 2-3 hrs
    ↓
Project 5 (Portfolio VaR) → expand to multi-asset, 2-3 hrs
    ↓
Project 6 (Vol Scaling, stretch) → test mitigations, 2-3 hrs
```

Total: ~12–16 hours. You come out the other side with a working risk toolkit and the ability to talk about VaR like someone who's actually built it.

---

## What Calls to You?

1. Start with **Project 1** (the calculator) — get something working fast, then layer on?
2. Jump to **Project 2** (dashboard) — more visual, more immediately useful?
3. Start with **Project 5** (portfolio VaR) — most directly relevant to Spreadex?
4. Something else entirely?
