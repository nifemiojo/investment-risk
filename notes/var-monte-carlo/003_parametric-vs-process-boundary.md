# You're Right — Let Me Fix the Framing

**Date:** 2026-07-10
**Topic:** Clarifying what's a genuine limitation of parametric VaR vs what's just computational convenience

---

## Your Pushback

You pointed out: parametric VaR is flexible to other distributions — we established that in the parametric session. So saying "no closed-form quantile" as a Monte Carlo advantage is weak, because:

- Student's t? `scipy.stats.t.ppf(0.05, df=4)` works fine.
- Skewed-t? Numerical inversion exists.
- Most distributions you'd actually use? The quantile is computable.

You're correct. Let me redraw the boundary properly.

---

## What Parametric VaR Can Actually Do

The parametric framework is:

$$\text{VaR}_\alpha = Q_\alpha(\text{distribution} \mid \text{parameters estimated from data})$$

where $Q_\alpha$ is the α-quantile function.

**Terms:**
- $\text{VaR}_\alpha$: Value at Risk at confidence level $1-\alpha$
- $Q_\alpha$: the α-quantile (inverse CDF) of the chosen distribution
- distribution: any distribution whose quantile function is computationally accessible

This works for:
- Normal (μ̂, σ̂) → `norm.ppf(α, loc=μ̂, scale=σ̂)`
- Student's t (μ̂, σ̂, ν̂) → `t.ppf(α, df=ν̂, loc=μ̂, scale=σ̂)`
- Any distribution in scipy's catalog

The limitation isn't "can't compute the quantile." It's deeper.

---

## The Real Boundary: Distributions vs Processes

### What Parametric VaR Needs

Parametric VaR requires that you can characterize the **single-period return distribution** with a fixed set of parameters. Once you have those parameters, you compute one quantile, and you're done.

This means parametric VaR assumes:

1. **Returns are independent across periods.** Day 1 and day 2 are separate rolls from the same distribution. The parameters (μ̂, σ̂) are fixed.

2. **The distribution is stationary within the estimation window.** The same μ̂, σ̂ describe every day in the window.

3. **The portfolio return is a linear function of asset returns.** Portfolio return = w₁r₁ + w₂r₂ + ... — the quantile of the weighted sum can be computed from the joint distribution.

### Where This Breaks

**Break 1: When the process matters, not just the distribution.**

Consider a GARCH(1,1) process:

$$r_t = \mu + \sigma_t \cdot \epsilon_t$$

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \sigma_{t-1}^2$$

**Terms:**
- $r_t$: return at time t
- $\sigma_t^2$: conditional variance at time t (volatility *today*)
- $\omega$: baseline variance level
- $\alpha$: how much yesterday's shock feeds into today's volatility
- $\beta$: how much yesterday's volatility persists into today
- $\epsilon_t$: random shock, typically $\epsilon_t \sim N(0,1)$

The single-period distribution of $r_t$ in a GARCH process is *still* approximately normal (actually heavier-tailed, but let's set that aside). You could estimate μ̂ and σ̂ from a GARCH sample and plug them into the parametric formula.

**But you'd miss the point.** In a GARCH world, the risk *tomorrow* depends on what happened *today*. If today was a −3% shock, tomorrow's σ is elevated. The parametric formula, which averages over all days, gives you the *unconditional* VaR — what the risk looks like on an average day. It can't tell you: *given that today crashed, what's tomorrow's VaR?*

Monte Carlo can. You simulate day 1 → compute σ₂ from the GARCH equation → simulate day 2 with that elevated σ₂. The sequence matters.

**Break 2: When the portfolio isn't a linear function of returns.**

If your portfolio contains options, the P&L is a nonlinear function of the underlying. A 1% move isn't 10× a 0.1% move — gamma bends the payoff.

Parametric VaR with a covariance matrix assumes:
$$\text{Portfolio return} = \sum w_i r_i$$

But for an option book:
$$\text{Portfolio P\&L} = f(S_1, S_2, ..., \sigma_1, \sigma_2, ..., \tau)$$

where $f$ is a pricing function — nonlinear, multi-input, path-dependent. There's no simple quantile formula for this. You simulate the inputs, reprice the book for each scenario, and sort the P&Ls.

**Break 3: When you need a multi-period path, not a single-period return.**

10-day VaR under parametric is: 1-day VaR × √10. This √t scaling assumes independent, identically distributed returns — the same assumption we just undermined. If returns have autocorrelation or volatility clustering, √10 scaling is wrong in ways that can't be fixed by tweaking a parameter. You need to simulate the 10-day path, day by day, letting each day's outcome feed into the next day's parameters.

---

## The Fixed Boundary

| | Parametric VaR | Monte Carlo VaR |
|---|---|---|
| **Assumes** | Single-period distribution with fixed parameters | A data-generating *process* you simulate from |
| **Handles** | Any distribution with a computable quantile | Any process you can code |
| **Captures** | What the return looks like on an average day | What the return looks like *given what just happened* |
| **Portfolios** | Linear (weighted sum of returns) | Nonlinear (full revaluation of positions) |
| **Multi-period** | √t scaling | Simulate the actual path |

---

## Check-In

The key distinction isn't "can you compute the quantile" — it's "can you reduce the problem to a single-period, fixed-parameter distribution."

Here's the question I want you to sit with: **At Spreadex, do you hold positions where the P&L is nonlinear in the underlying?** Options obviously. But what about the autohedging itself — does the hedging create path-dependency? If the system hedges more aggressively after a loss, does that make tomorrow's risk depend on today's outcome?