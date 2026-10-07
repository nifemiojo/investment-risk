# Session Summary: Parametric VaR Mastered

**Date:** 2026-07-07
**Topic:** Complete summary of the parametric VaR teaching session — what we covered, key insights, and readiness for Monte Carlo

---

## Session Arc

```
001: Find the hazy concept → Z-score, normality jump, formula
002: Z-score = distance, not probability — formula derivation
003: Develop your ideas — compression, templates, models
004: Z-score solidified — quiz passed
005: Three spaces, two translations — structured mental model
006: Quantiles & percentiles refresher
007: CDF — no closed form, numerical computation
008: What "parametric" actually means
009: Sample vs population, distribution flexibility, bias-variance tradeoff
010: 7 limitations + practical mitigations
011: 7 failure modes — what it looks like when it breaks
012: How practitioners actually use it — despite everything
```

---

## What You Now Understand

### The Definition
Parametric VaR = $\mu - z_{\alpha} \cdot \sigma$ is derived by standardizing a normal random variable and using the inverse CDF to find the $\alpha$-quantile.

### The Z-Score
- Distance from mean in standard deviation units — **not a probability**
- Standard normal N(0,1) is the universal translator: its x-axis IS the z-axis
- $z_{0.05} = 1.6449$ means "1.6449 standard deviations below the mean"

### The Architecture
```
Real World (r) → standardize → Standard Normal (z) → inverse CDF → Probability (p)
                     ←── un-standardize ──              ←── CDF ──
```
Three spaces, two translations. Every parametric VaR calculation is a round-trip through this system.

### What "Parametric" Means
- Model defined by a fixed, finite set of parameters
- Historical VaR is non-parametric (252 data points ARE the model)
- Parametric VaR is parametric (2 numbers replace 252 data points)
- The framework is flexible — you can swap distributions (Student's t, skewed t, GED)
- More parameters = more flexibility but more estimation error

### The CDF Reality
- $\Phi(z) = \int_{-\infty}^{z} \frac{1}{\sqrt{2\pi}} e^{-t^2/2} dt$ has no closed form
- Computed numerically via rational approximations — accurate to ~15 decimal places
- `norm.ppf()` and `norm.cdf()` in scipy handle this invisibly

### Limitations & Mitigations
| Limitation | Fix |
|---|---|
| Normality wrong | Student's t, Cornish-Fisher |
| Mean noisy | Set μ=0 for short horizons |
| Vol time-varying | EWMA, GARCH |
| √t scaling wrong | Overlapping returns |
| Window arbitrary | EWMA decay |
| Correlations needed | Factor models, shrinkage |
| Single number | Add ES, backtesting |

### Failure Modes
1. Calm-before-storm (VaR shrinks, risk explodes)
2. Correlation collapse (diversification disappears)
3. Window cliff (artifacts from rolling window edges)
4. Silent drift (no backtesting, model wrong for months)
5. Mean misdirection (noisy μ̂ adds error)
6. Procyclical amplification (VaR-based limits drive the cycle)
7. Precision illusion (6 decimal places on a ±30% estimate)

### How Practitioners Use It
- Common language, not a forecast
- Speedometer, not GPS
- Conversation starter, not ender
- Fence with a gate, not a wall
- Always layered: VaR → variants → ES → stress tests → backtesting → human judgment

---

## Key Mental Models Built

1. **Template metaphor:** N(0,1) is the immutable master template; N(μ,σ) is the data-specific instance
2. **Compression vs fidelity:** Parametric efficiency (2 numbers) trades off against historical honesty (252 points)
3. **Three-space architecture:** Real world ↔ Standard Normal ↔ Probability space
4. **Defense-in-depth:** No single risk number is trusted alone

---

## Connection to Monte Carlo

Monte Carlo VaR is the third method — and it bridges the gap between parametric and historical:

| Method | How It Gets the Distribution |
|---|---|
| Historical | Uses actual past returns |
| Parametric | Imposes a parametric distribution (normal) |
| **Monte Carlo** | **Simulates thousands of possible futures from a model** |

You now understand:
- ✅ Why methods differ (distribution assumptions)
- ✅ What the normal distribution imposes (symmetry, thin tails, specific kurtosis)
- ✅ How quantiles are extracted from distributions
- ✅ The tradeoff between model simplicity and model accuracy

Monte Carlo will let you relax the normality assumption while keeping the parametric framework — you can simulate from a Student's t, a GARCH process, or any distribution you specify. The core mechanics (generate returns → sort → find quantile) are the same. The new piece is the simulation engine.

---

## Files Created (12)

All in `sessions/var-parametric-method/`:

| File | Topic |
|---|---|
| 001 | Finding the hazy concept |
| 002 | Z-score = distance, not probability |
| 003 | Evaluating your ideas |
| 004 | Z-score solidified |
| 005 | Three spaces, two translations |
| 006 | Quantiles & percentiles refresher |
| 007 | CDF — no closed form |
| 008 | What "parametric" means |
| 009 | Flexibility & tradeoffs |
| 010 | Limitations & mitigations |
| 011 | Failure modes in practice |
| 012 | Practical decision-making |
