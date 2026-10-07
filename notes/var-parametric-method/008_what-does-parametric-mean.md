# What Does "Parametric" Actually Mean?

**Date:** 2026-07-07
**Topic:** The meaning of "parametric" in parametric VaR and in statistics generally

---

## The One-Sentence Definition

**Parametric** means the model is fully specified by a fixed, finite set of numbers — the parameters. Once you know those numbers, you know everything the model will ever say. You can throw the original data away.

---

## Parametric vs Non-Parametric — The Core Distinction

| | Parametric | Non-Parametric |
|---|---|---|
| **Model defined by** | A fixed set of parameters | The data itself |
| **Number of "things" to store** | Constant (e.g., 2: μ, σ) | Grows with data (e.g., 252 points) |
| **Data after fitting** | Can be discarded | Must be retained |
| **Extrapolation** | Smooth, continuous, any quantile | Only at observed data points |
| **Assumptions** | Strong (the distribution family) | Weak (only that future ≈ past) |
| **Example** | Normal distribution N(μ, σ²) | Empirical distribution (sorted returns) |

The word comes from the Greek *para-* (beside, auxiliary) + *metron* (measure). Parameters are the auxiliary measurements that define the model.

---

## In the Context of VaR

### Historical VaR = Non-Parametric

The model IS the data. No compression. No distribution family assumed.

```
Data: r₁, r₂, ..., r₂₅₂
Model: the empirical CDF built from those 252 points
Storage: 252 numbers
VaR: sort → position 13 → done
```

There are no "parameters" to estimate (beyond "which percentile" which is a choice, not a parameter estimated from data). The model has as many "moving parts" as data points.

### Parametric VaR = Parametric

The model is $N(\mu, \sigma^2)$. Once you estimate $\mu$ and $\sigma$, you're done.

```
Data: r₁, r₂, ..., r₂₅₂
Step 1: Estimate parameters → μ̂ = mean(r), σ̂ = std(r)
Step 2: Discard data (optional — you don't need it anymore)
Model: N(μ̂, σ̂²)
Storage: 2 numbers
VaR: μ̂ - z·σ̂ → done
```

Two parameters replace 252 data points. That's the compression you identified.

---

## Why "Parametric" and Not "Normal" or "Gaussian"?

Because the method isn't tied to the normal distribution. You could use:

| Distribution | Parameters | When You'd Use It |
|---|---|---|
| Normal | μ, σ (2) | Standard assumption |
| Student's t | μ, σ, ν (3) | When you want fatter tails (ν controls tail thickness) |
| Skewed normal | μ, σ, α (3) | When returns are asymmetric |
| Log-normal | μ, σ (2) | When returns are multiplicative |

All of these are parametric methods. They all work the same way: estimate parameters from data → use the distribution's CDF to find the quantile. The normal is just the most common choice.

The method is called "parametric VaR" because the defining feature is the use of a parametric distribution — not specifically the normal distribution. Though in practice "parametric VaR" almost always means "normal parametric VaR" unless specified otherwise.

---

## The Deeper Statistical Meaning

In statistics, the parametric/non-parametric distinction is about how the model complexity scales:

```
Parametric:
  Model complexity = O(1)  — fixed number of parameters
  Information per parameter → ∞ as data grows
  Risk: model is wrong (bias)

Non-parametric:
  Model complexity = O(n)  — grows with data
  Information per parameter → 0 as data grows  
  Risk: model is noisy (variance)
```

This is the bias-variance tradeoff in model selection. Parametric models have high bias (they force a specific shape) but low variance (few parameters to estimate, so estimates are stable). Non-parametric models have low bias (they follow the data) but high variance (estimates are sensitive to which data points you have).

---

## What It's NOT

"Parametric" does NOT mean:
- "Uses parameters" (every model does — even historical VaR has the percentile as a parameter)
- "More mathematical" (non-parametric methods can be deeply mathematical)
- "Assumes normality" (a subset of parametric methods do; the word itself is broader)

It specifically means: **the model is a member of a parametric family** — a distribution whose shape is completely determined by a small, fixed set of numbers.

---

## Connecting to Your Template Metaphor

Your "template" metaphor is exactly what "parametric" means:

```
Parametric family = template with empty slots
  N(μ, σ²): slots are μ and σ
  
Your data fills the slots:
  μ̂ = 0.04%, σ̂ = 1.2%
  
The filled template IS your model:
  N(0.04%, 1.2%²)
```

The number of slots is fixed regardless of how much data you have. That's the parametric property.

---

## One Question

If you wanted fatter tails than the normal distribution provides, which parametric distribution might you choose instead, and what extra parameter would it add?
