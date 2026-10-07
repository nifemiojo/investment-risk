# Notebook 14 Implementation — Portfolio VaR Dashboard

**Date:** 2026-07-24
**Topic:** Implementing the portfolio VaR dashboard notebook from the lesson plan
**Turn:** 021

## User request

Implement notebook 14 of the historical VaR project — the Portfolio VaR Dashboard — as specified in the lesson plan at `areas/finance/projects/historical-var/.hermes/plans/2026-07-21_portfolio-var-lesson-plan.md` and the handoff at `areas/finance/sessions/portfolio-var-prerequisites/HANDOFF.md`.

## Work and response

### What was built

Notebook 14 (`notebooks/14_portfolio_var_dashboard.ipynb`) — the culmination notebook combining everything from the single-asset dashboard (Notebook 11) with the portfolio-specific signals (Notebooks 12, 13, 15).

### Structure: Six parts

**Part A: The portfolio VaR dashboard**
- All five methods (equal, decay λ=0.94, fast 60d, vol-scaled, combined) on portfolio returns
- Methods table with portfolio-specific failure modes

**Part B: Method divergence as signal**
- Three signals (Ordering, Shape, Regime) — same as Notebook 11 but on portfolio returns
- Interpretation table mapping signal combinations to actions

**Part C: Three crises through the portfolio dashboard**
- COVID crash, 2022 rate hikes, Recent calm — portfolio perspective
- Key point: 2022 is where the portfolio view matters most (correlation breakdown)

**Part D: The portfolio-specific signals**
- Diversification benefit — reliability gauge
- Correlation ratio (60d/252d) — staleness detector
- Correlation-adjusted VaR — from Notebook 15's blend methodology
- Breach comparison — baseline vs adjusted

**Part E: The complete picture**
- 2×3 grid: VaR methods, benefit, correlation ratio, baseline vs adjusted, breach rates by regime, latest snapshot
- Escalation ladder — portfolio edition (green/yellow/orange/red)

**Part F: Practical interpretation**
- Spreadex context (live trading desk monitoring)
- FINBOURNE context (institutional reporting)
- Personal toolkit (template for any 2-asset pair)
- Limitations table

### Execution results

- 2,150 daily returns (2018-01-03 to 2026-07-24), 1,898 VaR observations
- Diversification benefit: mean 16.3%, min 3.8% (Jun 2021), max 31.6% (Nov 2024), latest 14.9%
- Correlation ratio: latest 1.83, mean 1.08
- Baseline VaR: mean 1.116%, breaches 5.16% (expected 5.00%)
- Adjusted VaR: mean 1.201%, breaches 4.48% (mean α = 0.57, 67.5% of days adjusted)
- Baseline is closer to expected breach rate (0.16% vs 0.52% deviation)
- The symmetric blend is conservative — baseline wins overall, which sets up Notebook 15b's asymmetric refinement

### Design decisions

- Parameterised RATIO_THRESHOLD (1.5) and BLEND_MAX_RATIO (2.5) in the Parameters cell
- £10M portfolio value (consistent with Notebook 11's £10M SPY position)
- `compute_alpha` function replicated from Notebook 15 (same implementation)
- Vol-scaled/combined loop uses `portfolio_returns` and `trailing_vol` computed on portfolio returns
- All plots use `PORTFOLIO_VALUE` for £ formatting

### Conventions followed

- Notebook structure: Parameters cell, separate Imports cell, Part A/B/C/D/E/F sections
- `sys.path.insert(0, "..")` for imports from `src/`
- Existing functions only — no new src modules needed
- LaTeX: `$$...$$` display, `$...$` inline
- Variable naming: domain-meaningful (benefit, naive_sum, ratio_aligned)
- Matplotlib only, `%matplotlib inline`, white figure background

## Next step

User reviews the notebook, asks questions, suggests improvements. After review: Notebook 15b (asymmetric blend refinement) or refinements to this notebook.
