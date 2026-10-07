# Monte Carlo: What Simulation Actually Buys You

**Date:** 2026-07-10
**Topic:** The three gaps Monte Carlo fills — what you can simulate that formulas and history can't give you

---

## What You Got Right

You said two things worth developing:

> "the simulation gives you chance to dictate properties about the sample/observations, maybe like the relationship between observations"

> "the more you sample... you will converge to the properties of the distribution"

Both are correct. Let me sharpen each.

---

## Convergence Is the Mechanism, Not the Point

You're right about convergence. If you simulate returns from a normal distribution N(μ̂, σ̂²):

- With 100 draws: the 5th percentile might be −1.58%
- With 1,000 draws: −1.63%
- With 10,000 draws: −1.64%
- With 100,000 draws: −1.644% (approaching the true parametric value)

This is the Law of Large Numbers at work. The simulated quantile converges to the true quantile.

**But this is also why simulating from a normal distribution is pointless for VaR.** You already have the formula μ̂ − 1.6449 · σ̂. Simulation adds nothing except sampling noise.

So if convergence to the normal quantile isn't the point, what is?

---

## The Three Gaps Monte Carlo Fills

### Gap 1: Distributions With No Closed-Form Quantile

Parametric VaR works because the normal distribution has a simple quantile formula: μ − z_α · σ. But what if you think returns follow a **Student's t-distribution** with 4 degrees of freedom?

The Student's t quantile exists — you can look it up — but there's no simple formula. You need a table or a numerical inversion. And what about more exotic distributions? A mixture of two normals? A skewed-t? A distribution you estimated from a kernel density?

Monte Carlo doesn't care. You simulate from whatever distribution you specify, sort, and read. **Any distribution you can sample from, you can compute VaR for.**

### Gap 2: Dependence Between Observations — The One You Flagged

This is the most important gap, and you named it: *"relationship between observations."*

Both parametric VaR and historical VaR treat each day's return as an independent draw. Day 1's return doesn't affect day 2's return. The parametric formula folds all information into two numbers; historical VaR treats the sorted list as if order doesn't matter.

But in reality:

- **Volatility clusters:** A big down day tends to be followed by more volatile days (GARCH effects)
- **Autocorrelation:** Some strategies have momentum — today's return predicts tomorrow's direction
- **Path-dependency:** If you hold a position for 10 days, the return over those 10 days depends on the *sequence* of daily returns, not just their final distribution

Monte Carlo can simulate **processes** — not just distributions. You can specify:

$$r_t = \mu + \phi \cdot r_{t-1} + \epsilon_t$$

where today's return depends on yesterday's return. Or:

$$r_t = \mu + \sigma_t \cdot \epsilon_t, \quad \sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \sigma_{t-1}^2$$

This is a GARCH(1,1) process — volatility today depends on yesterday's shock and yesterday's volatility. **You can't reduce this to two parameters and a formula.** But you can simulate from it.

### Gap 3: Multi-Asset Portfolios With Complex Dependencies

Parametric VaR for a portfolio uses the covariance matrix Σ: VaR = μ_p − z_α · σ_p, where σ_p = √(w'Σw). This assumes linear correlations capture all dependencies.

But what if:
- Assets have **tail dependence** (they crash together more than they boom together)?
- Dependencies are **nonlinear** (FX and equities correlate differently in up vs down markets)?
- You want to simulate from a **copula** — a model that captures dependence structure separately from marginal distributions?

Monte Carlo can simulate correlated returns from any joint distribution you specify, including ones with nonlinear dependence structures.

---

## The Unifying Insight

Historical VaR asks: *"What happened?"*

Parametric VaR asks: *"What would happen if returns were normal?"*

Monte Carlo VaR asks: *"What would happen if returns followed this specific process I've modeled?"*

The simulation engine lets you specify **any data-generating process you can write down** — not just the ones with convenient formulas. The price you pay is computation. The benefit is that you're no longer limited to what's mathematically tractable.

---

## Check-In

I've laid out three gaps. But let me test one thing before we go further:

**You mentioned "relationship between observations." Can you give me a concrete example — from markets you've observed or from Spreadex's positions — where the *sequence* of returns would matter, not just their distribution?** 

In other words: when would knowing that a big down day was followed by another big down day (vol clustering) change your risk assessment, compared to just knowing that big down days happen 5% of the time?