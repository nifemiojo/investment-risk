# LaTeX Formula Update Summary

**Date:** 2026-07-03  
**Update:** All teaching session files converted to use LaTeX ($$) format for equations

---

## Files Updated

1. **022_component-2-time-horizon.md**
   - Square root of time rule: $$\sigma_{10\text{-day}} = \sigma_1 \times \sqrt{10}$$
   - VaR scaling: $$\text{VaR}_{10\text{-day}, 95\%} = 1.85\% \times \sqrt{10} \approx 5.85\%$$

2. **021_sample-statistic-vs-prediction.md**
   - Stationarity hypothesis: $$H_0: F(R_t) = F(R_{t+1})$$
   - Quantile relationship: $$\text{Quantile}_{\text{past}} \approx \text{Quantile}_{\text{future}}$$

3. **023_monthly-data-vs-scaled-daily.md**
   - Monthly scaling: $$\text{Monthly VaR} = -1.85\% \times \sqrt{21} = -8.47\%$$
   - Independence assumption: $$P(R_t \mid R_{t-1}) = P(R_t)$$

4. **025_underlying-data-and-time-horizons.md**
   - 10-day scaling: $$\text{Scale: } -1.85\% \times \sqrt{10} = -5.85\%$$
   - Direct comparison formulas now render as equations

5. **017_precise-var-definition.md**
   - Time horizon notation: $$\text{VaR}_h = \text{Value at Risk over horizon } h$$
   - Where $$h = 1 \text{ day}, 10 \text{ days}, 1 \text{ month}, \ldots$$

6. **019_component-1-the-loss-deep.md**
   - Portfolio returns: $$\text{Return} = \frac{V_1 - V_0}{V_0}$$
   - Loss definition: $$\text{Loss (as positive)} = -\text{Return} = \frac{V_0 - V_1}{V_0}$$

7. **026_component-4-model-assumption.md**
   - Stationarity formality: $$F(R_t) = F(R_{t+1}) = F(R_{t+h})$$

---

## Rendering Notes

- All formula blocks now use `$$..$$` (inline/block LaTeX)
- Should render properly in Markdown viewers that support LaTeX (most modern platforms)
- Formulas will appear as professional mathematical equations, not as plain text within code blocks

---

## Next: Component 3 Deep-Dive

Ready to explore **Confidence Level** (95% vs 99% vs 99.9%)?

This will complete your core VaR definition:
- ✅ Component 1: The Loss
- ✅ Component 2: Time Horizon
- ✅ Component 3: Underlying Data
- ✅ Component 4: Model Assumption
- ⚠️ Confidence Level: Why these specific thresholds?
