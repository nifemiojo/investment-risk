# Your Understanding — Evaluated, Refined, and Extended

**Date:** 2026-07-07
**Topic:** Evaluating your definition of parametric, the flexibility to swap distributions, and the sample-vs-population distinction

---

## Your Definition — Let Me Check It

You said:

> "Parametric means we're using a model distribution over our data and we compress our sample data into estimates of the population and feed them into the distribution template model and it's this distribution template model that specifies the number of parameters which are used to draw the distribution which assumes other characteristics of the distribution that are then imposed on top of your data which is then discarded and the distribution is used for probability inference."

**Verdict: Essentially correct.** Let me refine two subtle points.

---

## Refinement 1: Sample Statistics vs Population Parameters

You said "we compress our sample data into estimates of the population." This is exactly right, and it's worth making the notation explicit:

| | Sample (what we compute) | Population (what we assume exists) |
|---|---|---|
| Mean | $\hat{\mu} = \frac{1}{n}\sum r_i$ | $\mu$ (true, unknown) |
| Std Dev | $\hat{\sigma} = \sqrt{\frac{1}{n-1}\sum(r_i - \hat{\mu})^2}$ | $\sigma$ (true, unknown) |

The hat ($\hat{}$) means "estimate." We never know the true $\mu$ and $\sigma$ — we estimate them from a finite sample and hope they're close.

This matters because:

$$\text{VaR}_{\text{true}} = \mu - z \cdot \sigma \quad \text{(uses unknown population parameters)}$$

$$\text{VaR}_{\text{estimated}} = \hat{\mu} - z \cdot \hat{\sigma} \quad \text{(uses sample estimates)}$$

The VaR you compute is itself an estimate. There's **estimation error** in $\hat{\mu}$ and $\hat{\sigma}$ that propagates into your VaR. With 252 data points, this error is usually small — but it's real.

This is another layer of uncertainty that the parametric method doesn't advertise: not only might the model be wrong (normality assumption), but even if it's right, your parameter estimates are noisy.

---

## Refinement 2: "Imposed on Top of Your Data"

You said the distribution's characteristics are "imposed on top of your data." More precisely: they **replace** your data's characteristics.

```
Your data might have:              Normal N(μ̂, σ̂²) forces:
  skewness = -0.3        →        skewness = 0
  kurtosis = 4.2         →        kurtosis = 3
  left tail: power law   →        left tail: exponential decay
```

The template doesn't sit "on top" — it **overwrites**. Every feature of your data that isn't captured by $\hat{\mu}$ and $\hat{\sigma}$ is erased and replaced by the normal distribution's opinion about what that feature should be.

This is why it's called "parametric" and not "descriptive." You're not describing your data. You're fitting a model to it and then using the model instead of the data.

---

## Your Insight on Flexibility — This Is the Important One

> "If you think normal distribution makes too many harmful assumptions you can switch out the model/distribution for a new one?"

**Yes. And this is the whole game.**

The parametric approach is a framework, not a specific distribution:

```
PARAMETRIC VAR FRAMEWORK
========================

Step 1: Choose a parametric family      ← YOU DECIDE
Step 2: Estimate parameters from data   ← mechanical
Step 3: Use the family's CDF⁻¹          ← built into the family
Step 4: Compute VaR                     ← mechanical
```

Step 1 is where all the judgment lives. The rest is mechanical.

---

## A Tour of Parametric Families for VaR

| Family | Parameters | What It Does Differently | When to Use |
|---|---|---|---|
| **Normal** | μ, σ (2) | Baseline. Symmetric, thin tails. | Quick estimates, short horizons, diversified portfolios |
| **Student's t** | μ, σ, ν (3) | Fatter tails. ν → ∞ recovers normal. ν ≈ 3–5 for financial returns. | When you believe tail events are more common than normal predicts |
| **Skewed t** | μ, σ, ν, α (4) | Fatter tails + asymmetry. α controls skew direction. | When returns have both fat tails and crash asymmetry |
| **Generalized Error (GED)** | μ, σ, β (3) | β controls tail thickness (β < 2 = fatter than normal, β = 2 = normal, β > 2 = thinner) | When you want flexible tail control without asymmetry |
| **Cornish-Fisher** | μ, σ, S, K (4) | Adjusts normal quantiles using sample skewness (S) and kurtosis (K). Not a true distribution but a correction. | When you want to keep the normal framework but adjust for non-normality |

---

## The Tradeoff: More Parameters ≠ Better

You might think: "If normal is too restrictive, why not always use the most flexible distribution?"

Because every extra parameter must be **estimated from the same data**. With 252 points:

| Parameters | Information per Parameter | Estimation Risk |
|---|---|---|
| 2 (normal) | 126 points/param | Low |
| 3 (t) | 84 points/param | Moderate |
| 4 (skewed t) | 63 points/param | Higher |

More parameters = more flexibility = more estimation error. This is the **bias-variance tradeoff** again:

```
Normal:    high bias (wrong shape),     low variance (stable estimates)
Skewed t:  low bias (flexible shape),   high variance (unstable estimates)
```

A skewed t with ν = 3.1 estimated from 252 noisy daily returns might give you a VaR that's very sensitive to which 252 days you picked. The normal's VaR is more stable — wrong, but stable.

---

## Why Normal Remains the Default (for Better or Worse)

Despite its flaws, normal parametric VaR dominates practice because:

1. **Tractability.** Two parameters. No convergence issues. Everyone understands it.
2. **CLT cover.** For diversified portfolios over short horizons, the central limit theorem suggests returns are *approximately* normal — even if individual assets aren't.
3. **Convention.** Regulators, risk systems, and counterparties all speak "normal parametric VaR." Deviating means explaining yourself.
4. **It's often good enough.** For a 95% 1-day VaR on a diversified portfolio in normal times, the error from assuming normality is often smaller than the error from other sources (bad data, regime change, liquidity).

The real danger isn't using normal parametric VaR — it's using it **without knowing what you're assuming**. Which, by this point in the session, is no longer you.

---

## The Meta-Point

You've now understood parametric VaR at three levels:

| Level | Understanding |
|---|---|
| **Mechanical** | VaR = μ̂ − z·σ̂. Plug in numbers, get answer. |
| **Structural** | Three spaces, two translations. Standard normal as universal translator. |
| **Philosophical** | Parametric = choose a family, estimate parameters, discard data. The model replaces the data. Every family has opinions. You choose which opinions to accept. |

Level 3 is where dangerous-good lives. Most people stop at Level 1.

---

## Check-In

You said the parametric method allows you to swap distributions. If you swapped to a Student's t with ν = 4 on your 60/40 portfolio (μ̂ = 0.0447%, σ̂ = 0.8162%), would the 95% VaR be larger or smaller in magnitude than the normal parametric VaR of -1.297%? And why?
