# Volatility Clustering: Why the Sequence Destroys the Model

**Date:** 2026-07-10
**Topic:** Your oil shock example — how clustered volatility breaks parametric VaR in ways that are structurally invisible to the model

---

## Your Example, Made Concrete

You described an oil price shock (Iran war) that creates an *entire period* of elevated volatility. Let me put numbers on it.

**Scenario:** 252 trading days. The first 200 days are "normal" with σ = 1.5%. Days 201–252 are "crisis" with σ = 4.0%. The actual daily returns are drawn from these two regimes.

**What parametric VaR sees:**

You estimate σ̂ from the full 252-day window. The sample variance blends the two regimes:

$$\hat{\sigma}^2 = \frac{200 \cdot (1.5\%)^2 + 52 \cdot (4.0\%)^2}{252} = \frac{200 \cdot 2.25 + 52 \cdot 16.0}{252} = \frac{450 + 832}{252} = 5.09$$

$$\hat{\sigma} \approx 2.26\%$$

**Terms:**
- $\hat{\sigma}^2$: estimated variance from the full window
- 200: number of calm days
- 52: number of crisis days
- 1.5%: calm-period daily volatility
- 4.0%: crisis-period daily volatility

So the model says: "daily volatility is 2.26%." Let's see what happens.

---

## What Breaks

### During the Calm Period (Days 1–200)

The model's VaR at 95% (assuming μ̂ ≈ 0):

$$\text{VaR}_{0.05} = 0 - 1.6449 \cdot 2.26\% = -3.71\%$$

But the *true* volatility during calm days is 1.5%. The true VaR should be:

$$\text{VaR}_{0.05}^{\text{true}} = 0 - 1.6449 \cdot 1.5\% = -2.47\%$$

The model is **overestimating risk** — setting a −3.71% threshold when losses only exceed −2.47% on 5% of calm days. You'd get fewer exceptions than expected. The model is too conservative.

### During the Crisis Period (Days 201–252)

The true volatility is 4.0%. The true VaR should be:

$$\text{VaR}_{0.05}^{\text{true}} = 0 - 1.6449 \cdot 4.0\% = -6.58\%$$

But the model still says −3.71%. You'd expect losses to exceed −3.71% on roughly **20% of crisis days** (since 3.71% / 4.0% ≈ 0.93 standard deviations, which is the 18th percentile — about 82% of observations are above this threshold, so ~18% breach).

**Terms:**
- 3.71% / 4.0% ≈ 0.928: the model's VaR threshold expressed in crisis-period standard deviations
- 18th percentile: the probability of a return below −0.928σ in a normal distribution

Instead of the expected 5% exception rate, you get ~18% during the crisis. A backtest would flag this as a model failure.

---

## The Structural Problem

Parametric VaR with a fixed window commits you to a single σ̂ that averages across regimes. This averaging is invisible — the model doesn't know the data came from two different distributions. It just sees 252 numbers and compresses them.

The sequence you described — 200 calm days followed by 52 crisis days — is the worst case for this compression. The model is simultaneously too conservative (calm period) and too dangerous (crisis period).

---

## What Monte Carlo Would Let You Do

Instead of compressing 252 days into μ̂ and σ̂, you could specify a **regime-switching model**:

- **Regime 1 (calm):** σ = 1.5%, probability of staying in calm = 98% per day
- **Regime 2 (crisis):** σ = 4.0%, probability of staying in crisis = 95% per day

Then simulate 10,000 paths where each day the model randomly stays in the current regime or switches. The simulated returns reflect the fact that volatility isn't constant — it shifts between regimes.

The VaR you get depends on which regime you're *currently in* when you run the simulation. If you're in calm, the simulated paths mostly stay in calm (with occasional crisis bursts), and the VaR is lower. If you're in crisis, the simulated paths reflect elevated near-term volatility.

This is the power: **the VaR is conditional on the current state of the world, not an unconditional average.**

---

## But This Is Also Monte Carlo's First Failure Mode

You've touched on something important. Let me flag it now: **the model is only as good as the regimes you specify.**

In the example above, I said "two regimes, σ = 1.5% calm, σ = 4.0% crisis." But how do I know those numbers? I estimated them from the same data after the fact. I knew there was a crisis because I could see it in the rearview mirror.

The Monte Carlo gains over parametric come from *better specification of the data-generating process*. But that specification is itself an act of modeling — and it carries all the same estimation risk, plus new ones:

- How many regimes? (2? 3? Continuous?)
- What are the transition probabilities?
- When does a regime actually change? (You only know in hindsight)

This is a theme we'll return to: **Monte Carlo lets you model more complex processes, but the complexity creates new ways to be wrong.**

---

## Check-In

Your oil shock example is a clean illustration of why the sequence of returns matters. But you also have a closer-to-home example: **Spreadex's autohedging system.** 

If the system hedges more aggressively after a loss — tightening limits, increasing hedge ratios — then the risk profile of the room *depends on what happened yesterday*. That's a feedback loop. Parametric and historical VaR can't see it. Monte Carlo could simulate it.

Does that resonate? Does the autohedging behavior at Spreadex create path-dependency in the risk profile?