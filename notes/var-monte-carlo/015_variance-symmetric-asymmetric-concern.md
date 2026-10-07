# The Variance Problem: Symmetric Measure for Asymmetric Concern

**Date:** 2026-07-10
**Topic:** Why variance treats rallies and crashes the same — and what that means for risk models

---

## The Tension You Identified

GARCH feeds on $r_{t-1}^2$. A +5% rally and a −5% crash produce the same squared return (0.0025), so they spike tomorrow's volatility by the same amount.

But your concern as a risk manager after a +5% rally is very different from your concern after a −5% crash:

- **After a +5% rally:** Your position is worth more. You have more cushion. If anything, you might be *less* worried about hitting a loss limit. Yet GARCH says: "volatility is elevated — widen the VaR limit."

- **After a −5% crash:** Your position is worth less. You're closer to limits. You're genuinely more worried. GARCH says the same thing: "volatility is elevated" — but this time it aligns with your intuition.

The model can't tell the difference between "good volatility" and "bad volatility." And you're right: variance, by definition, can't.

---

## The Empirical Reality: It's Actually Worse Than Symmetric

The model says +5% and −5% have equal effects on future volatility. But empirically, they don't.

**The leverage effect:** Negative returns increase future volatility *more* than positive returns of the same magnitude.

There are two explanations:

### 1. The Mechanical Leverage Story

When a firm's stock price falls, its debt-to-equity ratio rises. The equity becomes a riskier claim on the same assets. Higher leverage → higher equity volatility.

$$\text{Leverage} = \frac{\text{Debt}}{\text{Equity}} \uparrow \text{ when stock price } \downarrow$$

This is mechanical: the same dollar amount of debt is now a larger fraction of a smaller equity value. So volatility increases. This effect is asymmetric — it operates on the downside, not the upside.

### 2. The Volatility Feedback Story

When volatility spikes, investors demand higher risk premiums. Higher required returns → lower prices. Lower prices → more uncertainty. It's a feedback loop: vol ↑ → price ↓ → vol ↑. This runs in the opposite direction for positive returns, but the effect is weaker — rallies don't trigger the same fear-driven repricing.

### The Empirical Magnitude

In equity markets, a −1% shock typically increases next-day volatility about 1.5× to 2× as much as a +1% shock. The standard GARCH model misses this entirely.

---

## Models That Fix This

### GJR-GARCH (Glosten-Jagannathan-Runkle)

Adds a dummy variable that activates only for negative returns:

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \gamma \cdot r_{t-1}^2 \cdot I_{t-1} + \beta \cdot \sigma_{t-1}^2$$

where $I_{t-1} = 1$ if $r_{t-1} < 0$, and $0$ otherwise.

**Terms:**
- $\gamma$: the extra effect of a *negative* shock on volatility (the leverage parameter)
- $I_{t-1}$: indicator — flips on for negative returns

Now:
- $r_{t-1} = +5\%$: effect = $\alpha \cdot 0.0025$ (standard)
- $r_{t-1} = -5\%$: effect = $(\alpha + \gamma) \cdot 0.0025$ (amplified)

### EGARCH (Exponential GARCH)

Models the log of variance and allows the sign of the shock to matter:

$$\ln(\sigma_t^2) = \omega + \alpha \cdot \left|\frac{r_{t-1}}{\sigma_{t-1}}\right| + \gamma \cdot \frac{r_{t-1}}{\sigma_{t-1}} + \beta \cdot \ln(\sigma_{t-1}^2)$$

**Terms:**
- $\alpha$: magnitude effect (how big the shock was, regardless of sign)
- $\gamma$: sign effect (negative if leverage effect exists — negative shocks raise vol more)

---

## The Deeper Point: Is Variance Even the Right Measure?

You're raising a question that goes beyond GARCH specifications. If we only care about downside risk, why are we using a symmetric measure at all?

**Semi-variance** only counts observations below a threshold (usually the mean or zero):

$$\text{Semi-variance} = \frac{1}{n}\sum_{i=1}^{n} \min(r_i - \mu, 0)^2$$

This is the foundation of the **Sortino ratio** (which replaces Sharpe's standard deviation with downside deviation).

But semi-variance models for time-varying risk are much less developed than GARCH. The field has mostly stuck with symmetric variance because:
- It's mathematically tractable
- It connects to option pricing (Black-Scholes uses σ, not semi-σ)
- In practice, the symmetric version works reasonably well — the leverage asymmetry is real but not enormous

---

## What This Means for Monte Carlo VaR

You can simulate from a GJR-GARCH or EGARCH process instead of standard GARCH. Monte Carlo doesn't care — it simulates whatever process you specify.

The point is: **every modeling choice has consequences.** Standard GARCH treats rallies and crashes equally. That's a choice you're making, whether you realize it or not. GJR-GARCH or EGARCH are better, but they require estimating an additional parameter (γ), which adds estimation risk.

The Monte Carlo principle remains: **you get out what you put in.** If your process model treats upside and downside symmetrically, your VaR will too. If you want asymmetry, you need to specify it in the model.

---

## Check-In

You've identified a real limitation: variance is symmetric but risk concern is asymmetric. The standard GARCH inherits this symmetry. There are fixes (GJR-GARCH, EGARCH), but they add complexity.

The meta-point: **every model has assumptions baked into its structure.** Part of being dangerous-good at this is recognizing which assumptions are in play and whether they matter for the decision at hand.

Does this land? And do you want to continue with GARCH (estimation, simulation) or move to Monte Carlo's failure modes?