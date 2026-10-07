# Monte Carlo VaR: Where Does Your Understanding Break?

**Date:** 2026-07-10
**Topic:** First pass at Monte Carlo VaR — what you already know, what's hazy, and where we start

---

## What You Already Know

From your parametric and historical VaR sessions, you understand:

| Method | How It Gets the Distribution | Core Mechanics |
|---|---|---|
| **Historical** | Uses actual past returns (252 data points) | Sort → find percentile |
| **Parametric** | Imposes a distribution (normal) defined by μ̂, σ̂ | Formula: μ − z_α · σ |
| **Monte Carlo** | Simulates thousands of possible futures | ??? |

You also know the four-component framework:
1. **The Loss** — what is being measured
2. **Time Horizon** — the rehedging period
3. **Underlying Data** — what sample, how big
4. **Model Assumption** — stationarity (the past distribution ≈ future distribution)

And you understand the key trade-off: **parametric efficiency (2 numbers) vs historical honesty (252 points).**

---

## Monte Carlo in One Sentence

**Monte Carlo VaR simulates thousands of possible future return paths from a model you specify, then sorts the simulated outcomes and reads the percentile — exactly like historical VaR, but with fake returns instead of real ones.**

That's the core. The "sort and read" step is identical to historical VaR. The new piece is: *where do the returns come from?*

---

## Concrete Example — Before We Define Anything

Let me give you a toy example. This is the entire method in miniature.

**Setup:** You have a position in SPY. You've estimated that daily returns are approximately normal with μ̂ = 0.05% and σ̂ = 1.2%.

**Step 1 — Simulate:** Instead of looking at 252 past returns, you *generate* 10,000 random returns from a normal distribution with μ̂ = 0.05% and σ̂ = 1.2%:

```
Simulated return 1:    +0.83%
Simulated return 2:    -1.42%
Simulated return 3:    +2.11%
...
Simulated return 9999: -0.67%
Simulated return 10000: +0.14%
```

**Step 2 — Sort:** Sort these 10,000 simulated returns from worst to best.

**Step 3 — Read:** Find the 5th percentile. That's your 95% 1-day VaR.

---

## Pause — Here's the Question

If you already have μ̂ and σ̂, and you're simulating 10,000 draws from a normal distribution, then the 5th percentile of those simulated returns will converge to... exactly μ̂ − 1.6449 · σ̂. The parametric VaR formula.

**So what's the point?** If you're simulating from a normal distribution, Monte Carlo gives you the same answer as parametric VaR, just with more computational effort. The method only earns its keep when you do something the parametric formula *can't* do.

**Before we go further — what do you think Monte Carlo is *for*?** Given that you already have parametric and historical VaR, what gap does simulation fill? What can you do with simulated returns that you can't do with a formula or with sorted past returns?