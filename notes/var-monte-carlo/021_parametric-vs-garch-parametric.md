# Parametric VaR vs GARCH Parametric VaR: The Difference

**Date:** 2026-07-10
**Topic:** Both are parametric formulas, but the volatility estimate is different — and that's the whole game

---

## The Two Formulas

### Standard Parametric VaR

$$\text{VaR}_{0.05} = \mu - z_{0.05} \cdot \hat{\sigma}$$

- $\hat{\sigma}$: sample standard deviation from the full estimation window (e.g., 252 days)
- Same number every day until you re-estimate

### GARCH Parametric VaR

$$\text{VaR}_{0.05} = \mu - z_{0.05} \cdot \hat{\sigma}_t$$

- $\hat{\sigma}_t$: today's conditional volatility from the GARCH equation
- Different number every day, depending on what happened yesterday

---

## Why They're Different

Standard parametric VaR answers: "What's the risk on an average day?"

GARCH parametric VaR answers: "What's the risk today, given what just happened?"

Same formula structure. Same $z_{0.05} = -1.6449$. The only difference is which σ̂ you plug in.

---

## Concrete Example Over 5 Days

Imagine a market that crashes, then recovers. Full-sample σ̂ = 1.30%.

| Day | Yesterday's Return | GARCH $\hat{\sigma}_t$ | Standard Parametric VaR | GARCH Parametric VaR |
|---|---|---|---|---|
| Mon | +0.2% (calm) | 1.10% | £21,400 | £18,100 |
| Tue | −3.5% (crash!) | 1.55% | £21,400 | **£25,500** |
| Wed | −1.2% (still volatile) | 1.48% | £21,400 | **£24,300** |
| Thu | +0.8% (calming) | 1.35% | £21,400 | £22,200 |
| Fri | +0.1% (calm) | 1.20% | £21,400 | £19,700 |

Standard parametric VaR: £21,400 every day. Like a speedometer stuck at 30 mph regardless of whether you're on a highway or an icy road.

GARCH parametric VaR: adjusts. £18,100 on calm Monday. £25,500 on Tuesday after the crash. £19,700 by Friday when things settle.

---

## What You're Actually Comparing

| | Standard Parametric | GARCH Parametric | Monte Carlo + GARCH |
|---|---|---|---|
| **σ̂ source** | Full sample standard deviation | GARCH equation (conditional on yesterday) | GARCH equation |
| **Formula** | μ − z_α · σ̂ | μ − z_α · σ̂_t | Sort simulated returns |
| **σ̂ changes daily?** | No | Yes | Yes |
| **Works for 1-day?** | Yes | Yes | Yes (but overkill) |
| **Works for 10-day?** | √10 scaling only | √10 scaling only | Yes (simulates actual paths) |

---

## The Two Innovations, Separated

GARCH innovates on **how you estimate volatility.** It replaces "one number from the full sample" with "a number that updates based on what just happened."

Monte Carlo innovates on **how you compute the quantile.** It replaces "plug into a formula" with "simulate from the model and sort."

These are independent. You can use GARCH without Monte Carlo (1-day VaR with the formula). You can use Monte Carlo without GARCH (simulate from a fixed distribution). Or you can combine them (10-day VaR with GARCH paths).

---

## Check-In

Does this land? The difference between standard parametric VaR and GARCH parametric VaR is purely in the σ̂ — fixed sample statistic vs time-varying conditional estimate. Same formula, different input, very different answer on volatile days.