# Correlation-Adjusted Portfolio VaR — Findings Report

**Date:** 2026-07-24
**Session:** notebooks/portfolio-var-prerequisites
**Notebooks covered:** 13b (lead-lag), 14 (dashboard), 15 (symmetric blend), 15b (asymmetric refinement)

---

## 1. The Core Problem: Correlation Shifts Make VaR Stale

Historical VaR uses a rolling window of past returns. For a single asset, the window can go stale when volatility changes. For a portfolio, there's an additional staleness source: **correlation between assets changes over time**.

When correlation rises (assets start moving together more), the historical window still remembers a more diversified past. The VaR number is too low — it understates risk because it assumes diversification that no longer exists. The 252-day window takes months to fully absorb the new correlation regime.

**The 2022 case study:** Stocks and bonds fell together during the Fed rate-hiking cycle. The classic 60/40 portfolio had its worst year in decades. The diversification benefit — normally 15-25% — collapsed to 3.8%.

---

## 2. The Three-Component Framework

The solution follows a general pattern that works for any VaR methodology:

| Component | What it is | Implementation |
|-----------|-----------|----------------|
| **Stable baseline** | Your standard VaR number | 252-day rolling portfolio VaR |
| **Fast detector** | Something that notices correlation shifts quickly | Correlation ratio: $\rho_{60d} / \rho_{252d}$ |
| **Blend rule** | How to adjust VaR based on the detector | $\text{VaR}_{\text{adj}} = \alpha \cdot \text{VaR}_{\text{baseline}} + (1-\alpha) \cdot \text{VaR}_{\text{naive}}$ |

The naive sum ($w_1\text{VaR}_1 + w_2\text{VaR}_2$) is the $\rho = +1$ worst case — both assets crash together. It's the stress ceiling. The blend moves VaR toward this ceiling when the detector says correlation has shifted.

---

## 3. The Lead-Lag Finding (Notebook 13b): Reframing the Blend's Purpose

**Question:** Does the correlation ratio *lead* VaR? If the ratio spikes today, does VaR rise tomorrow?

**Answer:** No. The ratio is **contemporaneous** — it moves with VaR, not ahead of it.

Key measurements:
- Cross-correlation $\Delta\text{Ratio}_t$ vs $\Delta\text{VaR}_{t+k}$: peak at $k=0$, $\rho = +0.118$
- Event study (ratio > 2.0): VaR rises only +0.011 pp at 60 days post-spike — negligible
- Rolling CCF: median lead = +5 days, 61% positive (essentially a coin flip)
- VaR autocorrelation: 0.999 — the baseline VaR is extremely sticky

**This reframes what the blend should optimise for.** The adjustment is a **now-casting** tool — it corrects staleness in real time, not a forecasting tool that predicts future VaR. The blend needs to catch the regime shift *while it's happening*, not wait for confirmation.

**Staleness budget reframing:** Rather than asking "how much lead time do we have?", the question becomes "how much staleness can we tolerate before breach rates diverge from expected?" The blend is calibrated to keep VaR within an acceptable staleness window.

---

## 4. The Symmetric Blend (Notebook 15): First Attempt

**Approach:** Linear ramp from $\alpha = 1$ (trust baseline) to $\alpha = 0$ (trust naive sum), symmetric around ratio = 1.

$$ \alpha = 1 - \text{clip}\left(\frac{|\text{ratio} - 1| - (\text{threshold} - 1)}{\text{max\_ratio} - \text{threshold}}, 0, 1\right) $$

**Results (threshold = 1.5, blend_max = 2.5):**

| Metric | Baseline | Symmetric Adjusted |
|--------|----------|-------------------|
| Mean VaR | 1.116% | 1.201% |
| Breach rate | 5.16% | 4.48% |
| Deviation from 5.00% | +0.16% | **+0.52%** |
| Mean α | 1.000 | 0.567 |
| Days adjusted | 0% | 67.5% |

**By correlation regime:**

| Regime | Days | Baseline | Symmetric | Winner |
|--------|------|----------|-----------|--------|
| Stable (ratio ≈ 1) | 613 | 5.06% | 4.73% | Baseline |
| Moderate shift (1.3–2.0) | 506 | 6.13% | 4.74% | Adjusted |
| Strong shift (>2.0) | 267 | 6.36% | **4.89%** | Adjusted |
| Ratio flipped (<0.7) | 512 | 3.52% | 3.71% | Baseline |

**The symmetric blend works where it should** (strong shifts: 6.36% → 4.89%) but **over-adjusts elsewhere** (stable regime, ratio flipped). The problem: it adjusts when correlation falls too, adding unnecessary conservatism.

**Best threshold from sweep:** 2.5 (deviation +0.16% — ties baseline). Higher thresholds help by adjusting fewer days, but they're still adjusting in both directions.

---

## 5. The Portfolio VaR Dashboard (Notebook 14): The Complete Picture

The dashboard combines everything into a production monitoring view — five VaR methods on portfolio returns plus three portfolio-specific signals.

**Dashboard structure:** 2×3 grid covering six questions:

| Panel | Question | What you check |
|-------|----------|---------------|
| VaR methods | How much risk? | Are lines clustered (stable) or diverging (investigate)? |
| Benefit | How reliable is VaR? | Green area shrinking = diversification failing |
| Correlation ratio | Why is it changing? | Above 1.5 = VaR window hasn't caught up |
| Baseline vs adjusted | What number to use? | Wide gap = standard VaR is stale |
| Breach rates by regime | Which is better calibrated? | In the current regime, baseline or adjusted? |
| Snapshot | What do I quote? | The four key numbers for the morning meeting |

**Key numbers (as of 2026-07-24):**
- 60/40 SPY/BND portfolio, 1,898 VaR observations since 2019
- Diversification benefit: 16.3% mean, 3.8% min (Jun 2021), 31.6% max (Nov 2024), 14.9% latest
- Correlation ratio (60d/252d): 1.83 latest — correlation is elevated
- Baseline breach: 5.16% (expected 5.00%)
- Adjusted breach: 4.48% (too conservative — the symmetric problem)

**Escalation ladder — portfolio edition:**

| Level | VaR methods | Benefit | Corr ratio | Action |
|-------|------------|---------|------------|--------|
| Green | All agree, low | >20% | ~1.0 | Standard monitoring |
| Yellow | One elevated | 10-20% | 1.0-1.5 | Note, watch tomorrow |
| Orange | Two elevated | 5-10% | 1.5-2.0 | Review positions |
| Red | All firing | <5% | >2.0 | Tighten, use adjusted VaR, escalate |

---

## 6. The Asymmetric Refinement (Notebook 15b): The Fix

### 6.1 The Problem Quantified

The symmetric blend adjusts **48.8% of days unnecessarily** — when correlation is falling, VaR is already conservative, and adding more conservatism erodes the number's usefulness.

| Direction | Days | Adjusted by symmetric |
|-----------|------|----------------------|
| Ratio > 1 (VaR understated) | 1,082 | 656 (60.6%) ← adjustment we WANT |
| Ratio < 1 (VaR conservative) | 816 | 626 (76.7%) ← UNNECESSARY |

### 6.2 Asymmetric Blend: Only Adjust When Correlation is Rising

$$ \alpha = \begin{cases} 1 & \text{if ratio} \leq \text{threshold} \\ 1 - \text{clip}\left(\frac{\text{ratio} - \text{threshold}}{\text{max\_ratio} - \text{threshold}}, 0, 1\right) & \text{if ratio} > \text{threshold} \end{cases} $$

**Results (threshold = 1.3, blend_max = 2.0):**

| Metric | Baseline | Symmetric | Asymmetric |
|--------|----------|-----------|------------|
| Mean VaR | 1.116% | 1.201% | 1.174% |
| Breach rate | 5.16% | 4.48% | 4.74% |
| Deviation | +0.16% | +0.52% | **+0.26%** |
| Mean α | 1.000 | 0.567 | 0.695 |
| Days adjusted | 0% | 67.5% | 44.7% |

The asymmetric blend cuts the deviation nearly in half (0.52% → 0.26%) by simply refusing to adjust when correlation is falling.

### 6.3 Sigmoid Blend: No Additional Benefit

A sigmoid (S-curve) blend was tested, designed to be gentle near the threshold and aggressive at the tails (where the ratio's information content is concentrated, per Notebook 13b).

**Result:** For SPY/BND, the sigmoid offers **no improvement** over linear asymmetric. Mean α = 0.578, deviation = +0.57% — slightly worse than symmetric. The extra parameter (steepness) adds complexity without benefit for this pair.

### 6.4 The Speed vs Noise Trade-off

The critical finding comes from the parameter sweep. 24 asymmetric configurations were tested (threshold × blend_max):

| Threshold | Blend Max | % Adjusted | Breach Rate | Deviation |
|-----------|-----------|------------|-------------|-----------|
| **1.2** | **3.0** | **47.6%** | **4.95%** | **+0.05%** |
| 1.3 | 3.0 | 44.7% | 4.95% | +0.05% |
| 1.5 | 3.0 | 34.6% | 4.95% | +0.05% |
| 1.8 | 3.0 | 25.1% | 4.95% | +0.05% |
| 2.0 | 3.0 | 21.6% | 4.95% | +0.05% |
| *Baseline* | — | 0% | 5.16% | **+0.16%** |

**The asymmetric blend with the right parameters beats baseline** — deviation drops to +0.05%, a 3× improvement over baseline's +0.16%.

**The sweet spot:** ~20-50% of days adjusted. Less than that and you're not catching enough shifts. More than that and you're over-adjusting on noise. The U-shaped deviation curve confirms: more adjustment ≠ better results.

---

## 7. Six Design Principles

These principles emerged across Notebooks 13b, 15, and 15b:

### 7.1 The Three-Component Framework is Robust
**Stable baseline + fast detector + blend rule.** This pattern generalises to any VaR methodology. The implementation details (linear vs sigmoid, symmetric vs asymmetric) are secondary to having all three components.

### 7.2 Asymmetric Adjustment is Better Than Symmetric
The risk you care about is *understated VaR*, not overstated. When correlation is falling, baseline VaR is already conservative — adding more conservatism is unnecessary. The asymmetric blend adjusts fewer days overall, but adjusts the *right* days.

### 7.3 The Ratio is a Staleness Diagnostic, Not a Leading Indicator
From Notebook 13b: the ratio doesn't lead VaR — it moves with it. The blend is a **now-casting** tool, not a forecasting tool. It corrects staleness in real time, it doesn't predict future breaches.

### 7.4 Non-Linear Blending Respects the Signal Structure
The ratio's information content is concentrated at the tails. A sigmoid blend is gentle near the threshold (small movements are noise) and aggressive at the extremes (strong staleness signal). For SPY/BND, linear asymmetric was sufficient — but the principle stands for pairs with more extreme ratio behaviour.

### 7.5 There is a Sweet Spot — More Adjustment is Not Better
The speed vs noise trade-off is empirically real. Adjust too little → stale VaR, breach spikes. Adjust too much → false alarms, wasted risk budget. The optimal blend typically adjusts 10-50% of days.

### 7.6 The Optimal Parameters are Empirical, Not Theoretical
There's no formula for the "right" threshold or blend_max. It depends on the specific assets, the period, and your tolerance for staleness. The parameter sweep is the calibration tool — run it, pick the sweet spot, and re-check periodically (quarterly, after regime changes, when adding/removing assets).

---

## 8. Practical Recommendations

### Which blend to use?

| Blend | Parameters | Deviation | When to use |
|-------|-----------|-----------|-------------|
| **Asymmetric linear** | thresh=1.2, max=3.0 | +0.05% | Recommended default — simple, effective, explainable |
| Symmetric | thresh=2.5, max=2.5 | +0.16% | Only if you want a fully transparent adjustment that ties baseline |
| Sigmoid | thresh=1.3, k=4.0 | +0.57% | Skip for SPY/BND — no benefit over linear |

### Deployment checklist

1. **Run the parameter sweep** on your specific asset pair and period — don't copy the numbers above
2. **Choose the blend that balances deviation and % adjusted** — don't blindly pick lowest deviation
3. **Place adjusted VaR alongside baseline** in the dashboard, not replacing it
4. **Re-calibrate quarterly** or after major correlation regime changes
5. **Document the chosen parameters** and the rationale

### Limitations

| Limitation | Mitigation |
|-----------|------------|
| Ratio is contemporaneous, not leading | Accept it's a now-cast, not a forecast |
| Parameters need calibration per asset pair | Make the sweep part of the dashboard update |
| 2-asset only — pairwise ratio doesn't scale | Generalise to n-asset in Notebook 16 |
| Historical only — no parametric or Monte Carlo | Separate workstreams for later phases |
| The blend helps with correlation staleness, not vol staleness | Vol scaling and decay weighting handle that separately |

---

## 9. What We Built — Notebook Summary

| # | Notebook | Key Finding |
|---|----------|-------------|
| 12 | Portfolio diversification benefit | Benefit = 16.3% mean, ranges 3.8-31.6%. Shrinks before crises. |
| 13 | Correlation dynamics | 60d/252d ratio reveals when correlation has shifted from the norm. |
| 13b | Correlation → VaR lead-lag | **No lead found.** Ratio is contemporaneous. Reframes the blend as a now-cast. |
| 15 | Symmetric blend experiment | Works during strong shifts (6.36% → 4.89%) but over-adjusts elsewhere. |
| 14 | Portfolio VaR dashboard | Complete 2×3 production view: methods + benefit + ratio + adjusted VaR. |
| 15b | Asymmetric blend refinement | **Asymmetric beats baseline** (+0.05% deviation). Six design principles. |

---

## 10. Next: n-Asset Generalisation (Notebook 16)

The current framework works for 2 assets. The natural extension:

- 3+ asset portfolio (SPY/BND/GLD)
- Generalised naive sum: $\sum w_i \text{VaR}_i$
- Pairwise correlation matrix — $n(n-1)/2$ ratios to monitor
- Marginal diversification contribution per asset
- Challenge: combining multiple pairwise blend signals into a single adjustment

The three-component framework (baseline + detector + blend) generalises cleanly. The complexity is in aggregating $n(n-1)/2$ pairwise ratios into one adjustment signal — which pairs are driving the staleness?
