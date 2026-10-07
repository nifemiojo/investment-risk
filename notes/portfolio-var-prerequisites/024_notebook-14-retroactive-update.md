# Notebook 14 Retroactive Update — Integrating 15b Findings

**Date:** 2026-07-24
**Topic:** Updating the portfolio VaR dashboard to use the refined asymmetric blend
**Turn:** 024

## User request

Retroactively update notebook 14 (Portfolio VaR Dashboard) with the findings from notebook 15b to better reflect the overall findings and help a real decision maker.

## Changes made

### Code changes

- **Parameters:** Replaced `RATIO_THRESHOLD = 1.5` / `BLEND_MAX_RATIO = 2.5` with `ASYM_THRESHOLD = 1.2` / `ASYM_BLEND_MAX = 3.0` (optimal from 15b sweep)
- **compute_alpha function:** Replaced the symmetric `compute_alpha(ratio, threshold, blend_max)` with the asymmetric `asymmetric_alpha(ratio, threshold, blend_max)` — only activates when ratio > threshold
- **Adjusted VaR computation:** Now uses the asymmetric function with the new parameters
- **Snapshot cell:** Added correlation direction indicator ("↑ rising (VaR understated)" or "↓ falling (VaR conservative)")

### Narrative changes

- **Opening:** Added reference to Notebook 15b refinement
- **Part D intro:** Described the asymmetric approach — only adjusts when correlation is rising
- **Part D interpretation table:** Updated "Quick read" column to note asymmetry — only adjust when ratio is above 1
- **Part D interpretation:** Added explicit paragraph about the 15b finding (asymmetric beats baseline)
- **Part E escalation ladder:** Adjusted thresholds to match new parameters, added design principle about credibility
- **Part F (Spreadex):** Updated the walk-through to mention asymmetric activation at 1.2
- **Part F (FINBOURNE):** Added credibility argument — asymmetric only activates when there's a real reason
- **Part F (limitations):** Added "Parameters are asset-specific" row, referencing the 15b sweep
- **Key takeaways:** Complete rewrite — 7 takeaways incorporating 13b and 15b findings

### Results

| Metric | Before (symmetric) | After (asymmetric) |
|--------|-------------------|-------------------|
| Mean VaR | 1.201% | 1.155% |
| Breaches | 85 (4.48%) | 94 (4.95%) |
| Deviation | +0.52% | **+0.05%** |
| Baseline wins? | Yes | **No — adjusted wins** |
| Days adjusted | 67.5% | 47.6% |
| Mean α | 0.567 | 0.793 |

The adjusted VaR now beats baseline on breach calibration, the number of days adjusted is in the sweet spot (~48%), and the adjustment only activates when correlation is actually rising — making it credible to a decision maker.

## Next step

Both notebooks 14 and 15b now tell a consistent story. Notebook 16 (n-asset) is the remaining item.
