# Historical VaR Session Summary — Handover

**Date:** 2026-07-06
**Session folder:** `./sessions/var-methods-historical/`
**Status:** Conceptual foundation complete. Ready to start implementation.

---

## What We Covered (9 Files)

| File | Topic | Key Takeaway |
|---|---|---|
| 001 | Core idea | Historical VaR = sort past returns, read the pth percentile. No formulas, no distribution assumptions. |
| 002 | Percentile conventions | Nearest rank (ceil) vs linear interpolation. Latter is production standard. |
| 002b | Indexing clarification | Nearest rank maps first obs to cover 0→1/n; interpolation maps it to exactly 0th percentile. |
| 003 | Convention + sample size | Use interpolation. 252-day window is baseline. Accuracy (sample) > precision (convention). |
| 004 | Why 252 days | 365 − 104 weekends − 9 holidays ≈ 252. One annual cycle of market behavior. |
| 005 | Sample size trade-offs | Short = reactive but noisy. Long = stable but stale. Regime-change examples with concrete numbers. |
| 006 | Production mitigations | Decay weighting (λ=0.94), vol scaling (rescale to current σ), multi-window dashboard. |
| 007 | Strengths | Non-parametric captures fat tails. Zero parameters. Explainable. Implicit multi-asset correlation. |
| 008 | Distribution shape | Location + Scale + Shape (skew, kurtosis, multimodality). Vol scaling assumes shape stable — testable. |
| 009 | Project scoping | 6 projects sequenced: Calculator → Method Comparison → Dashboard → Backtesting → Portfolio → Vol Scaling. |

---

## Key Concepts Internalized

- Historical VaR is non-parametric — it lets the data speak, fat tails and all
- The only "parameter" is the window size, and it's a bias-variance trade-off
- The stationarity assumption is the real bet — it breaks at regime changes, and every mitigation (decay weighting, vol scaling, multi-window) is a partial fix
- Distribution shape (skew, kurtosis) is what parametric VaR misses and historical VaR captures
- Production systems don't use a single VaR number; they use dashboards with multiple windows and methods

---

## Where We Left Off

User chose to move from theory to practice. Six projects scoped (file 009). Recommended starting point: **Project 1 — Single-Asset Historical VaR Calculator**.

Next session should:
1. Set up the sandbox Python environment
2. Pull SPY data via yfinance
3. Implement the core historical VaR function
4. Test with different windows and confidence levels
5. Verify against manual calculation for a small sample

---

## User Preferences Active

- Auto-save all responses to `./sessions/<topic>/NNN_*.md` (skill: `teaching-session-logging`)
- LaTeX: `$$...$$` for display math, `$...$` for inline math (never `$$...$$` inline)
- Sandbox miniconda env for Python work
- Notebooks (.ipynb) for demos/non-prod
- Socratic teaching style: find hazy concept, drill depth over breadth
