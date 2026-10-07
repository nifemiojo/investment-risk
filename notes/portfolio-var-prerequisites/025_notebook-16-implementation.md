# Notebook 16 Implementation — n-Asset Generalisation

**Date:** 2026-07-24
**Topic:** Scaling the portfolio VaR framework from 2 to n assets
**Turn:** 025

## User request

Build notebook 16 following the detailed design spec in the plan — 3-asset SPY/BND/GLD with pairwise correlation matrix, drop-one-out benefit decomposition, and three aggregation methods for the adjusted VaR.

## What was built

Notebook 16 (`notebooks/16_n_asset_generalisation.ipynb`) — the final notebook in the historical portfolio VaR phase.

### Structure: 6 parts

**Part A: Data pipeline — scaling is trivial**
- SPY/BND/GLD at 40/30/30, 1,898 VaR observations
- All five VaR methods work without modification (demonstrated, not re-computed to keep notebook focused)

**Part B: Pairwise correlation matrix**
- 3 pairwise ratios computed: SPY-BND, SPY-GLD, BND-GLD
- Three-line chart + "most extreme pair" tracker
- Shows which pair dominates the correlation regime at any point

**Part C: Drop-one-out benefit decomposition**
- Full 3-asset benefit: 33.8% mean
- Without SPY: 11.2% (SPY is the biggest single contributor at +22.6pp)
- Without BND: 27.4% (BND adds +6.4pp)
- Without GLD: 17.6% (GLD is the diversification workhorse at +16.2pp)

**Part D: Three aggregation methods**
- Max ratio: α=0.670, 941 days adjusted, breach 3.69%
- Weighted avg: α=0.817, 796 days adjusted, breach 4.43%
- Min α: α=0.567, 1,548 days adjusted, breach 3.27%
- Weighted avg wins but all over-correct — supporting the thesis

**Part E: What scales and what doesn't**
- Summary table: 7 concepts, 2 → n comparison, assessment column
- Honest explanation of why adjusted VaR aggregation gets fragile

**Part F: Practical recommendations**
- Per-portfolio-size recommendation table (2 → 3 → 4-10 → 10+)
- When to automate vs use judgment

### Key findings

- 3-asset benefit (33.8%) dwarfs 2-asset (16.3%) — GLD adds substantial diversification
- GLD is the diversification workhorse; BND contributes the least marginally
- All aggregation methods over-correct for 3 assets — the fragility thesis holds
- The correlation matrix as a monitoring dashboard is more valuable than an automated blend for larger n

## Phase complete

All 8 notebooks in the historical portfolio VaR phase are built and executed:
12 (benefit) → 13 (correlation dynamics) → 13b (lead-lag) → 15 (symmetric blend) → 15b (asymmetric refinement) → 14 (dashboard) → 16 (n-asset)

Next phase: parametric portfolio VaR, Monte Carlo, or other topics per the broader roadmap.
