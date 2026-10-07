# Simulation Frequency and Horizon: Two Clarifications

**Date:** 2026-07-10
**Topic:** When you need daily steps vs direct draws, and why you'd simulate longer horizons

---

## Question 1: If Parameters Are Estimated From 10-Day Data

You asked: if μ̂ and σ̂ are estimated from 10-day return observations, do you still need 10 daily steps per path?

**No.** You can draw directly from the 10-day distribution.

The simulation frequency should match the *process dynamics you're modeling*, not some fixed rule. Three cases:

### Case A: Simulating From a Distribution

If you're just sampling from a distribution (no process, no path-dependency), draw at whatever frequency your parameters are estimated at.

```
10-day μ̂ = 0.5%, 10-day σ̂ = 3.8%
→ Draw 10,000 ten-day returns directly from N(0.5%, 3.8%²)
→ One draw per scenario. No paths needed.
```

The frequency of the underlying data is irrelevant. You're not simulating a process — you're sampling from a distribution. One draw = one 10-day return.

### Case B: Simulating From a Process Estimated on 10-Day Data

This is trickier. If you estimate a GARCH model on 10-day returns, the parameters describe 10-day-to-10-day dynamics. You'd simulate 10-day steps:

```
Path i: r_10d(t=1) → r_10d(t=2) → ... → r_10d(t=H_10d)
```

But this is unusual. GARCH effects mostly matter at daily frequency. A volatility shock on day 1 of a 10-day period affects days 2–10 *within* that period. Estimating GARCH on 10-day data loses this intra-period dynamic.

### Case C: The Typical Setup

Most commonly in practice: you estimate the process on daily data, then simulate paths at daily frequency to whatever horizon you need.

```
Daily data → estimate GARCH(1,1) → simulate 10,000 paths × 10 days
```

The daily data gives you the daily dynamics. The 10-day VaR comes from aggregating the simulated paths — no shortcut available. This is the computationally expensive case.

### The General Rule

**Simulate at the frequency where the dependence structure lives.** If returns are independent, simulate at whatever frequency is convenient. If there's daily autocorrelation or volatility clustering, you need daily steps — regardless of what horizon VaR you want.

---

## Question 2: When Would Longer Horizons Be Useful?

You correctly identified that longer horizons compound modeling errors. So why bother?

### The Obvious Answer: Because Someone Needs It

- **Basel regulations** require 10-day VaR for market risk capital
- **Illiquid positions** can't be unwound in a day — the risk horizon is however long it takes to exit
- **Monthly/quarterly reporting** — boards and investors think in longer horizons
- **Strategic decisions** — "what's the worst plausible drawdown over the next quarter if we put on this position?"

### The Less Obvious Answer: Because √t Scaling Is Wrong

If you have a process with dependence, the 10-day VaR is **not** √10 × 1-day VaR. You can't compute it from the 1-day number. You need to simulate the actual paths.

$$\text{If } r_t \text{ has autocorrelation } \rho: \quad \sigma_{h\text{-day}} = \sigma_{1\text{-day}} \cdot \sqrt{h + 2\sum_{k=1}^{h-1}(h-k)\rho_k}$$

**Terms:**
- $\sigma_{h\text{-day}}$: volatility over h days
- $\rho_k$: autocorrelation at lag k
- $h$: horizon in days

If $\rho_k > 0$ (momentum): the h-day volatility is **higher** than √h · σ₁. The √t rule underestimates risk.

If $\rho_k < 0$ (mean reversion): the h-day volatility is **lower** than √h · σ₁. The √t rule overestimates risk.

### The Compounding Errors Point

You're right that longer horizons expose you to model misspecification. If you GARCH model is wrong, the error in your 10-day VaR gets amplified relative to your 1-day VaR. But that's not an argument against simulating longer horizons — it's an argument for **backtesting at multiple horizons** and being humble about the model.

The alternative — using √t scaling and ignoring dependence — is guaranteed to be wrong whenever dependence exists. Monte Carlo with a misspecified process may be wrong too, but it's at least *trying* to capture the structure.

---

## Check-In

So the two clarifications:

1. **Simulation frequency = where the dependence lives.** If there's no dependence (pure distribution), draw at whatever frequency is convenient. If there's daily dependence, simulate daily.

2. **Longer horizons are needed when someone asks for them** — regulators, illiquid positions, strategic decisions. And √t scaling is the wrong way to get there if dependence exists.

Does that clear it up? And here's the next thread to pull on: **if you simulate a GARCH process for 10-day VaR, what parameters does the GARCH model need, and how do you estimate them?** That's the bridge from "Monte Carlo is flexible" to "Monte Carlo in practice."