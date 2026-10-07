# Session Summary — Portfolio VaR Prerequisites & Implementation

**Date:** 2026-07-22
**Session:** Module 1 prerequisites + Notebooks 12, 13, 15

---

## Overview

Completed the conceptual foundation for portfolio historical VaR (Module 1) and built three notebooks extending the single-asset toolkit to a 60/40 SPY/BND portfolio. Established teaching principles for going forward.

---

## Session files created (17 files)

All at `/home/femi/femi-corp/areas/finance/sessions/portfolio-var-prerequisites/`:

| File | Topic | Key takeaway |
|------|-------|-------------|
| 001 | Portfolio return = weighted sum | $r_p = \sum w_i r_i$, P&L-sum intuition |
| 002 | Derivation + diversification in distribution | $r_p$ series encodes correlation through day-by-day pairings |
| 003 | Intuition: position P&L, volume knobs | Three mental models for the weighted sum |
| 004 | Covariance and correlation defined | Cov = co-deviation from means; ρ = standardised cov |
| 005 | Covariance relative to individual means | Both-above-mean and both-below-mean both give + product |
| 006 | Covariance: direction + magnitude | Two-dimensional signal in one number |
| 007 | Diversification benefit formula | $(w_1\text{VaR}_1 + w_2\text{VaR}_2 - \text{VaR}_p) / (w_1\text{VaR}_1 + w_2\text{VaR}_2)$ |
| 008 | Scale contamination in covariance | Same ρ, different σ → different Cov. ρ fixes this |
| 009 | When covariance is actually useful | For computation (portfolio variance, beta), not comparison |
| 010 | Correlation breakdown during crises | 252d ρ lags reality by months; 60d ρ adapts faster |
| 011 | Naive sum derivation from portfolio variance | At ρ=+1: $\sigma_p = w_1\sigma_1 + w_2\sigma_2$ |
| 012 | Naive sum in historical VaR | Percentile of weighted sum ≠ weighted sum of percentiles |
| 013 | Worked 10-day example | Day 5 vs Day 8: why alignments matter |
| 014 | Notebook 12 design | Structure, cells, decisions |
| 015 | What ρ = +1 means for naive sum | Rank ordering preserved → worst days align |
| 016 | Diversification benefit in practice | Three regimes, leading indicator, use cases |
| 017 | Correlation-reactive VaR systems | Three approaches: window switch, blend, monitoring |

---

## Notebooks built

### Notebook 12 — Portfolio Returns & Diversification Benefit ✅
**Path:** `projects/historical-var/notebooks/12_portfolio_diversification_benefit.ipynb`
**Status:** Built and executed. Part D updated with practical content.

**Key results (SPY/BND 60/40, 2018-2025):**

| Metric | Value |
|--------|-------|
| Portfolio VaR (95%) | 1.10% |
| Naive sum (ρ = +1) | 1.27% |
| Diversification benefit | 13.6% |
| Rolling benefit mean | 16.3% |
| Rolling benefit min | 3.8% (Jun 2021) |
| Rolling benefit max | 31.6% (Nov 2024) |
| Breach rate | 5.17% (expected 5.00%) |

**Regime breakdown:**

| Period | Avg Benefit | Min Benefit |
|--------|------------|-------------|
| Pre-COVID (2019) | 15.0% | 9.9% |
| COVID crash | 19.1% | 16.4% |
| Recovery (2021) | 12.3% | **3.8%** |
| Rate-hiking (2022) | 14.8% | 9.0% |
| Recent (2024-2025) | 23.4% | 14.1% |

---

### Notebook 13 — Correlation Dynamics ✅
**Path:** `projects/historical-var/notebooks/13_correlation_dynamics.ipynb`
**Status:** Built and executed. Includes Spreadex + FINBOURNE context.

**Key results:**

| | 252-day ρ | 60-day ρ |
|---|----------|---------|
| Mean | +0.10 | +0.05 |
| Min | −0.41 | −0.55 |
| Max | +0.39 | +0.71 |
| **Latest** | +0.30 | **+0.56** |

31.8% of days had |gap| > 0.2 between fast and slow estimates.

**Correlation ratio at key dates:**

| Date | Event | 252d ρ | 60d ρ | Ratio | Benefit |
|------|-------|--------|-------|-------|---------|
| Jun 2021 | Benefit min | +0.14 | +0.32 | 2.32 | 3.8% |
| Oct 2022 | CPI peak | +0.22 | +0.52 | 2.32 | 14.3% |
| Nov 2024 | Benefit max | +0.15 | **−0.11** | −0.71 | 31.6% |
| **Latest** | | +0.30 | **+0.56** | **1.86** | 14.9% |

**Latest signal:** Ratio = 1.86 — 60d correlation well above 252d. Diversification benefit declining from Nov 2024 peak. Watch.

---

### Notebook 15 — Correlation-Adjusted VaR Experiment ✅
**Path:** `projects/historical-var/notebooks/15_correlation_adjusted_var.ipynb`
**Status:** Built and executed. Three-component framework: baseline + detector + blend rule.

**Key finding:** Adjusted VaR improves breach calibration during strong correlation shifts (6.36% → 4.89% breaches), but symmetric blend is too conservative when fast correlation is more negative than slow. Refinement needed: asymmetric blend (only adjust when correlation is *rising*, not falling).

**Parameter sweep result:** Best threshold = 2.5 (22% of days adjusted), deviation +0.20% vs baseline +0.22%.

---

## Key mental models built

1. **Percentile of weighted sum ≠ weighted sum of percentiles** — the naive sum assumes rank ordering is preserved (ρ = +1). Reality breaks this.

2. **Portfolio return series as information compression** — each day's $r_p$ compresses the interaction; the distribution of $r_p$ reveals the diversification.

3. **Stable baseline + fast detector + blend rule** — the unifying pattern across all reactive VaR approaches. Multi-window divergence, diversification benefit, correlation ratio — all instances.

4. **Two-number story** — VaR = how much. Diversification benefit = how reliable. Neither alone tells the full story.

5. **Correlation as leading indicator** — benefit drops (ρ shifts) → then VaR catches up. Benefit hit 3.8% in Jun 2021, 6+ months before 2022 rate hikes.

6. **Covariance vs correlation** — covariance for computation (has units, scale matters), correlation for comparison (unitless, bounded).

---

## Teaching principles established this session

1. **Always include the "so what"** — practical use cases in relevant contexts (Spreadex live trading, FINBOURNE institutional reporting, personal toolkit development).

2. **Roadmap includes n-asset generalisation** — after 2-asset work is solid, extend to 3+ assets and general n-asset case.

---

## Remaining topics

### Immediate next
- **Notebook 14** — Portfolio VaR dashboard (all methods: equal, decay, vol-scaled, combined, multi-window on portfolio returns + diversification benefit + correlation ratio)
- **Notebook 15 refinement** — Asymmetric blend (only adjust when correlation is *rising*)

### Deferred to later phases
- Parametric portfolio VaR (covariance matrix method)
- Monte Carlo portfolio VaR
- Covariance shrinkage or robust estimation
- Portfolio optimisation / risk budgeting
- Multi-day horizon portfolio VaR
- Copulas or tail dependence

### n-Asset generalisation (future Notebook)
- 3+ asset portfolio (SPY/BND/GLD)
- Generalise naive sum: $\sum w_i \text{VaR}_i$
- Pairwise correlation matrix and its dynamics
- Which pairs are driving the benefit change?
- Marginal diversification contribution per asset

---

## Connection to broader learning arc

This session bridges single-asset historical VaR (Notebooks 01-11) to multi-asset portfolio risk. The core insight — portfolio VaR ≠ sum of individual VaRs — unlocks the diversification benefit as both a measurement and a monitoring signal.

This connects directly to:
- **Career direction:** systematic multi-asset investing, portfolio construction, risk management
- **Spreadex work:** multi-asset book monitoring, live risk systems
- **FINBOURNE experience:** institutional VaR models
- **Future topics:** risk budgeting, factor investing, alternative risk premia

The pattern established here ("stable baseline + fast detector + blend rule") will recur across all systematic risk monitoring the user builds going forward.

---

## User preferences (reconfirmed / newly established)

- Prefers consultative approach: design before code
- Wants practical "so what" framing in all teaching
- Sessions folder at `/home/femi/femi-corp/areas/finance/sessions/<topic-slug>/`
- Sandbox: `~/.pyenv/versions/miniconda3-latest/envs/sandbox`
- Notebooks pair with session files for conceptual depth
- n-Asset generalisation is on the roadmap
- C# mental models welcome as translation bridges
- Overfitting / parameter proliferation is a concern — keep parameters defensible
