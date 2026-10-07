# Notebook 15b Implementation — Asymmetric Blend Refinement

**Date:** 2026-07-24
**Topic:** Refining the correlation-adjusted VaR blend — asymmetric and sigmoid alternatives
**Turn:** 022

## User request

Implement notebook 15b as specified in the lesson plan — asymmetric blend refinement building on findings from notebooks 13b and 15.

## Work and response

### What was built

Notebook 15b (`notebooks/15b_asymmetric_blend_refinement.ipynb`) — refines the correlation-adjusted VaR blend from Notebook 15 with three improvements:

**Part A: The problem with symmetric blending**
- Quantified: 48.8% of symmetric adjustments are in the wrong direction (ratio < 1, correlation falling, VaR already conservative)
- Visual: α function shape shows the problematic left half

**Part B: Asymmetric blend**
- New `asymmetric_alpha(ratio, threshold, blend_max)` function — only activates when ratio > threshold
- Results: deviation +0.26% (vs symmetric +0.52%), mean α 0.695 (vs 0.567)
- Half the unnecessary adjustments eliminated

**Part C: Sigmoid blend**
- New `sigmoid_alpha(ratio, threshold, steepness)` function — gentle near threshold, aggressive at tails
- Result: similar to symmetric — sigmoid offers no additional benefit for this pair/period

**Part D: Speed vs noise — parameter sweep**
- Asymmetric sweep: threshold × blend_max (24 combos)
- Sigmoid sweep: threshold × steepness (25 combos)
- Best asymmetric config (thresh=1.2, max=3.0): deviation **+0.05%** — beats baseline (+0.16%)
- Visual: deviation vs % adjusted curves show sweet spot

**Part E: Six design principles**
1. Three-component framework is robust
2. Asymmetric > symmetric
3. Ratio is staleness diagnostic, not leading indicator (from 13b)
4. Non-linear respects signal structure
5. Sweet spot exists — more adjustment ≠ better
6. Parameters are empirical, not theoretical

**Part F: Practical recommendations**
- Recommendation table: when to use each blend
- Spreadex context
- When to re-calibrate
- Limitations

### Key result

The asymmetric blend with the right parameters **beats baseline** on breach calibration (+0.05% deviation vs baseline's +0.16%). The approach works — it just needs the right calibration and the foresight to only adjust in one direction.

### Files

- Created: `notebooks/15b_asymmetric_blend_refinement.ipynb`
- Updated: `.hermes/plans/2026-07-21_portfolio-var-lesson-plan.md` (status, 15b entry, sequence)

## Next step

Notebook 16 (n-asset generalisation) or user review of 14 and 15b.
