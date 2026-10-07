# Why Breach Distribution Matters More Than Average Breach Rate

**Date:** 2026-07-21
**Topic:** Calibration vs conditional calibration — why a 5% average doesn't mean the model works
**Turn:** 009

## The trap of the average

After running our backtests, here are the headline numbers:

| Method | Total breach rate | Verdict from average alone |
|--------|-----------------|---------------------------|
| Equal-weighted | 4.76% | "Near-perfect calibration" |
| Decay λ=0.94 | 5.97% | "Overstating risk" |
| Vol-scaled | 6.19% | "Worse" |
| Combined | 6.88% | "Worst" |

If you stopped here, you'd conclude equal-weighted is the best model. It's closest to the expected 5.00%. Case closed.

The case is not closed. Here's why.

## The same average, different distributions

Consider two hypothetical VaR models, both producing exactly 5% breaches over 1,000 days:

| Model | Breaches in calm years | Breaches in crisis year | Average |
|-------|----------------------|------------------------|---------|
| Model A | 1% per year (10 breaches over 4 calm years) | 16% (40 breaches in one crisis year) | 5% |
| Model B | 4.8% per year (12 breaches/year) | 5.2% (13 breaches) | 5% |

Both have the same 5% average. Both are "well-calibrated" by the headline metric. Are they equally good?

Model A is **conditionally miscalibrated**. It understates risk during calm periods (1% breaches when you expect 5% — a model that's too conservative) and catastrophically understates risk during crises (16% breaches — the model is dangerously wrong when it matters most).

Model B is **conditionally calibrated**. The breach rate is close to 5% in every regime. The model means the same thing regardless of market conditions.

## What our actual models show

Here are the real numbers from notebook 06:

| Regime | Equal | Decay λ=0.94 | Target |
|--------|-------|-------------|--------|
| Pre-COVID calm | **2.48%** | 5.32% | 5.00% |
| COVID crash | **17.20%** | 7.53% | 5.00% |
| Post-COVID | 4.41% | 5.99% | 5.00% |
| **Max deviation** | **12.20%** | 2.53% | — |

Equal-weighted looks great on average (4.76%) but is a disaster within regimes. The model says "95% VaR" but that number means something completely different depending on when you measure it:
- During calm: breaches happen 2.5% of the time. The model is too conservative — you're holding more capital than needed.
- During crises: breaches happen 17% of the time. The model is dangerously wrong — you don't have enough capital.

Decay-weighted looks worse on average (5.97%) but is far more consistent. The 95% VaR number means roughly the same thing in calm and crisis — about 5-7% of days breach, regardless of regime.

## Why conditional calibration matters

### In practice

You don't live through the "average" of all regimes. You live through one regime at a time. A model that's 2.5% in calm and 17% in crisis is a model that's consistently wrong — it's just wrong in opposite directions at different times.

The trader relying on equal-weighted VaR in February 2020 is being told their risk is manageable. By March, they're experiencing 3× more breaches than expected. The model didn't fail in March — it was already failing in February by being too optimistic. The 4.76% average is an average of two wrong answers, not one right answer.

### In statistical terms

Unconditional calibration (average breach rate = expected) is a necessary condition for a good model, but it's not sufficient. The model must also be **conditionally calibrated** — the breach rate should be close to expected in every identifiable subset of the data.

A model that breaches 0% on Mondays and 10% on Tuesdays has a 5% average but is useless. A model that breaches 2.5% in calm and 17.5% in crises is the same problem at a different frequency.

### In decision-making

If you're a risk manager setting position limits, the conditional behaviour matters more than the average:

- **Equal-weighted:** "Your VaR limit is £X. Most of the time you won't breach it. But when markets get volatile, expect to breach it 3× more often than the model suggests."
- **Decay-weighted:** "Your VaR limit is £X. You'll breach it slightly more often than expected during calm periods, but roughly as expected during volatile periods."

The second statement is more useful. It tells you what the number actually means.

## The right metrics for model comparison

Given all this, the right way to compare VaR models is:

| Metric | What it captures | Equal | Decay | Vol-Sc |
|--------|-----------------|-------|-------|--------|
| Unconditional breach rate | Average calibration | **4.76%** | 5.97% | 6.19% |
| Max regime deviation | Worst-case miscalibration | 12.20% | **2.53%** | **2.53%** |
| COVID reaction time | Speed of adaptation | 29 days | **6 days** | 9 days |
| Pre-COVID breach rate | Calm-period honesty | 2.48% | **5.32%** | 7.25% |

Equal wins on one metric (unconditional rate). Decay wins on two (consistency, speed). Vol-scaled ties on consistency but is slower.

The unconditional breach rate is the weakest of these metrics — it's the one that can look good while the model is failing conditionally. The regime-conditional rates tell you what the model actually does when it matters.

## The deeper principle

This pattern — "good on average, terrible within subgroups" — is not unique to VaR. It's Simpson's paradox in risk management: aggregate statistics can hide the fact that the model is wrong in every individual regime, just in opposite directions.

The honest way to evaluate any forecasting model:

1. **Don't just look at the average error.** Decompose it by identifiable subgroups.
2. **The subgroups that matter are the ones where being wrong is costly.** In VaR, that's crises.
3. **A model that's consistently slightly wrong is better than one that's perfectly right on average but catastrophically wrong in the tails.** Because you can adjust for consistent bias; you can't adjust for a model that fails exactly when you need it.

The meta-point for our project: this is why we built the breach investigation notebooks (04, 06). The headline breach rate on notebook 02 was interesting but incomplete. The regime breakdowns are where the real insights live.