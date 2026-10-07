# VaR Practical Roadmap: From Theory to Production Understanding

**Date:** 2026-07-10
**Topic:** Integrated practical roadmap spanning all three VaR methods, single-position to portfolio, with Spreadex investigation and external artifacts

---

## The Goal

By the end of this roadmap, you will:

1. **Build** all three VaR methods from scratch for single assets and portfolios
2. **Break** each method deliberately — force failure modes to surface
3. **Fix** the most important failures with mitigations
4. **Investigate** what Spreadex actually does, find the gaps, document them
5. **Externalize** everything into GitHub repositories and published writeups

---

## Phase 1: Single-Asset VaR Toolkit

**Goal:** Build a clean, tested Python library implementing all three methods for a single position. This is the foundation.

### 1A: Historical VaR Calculator

```
Input:  Ticker + position size + window + confidence level
Output: VaR number + rolling VaR series
```

**What to build:**
- `historical_var(returns, window, confidence)` — clean function
- Parametrized window (60d, 252d, 504d)
- Parametrized confidence (95%, 99%)
- Both percentile conventions (nearest-rank, linear interpolation) with comparison
- Rolling VaR series output for visualization

**Failure modes to surface:**
- Window cliff: show what happens when a big day drops out of the window
- Sample size sensitivity: 60d vs 252d vs 504d on the same data
- Regime change lag: how long after a volatility spike does 252d VaR catch up?

**Artifact:** `var-toolkit/historical.py` in a GitHub repo

---

### 1B: Parametric VaR Calculator

```
Input:  Ticker + position size + window + confidence + distribution
Output: VaR number + rolling VaR series
```

**What to build:**
- `parametric_var(returns, window, confidence, dist='normal')` 
- Normal distribution (standard)
- Student's t distribution (fatter tails)
- Cornish-Fisher expansion (skew + kurtosis correction)
- EWMA volatility (λ = 0.94) as alternative to equal-weighted

**Failure modes to surface:**
- Normality assumption: show how parametric VaR diverges from historical when returns are fat-tailed
- Mean noise: compare with μ=0 vs estimated μ̂
- Volatility time-variation: equal-weighted vs EWMA divergence during vol spikes
- Distribution sensitivity: normal vs t vs Cornish-Fisher on the same data

**Artifact:** `var-toolkit/parametric.py`

---

### 1C: Monte Carlo VaR Calculator

```
Input:  Ticker + position size + horizon + confidence + model spec
Output: VaR number + diagnostic plots
```

**What to build:**
- `monte_carlo_var(returns, horizon, confidence, n_paths, model='garch')`
- Simple distribution sampling (normal, t) — converges to parametric
- GARCH(1,1) simulation — 1-day and 10-day horizons
- Shock distribution choice (normal, t, skewed-t)
- Diagnostic: convergence plot (VaR vs number of paths)
- Diagnostic: Monte Carlo standard error

**Failure modes to surface:**
- Sampling error: same parameters, different seeds → different VaR
- Path count sensitivity: 100 vs 1,000 vs 10,000 vs 100,000 paths
- GARCH vs fixed-σ̂: show the difference in VaR after calm vs crash days
- 10-day √10 vs simulated: show the gap when GARCH has persistence

**Artifact:** `var-toolkit/monte_carlo.py`

---

### 1D: Method Comparison Dashboard

**What to build:**
- Single script that runs all three methods on the same data
- Rolling comparison over time: all three VaR series on one chart
- Divergence indicator: when do the methods disagree most?
- Table: "On [date], historical said X, parametric said Y, Monte Carlo said Z"

**Key insight to extract:**
- Parametric is fastest to react (σ̂ updates daily)
- Historical is slowest (window must fill with new data)
- Monte Carlo with GARCH is between them (conditional on current state, but parameter-dependent)

**Artifact:** `var-toolkit/compare.py` + visualization notebook

---

## Phase 2: Breaking Things Deliberately

**Goal:** For each method, construct scenarios where it fails, quantify the failure, and test mitigations.

### 2A: Historical VaR — Regime Change Stress Test

**Setup:** Use SPY data spanning COVID (2019–2021). Run 252d historical VaR.

**Break it:**
- Show VaR on Feb 19, 2020 (last calm day): what does the model say?
- Show actual returns Feb 20 – Mar 23, 2020: how many breaches?
- The window cliff: when does the COVID crash enter the 252d window? When does it exit?

**Test mitigations:**
- Decay weighting (λ = 0.94): does it catch the vol spike faster?
- Vol scaling: rescale historical returns to current vol — does it help?
- Multi-window: 60d catches the spike; 252d provides stability

**Artifact:** `var-toolkit/tests/break_historical.py` + analysis writeup

---

### 2B: Parametric VaR — Fat Tails and Vol Clustering

**Setup:** Use an asset with known fat tails (single stocks, crypto, or commodities).

**Break it:**
- Compute 95% and 99% parametric VaR assuming normality
- Backtest: count breaches at both confidence levels
- 95% should have ~5% breaches; 99% should have ~1%
- For fat-tailed assets, 99% breaches are much higher than 1% — the model is dangerously wrong at the tail

**Test mitigations:**
- Student's t: does ν=4 or ν=5 fix the breach rate?
- Cornish-Fisher: does the skew+kurtosis correction help?
- Compare: which mitigation gives breach rates closest to expected?

**Artifact:** `var-toolkit/tests/break_parametric.py` + analysis writeup

---

### 2C: Monte Carlo VaR — Model Risk Amplification

**Setup:** Fit GARCH to SPY, then simulate 10-day VaR.

**Break it:**
- Parameter sensitivity: vary α and β within their standard errors. How much does 10-day VaR change?
- Shock distribution: compare normal vs t(5) vs t(3) — how much wider is 10-day VaR?
- Path count: 1,000 vs 10,000 vs 100,000 — what's the standard error at each?
- Seed sensitivity: run 10 times with different seeds. What's the range of VaR estimates?

**Test mitigations:**
- Antithetic variates: does it reduce the standard error?
- Importance sampling: oversample the tail — more stable 99% VaR?
- Parameter uncertainty: bootstrap the GARCH estimation, report VaR confidence intervals

**Artifact:** `var-toolkit/tests/break_monte_carlo.py` + analysis writeup

---

### 2D: The Backtesting Gauntlet

**What to build:** A unified backtesting framework that works for all three methods.

**Features:**
- Rolling out-of-sample VaR forecasts (no look-ahead bias)
- Breach counting and breach rate comparison
- Kupiec test (unconditional coverage)
- Christoffersen test (breach independence)
- Breach clustering visualization
- Summary table: "Method X had Y breaches (expected Z), p-value = W"

**The gauntlet:** Run all three methods through the same backtest on the same data. Which survives? Which fails?

**Artifact:** `var-toolkit/backtest.py`

---

## Phase 3: Portfolio VaR

**Goal:** Extend from single-asset to multi-asset portfolios. Show how diversification changes everything.

### 3A: Historical Portfolio VaR

**What to build:**
- Portfolio return = weighted sum of individual returns
- Historical VaR on the portfolio return series
- Compare: sum of individual VaRs vs portfolio VaR (diversification benefit)
- Rolling correlation between assets: when does it spike?

**Break it:**
- 2022: stocks and bonds both fell. Correlation went positive. Show the diversification benefit evaporating.
- The window problem: the correlation matrix in the 252d window lags the true correlation shift

**Artifact:** `var-toolkit/portfolio.py`

---

### 3B: Parametric Portfolio VaR

**What to build:**
- Covariance matrix estimation from returns
- Portfolio variance: $w^T \Sigma w$
- Portfolio VaR: $\mu_p - z_\alpha \cdot \sigma_p$
- Marginal VaR: contribution of each position
- Component VaR: fraction of total VaR from each position

**Break it:**
- Correlation matrix estimation error: with 5 assets, how many unique correlations? (10). With 50 assets? (1,225). Estimation error grows fast.
- 2022 correlation regime change: does the covariance matrix capture the stock-bond correlation flip?

**Test mitigations:**
- Shrinkage: Ledoit-Wolf shrinkage toward constant correlation
- EWMA covariance: gives more weight to recent observations

**Artifact:** `var-toolkit/portfolio.py` (extended)

---

### 3C: Monte Carlo Portfolio VaR

**What to build:**
- Cholesky decomposition of covariance matrix ($\Sigma = LL^T$)
- Generate correlated random shocks: $\epsilon_{correlated} = L \cdot z$
- Multi-asset GARCH simulation (if feasible — this gets complex)
- Compare simple MC (fixed covariance) vs GARCH MC (time-varying covariance)

**Break it:**
- Correlation breakdown: run MC with pre-2022 correlations, then test on 2022 data
- Dimensionality: how many parameters in a 5-asset GARCH model? (5 × 3 GARCH params + 10 correlations = 25+). Estimation is fragile.

**Artifact:** `var-toolkit/portfolio.py` (extended)

---

## Phase 4: Spreadex Investigation

**Goal:** Understand what's actually happening in production, find the gaps, document them.

### 4A: Current State Assessment

**Questions to answer (through code inspection, documentation, and conversations):**

| Question | How to Answer |
|---|---|
| What VaR method does the autohedge system use? | Read the codebase, trace the VaR calculation |
| What distribution? What window? What confidence level? | Extract parameters from config or code |
| Is it single-asset VaR or portfolio VaR? | Check if correlations are factored in |
| Is it 1-day or multi-day? | Check the horizon parameter |
| How often is the model recalibrated? | Check for scheduled jobs or manual triggers |
| What happens when VaR is breached? | Read the alert/action logic |
| Who can override the model? | Check for manual override flags |
| What backtesting exists? | Search for breach monitoring or validation code |

**Output:** Internal document: "Spreadex VaR: Current State" — factual, not judgmental

### 4B: Gap Analysis

**Compare current state to what you now know is possible:**

| Gap | Severity | Business Impact |
|---|---|---|
| Normal assumption when data is fat-tailed | High | VaR breaches 2-3× expected at 99% |
| Fixed window misses vol clustering | Medium | Slow to react to crisis onset |
| No multi-window comparison | Medium | Can't distinguish regime change from noise |
| No backtesting dashboard | High | Model could be wrong for months |
| No correlation stress testing | Medium | Diversification benefit assumed, not tested |

**Output:** Internal document: "Spreadex VaR: Gaps and Recommendations"

### 4C: What the Business Actually Cares About

**Not all failure modes matter to the business. Find out which ones do:**

- Talk to traders: "What's the worst VaR failure you've seen? What did it cost?"
- Talk to risk managers: "What keeps you up at night about the VaR model?"
- Look at P&L events: "When did the room lose money unexpectedly? Was VaR warning us?"

**The business cares about:**
- VaR breaches that cost real money
- False alarms that triggered unnecessary hedging costs
- Model failures that were visible in hindsight but not caught in real-time
- How to translate VaR into business outcomes

**Output:** Internal document: "What Spreadex Actually Cares About"

---

## Phase 5: Investment Management Context

**Goal:** Understand how VaR is used differently in investment management vs dealer/market-making.

### Key Differences to Investigate

| Dimension | Dealer (Spreadex) | Investment Manager (AQR, etc.) |
|---|---|---|
| **VaR purpose** | Exposure monitoring, hedge trigger | Risk budgeting, position sizing, client reporting |
| **Horizon** | 1-day (can hedge tomorrow) | Multi-day to monthly (positions take time to adjust) |
| **Portfolio** | Client flow-driven, constantly changing | Strategy-driven, deliberate construction |
| **VaR use** | "Are we within limits?" | "How much risk budget should this strategy get?" |
| **Failure consequence** | Unhedged exposure → P&L loss | Risk budget exceeded → forced deleveraging |
| **Who cares** | Traders, risk managers, CFO | PMs, CIO, clients, consultants |

### What to Build

- A risk budgeting example: "Given a 60/40 portfolio with 10% risk budget, how do you allocate VaR across assets?"
- A volatility targeting overlay: "Scale positions so portfolio vol stays at 10%"
- A scenario: "A pension fund has £100M. Their risk budget is 8% annual vol. How much can they allocate to equities vs bonds vs alternatives?"

**Artifact:** `var-toolkit/investment-management/` — examples and writeup

---

## Phase 6: Externalization

**Goal:** Every piece of work produces two outputs: the internal deliverable AND an external, portable artifact.

### GitHub Repository: `var-toolkit`

```
var-toolkit/
├── README.md                    # Overview, installation, quickstart
├── historical.py                # Historical VaR + decay-weighted
├── parametric.py                # Parametric VaR (normal, t, Cornish-Fisher)
├── monte_carlo.py               # Monte Carlo VaR (distribution + GARCH)
├── portfolio.py                 # Portfolio VaR (all three methods)
├── backtest.py                  # Backtesting framework
├── compare.py                   # Method comparison dashboard
├── notebooks/
│   ├── 01_single_asset.ipynb    # Walkthrough: all methods on SPY
│   ├── 02_breaking_things.ipynb # Failure mode demonstrations
│   ├── 03_portfolio.ipynb       # Multi-asset portfolio VaR
│   ├── 04_backtesting.ipynb     # Full backtesting gauntlet
│   └── 05_investment_mgmt.ipynb # Risk budgeting, vol targeting
├── tests/
│   ├── break_historical.py
│   ├── break_parametric.py
│   └── break_monte_carlo.py
└── data/                        # Cached data for reproducibility
```

### Published Writeups

Each writeup is a standalone piece that demonstrates understanding:

1. **"Three Ways to Measure Risk: Historical, Parametric, and Monte Carlo VaR"** — educational, code-heavy, comparison-focused
2. **"When VaR Fails: A Systematic Catalog of Failure Modes"** — synthesis of all three methods' failure modes with real data
3. **"Volatility Clustering and VaR: Why Yesterday Matters"** — GARCH, conditional VaR, the oil shock example
4. **"Risk Budgeting for Systematic Portfolios"** — investment management application

---

## Sequencing

```
Week 1-2: Phase 1A (Historical) + 1B (Parametric)
Week 3-4: Phase 1C (Monte Carlo) + 1D (Comparison)
Week 5-6: Phase 2A (Break Historical) + 2B (Break Parametric)
Week 7-8: Phase 2C (Break Monte Carlo) + 2D (Backtesting)
Week 9-10: Phase 3 (Portfolio VaR)
Week 11-12: Phase 4 (Spreadex Investigation)
Week 13-14: Phase 5 (Investment Management) + Phase 6 (Externalization)
```

Total: ~14 weeks. Each phase produces artifacts that feed the next.

---

## Check-In

This is the full roadmap. Three questions:

1. **Scope:** Does this cover everything you want? Anything missing?
2. **Pacing:** Do you want to start with Phase 1 (building the toolkit) or jump to Phase 4 (Spreadex investigation) first?
3. **Environment:** Are you ready to set up the sandbox Python environment and pull some data? Or do you want to sketch the code structure first?