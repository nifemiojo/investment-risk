# The True Return-Generating Process — the Unobservable Source of Everything

**Date:** 2026-07-26
**Topic:** The hierarchy from the true return-generating process → observations → empirical distribution → moments. Why the process itself is unobservable, what we can estimate, and what we can't.

---

## Opening Question

> You download 252 daily SPY returns from yfinance. You compute the mean, variance, skewness, kurtosis. You fit a normal distribution. You compute VaR. At every step, you're working with *outputs* — the numbers that happened. But behind every one of those numbers is a vast, complex, unobservable machine that produced them: the true return-generating process.
>
> What is that machine? Why can't we see it? And if we can't see it, what exactly are we doing when we compute VaR?

---

## 1. The Hierarchy — From Source to Summary

There's a chain of abstraction from the deepest reality to the numbers you compute. Here it is, top to bottom:

```
LEVEL 1: THE TRUE RETURN-GENERATING PROCESS
         The actual causal machinery that produces returns.
         Unobservable. Complex. Time-varying.
              │
              │ generates
              ▼
LEVEL 2: OBSERVED RETURNS
         The numbers that actually happened.
         x₁, x₂, ..., xₙ. This is all you get to see.
              │
              │ you summarise
              ▼
LEVEL 3: THE EMPIRICAL DISTRIBUTION
         Tabulation of observed returns.
         "What shape did the data take?"
              │
              │ you compute
              ▼
LEVEL 4: SAMPLE MOMENTS
         x̄, s², γ̂₁, γ̂₂
         "What are the summary characteristics of the shape?"
              │
              │ you use
              ▼
LEVEL 5: VaR, RISK MEASURES, DECISIONS
         The numbers you actually act on.
```

Every level is a compression of the level above it. Each step loses information. The question is: does it lose the information you *need*?

---

## 2. Level 1 — What Is the True Return-Generating Process?

### A concrete picture

It's 9:30 AM on a Tuesday. The SPY opens. Over the next 6.5 hours, millions of market participants — pension funds, hedge funds, market makers, retail traders, algorithms — place orders. Each order is driven by:

- New information (earnings, economic data, Fed statements, geopolitical events)
- Existing positions (someone needs to hedge, someone needs to rebalance, someone is margin-called)
- Flows (pension contributions hitting the market at month-end, ETF creation/redemption)
- Microstructure (bid-ask spreads, order book depth, market maker inventory)
- Sentiment (fear, greed, narrative shifts, social media)
- Rules and constraints (risk limits, regulatory capital, mandate restrictions)
- Feedback loops (falling prices trigger stop-losses, which trigger more falling prices)

All of these interact simultaneously. There are second-order effects (falling prices change sentiment, which changes flows). There are cross-asset spillovers (SPY moves affect VIX, which affects options hedging, which affects SPY). There are regime shifts (a volatility spike changes everyone's behaviour at once).

At 4:00 PM, the market closes. SPY's return for the day is, say, −1.3%.

**That number — −1.3% — is the single output of an incomprehensibly complex process.** The process itself — all those causal forces interacting — is the true return-generating process.

### What makes it "true"

The true process is not a model. It's not a distribution. It's not an equation. It's reality — the actual physical-and-informational system that produces asset prices.

The true process:
- **Exists** whether or not you model it
- **Has no parameters** — it's not $N(\mu, \sigma^2)$ with some true $\mu$ and $\sigma$. It's the real thing, which may not be describable by any simple parametric form
- **Is probably non-stationary** — the rules of the game change. Regulation changes. Market structure changes. The dominant participants change. The true process in 2025 is not the same as the true process in 2005
- **Has memory** — yesterday's return affects today's behaviour (volatility clustering, trend-following, mean-reversion)
- **Contains feedback** — the process observing itself changes the process (if everyone uses the same VaR model, breach-triggered selling creates the very tail risk the model was measuring)

---

## 3. Why the True Process Is Unobservable

You cannot see the true return-generating process. You can only see its outputs — the realised returns. Here's why:

### Reason 1: You only see one path

The true process generates *one* history. You see the returns that happened: −1.3%, +0.5%, −0.2%, ... You never see the returns that *could have* happened but didn't. If the Fed had said something slightly different, or if a large pension fund had rebalanced a day earlier, the returns would have been different. You can't observe those counterfactuals.

This is the fundamental problem of inferring a process from a single realisation. You have one draw from an immensely complex system, and you're trying to infer the system's properties from that single draw.

### Reason 2: The process is inside a black box

You observe: price → return. You don't observe:
- Who placed which order and why
- What information arrived when
- What internal risk models triggered which trades
- What feedback loops were operating

The causal mechanisms are hidden. All you see is the net result.

### Reason 3: The process changes over time

Even if you could perfectly characterise the process for 2018–2023, that characterisation might not hold for 2024–2025. The process is non-stationary. The "true" process is a moving target.

### Reason 4: Observation affects the process

This is the reflexivity problem. If every bank adopts the same VaR methodology, and they all get the same breach signal on the same day, and they all reduce risk simultaneously, the selling pressure creates a crash. The act of measuring risk *changes* the risk. The observer is inside the system being observed.

---

## 4. What We Do Instead — Models as Approximations

Since we can't observe the true process, we build models of it. A model is a simplified description that captures *some* features of the true process while ignoring others.

### The modelling hierarchy

| What we want to know | What we use | What we lose |
|---------------------|-------------|--------------|
| The true process (reality) | A model of the process | Everything the model omits |
| The model's parameters | Estimates from data | Sampling error |
| The model's predictions | Point estimates + confidence intervals | Model error + estimation error |

### A model makes three kinds of choices

**1. Structural choices — what kind of thing is the process?**

- "Returns are independent draws from a fixed distribution" (i.i.d. assumption)
- "Returns have time-varying volatility" (GARCH)
- "Returns switch between two regimes" (regime-switching model)
- "Returns are driven by latent factors" (factor models)

Each is a bet about the nature of the true process.

**2. Distributional choices — what shape does the randomness take?**

- Normal distribution (symmetric, thin tails)
- Student's t (symmetric, adjustable tails)
- Skewed-t (asymmetric, adjustable tails)
- Empirical (no shape assumption — use the data's shape directly)

**3. Parameter choices — what numbers go into the model?**

- $\mu$ and $\sigma$ for a normal distribution
- $\nu$ (degrees of freedom) for a t-distribution
- $\lambda$ (decay factor) for EWMA volatility
- The window length (252 days? 60 days?)

---

## 5. The Process vs Distribution Distinction — This Is Critical

A **probability distribution** is a static object. It's a mathematical function $f(x)$ that assigns probabilities to outcomes. It has fixed moments. It has no memory — each draw is independent of the last.

A **stochastic process** is a sequence of random variables indexed by time. It *can* have memory — today's outcome can depend on yesterday's. It can be non-stationary — the distribution can shift over time. It can have feedback.

### The hierarchy

```
STOCHASTIC PROCESS           "How returns evolve through time"
    │                        (May have memory, may be non-stationary)
    │
    │  At a single point in time, the process implies a...
    ▼
CONDITIONAL DISTRIBUTION     "The distribution of tomorrow's return,
    │                         given everything we know today"
    │
    │  If the process is stationary, this is the same at every t...
    ▼
UNCONDITIONAL DISTRIBUTION   "The distribution of returns ignoring
                             time — pooling all observations"
```

Most of what you do with historical VaR collapses the process into an unconditional distribution. You take 252 returns, pool them, and treat them as draws from a single distribution. You're implicitly assuming:

1. The process is stationary over 252 days (the distribution doesn't change)
2. The returns are independent (no memory — yesterday doesn't affect today)

Both assumptions are false. Volatility clusters. Correlations shift. Regimes change. But for a 1-day VaR at 95% confidence with 252 days of data, the approximation often works *well enough* — which is why historical VaR is widely used despite its known flaws.

### When the approximation breaks

- During a regime change (the distribution shifts, but you're still using stale data)
- During a volatility spike (returns are no longer i.i.d. — large moves cluster)
- During a correlation breakdown (the relationship between assets changes)

These are exactly the moments when you most need accurate risk measurement — and exactly when the "returns are i.i.d. draws from a fixed distribution" assumption fails hardest.

---

## 6. What "Estimation" Actually Means at Each Level

When you say "we can only estimate the true process," you're compressing several distinct estimation problems:

### Level 1 → 2: You don't estimate the process. You observe its outputs.

This isn't estimation — it's measurement. You download the closing prices. They are what they are. No model involved (yet).

### Level 2 → 3: You summarise the outputs into an empirical distribution.

$$\hat{F}_n(x) = \frac{1}{n}\sum_{i=1}^n \mathbf{1}\{x_i \leq x\}$$

This is the empirical CDF. It's a nonparametric estimate of the true (unconditional) CDF. The error here is **sampling error**: your 252 days are a finite sample. If you had a different 252-day window, the empirical CDF would be different.

### Level 3 → 4: You compute sample moments.

$$\bar{x} = \frac{1}{n}\sum x_i, \quad s^2 = \frac{1}{n-1}\sum (x_i - \bar{x})^2, \quad \ldots$$

These are point estimates of the empirical distribution's moments. The error here is the **variance of the estimator** — each moment has its own sampling distribution. The sample mean of 252 observations has a standard error of $s/\sqrt{252}$. The sample skewness has a much larger standard error.

### Level 4 → 5: You compute VaR.

If historical VaR: $\widehat{\text{VaR}}_{\alpha} = \hat{F}_n^{-1}(\alpha)$ — you read a quantile from the empirical CDF. The error is entirely sampling error in $\hat{F}_n$.

If parametric VaR: $\widehat{\text{VaR}}_{\alpha} = \bar{x} - z_{\alpha} \cdot s$ — you assume a theoretical distribution and plug in estimates. The error is **sampling error + model error** (the normal distribution might be the wrong shape).

### The estimation chain

```
TRUE PROCESS (unobservable, complex, time-varying)
     │
     │ You observe ONE path (not the full process)
     ▼
OBSERVED RETURNS (the data — this is what you have)
     │
     │ You estimate the unconditional distribution from the data
     ▼
EMPIRICAL DISTRIBUTION (an estimate of the unconditional distribution)
     │
     │ You compute summary statistics
     ▼
SAMPLE MOMENTS (estimates of the empirical distribution's moments,
                which are estimates of the unconditional distribution's moments,
                which are properties of an approximation of the process)
     │
     │ You plug estimates into a formula (parametric) or read directly (historical)
     ▼
VaR ESTIMATE
```

Every arrow is a source of error. Every level compresses and approximates the level above it. The VaR number at the bottom is the product of all those approximations.

---

## 7. What This Means for VaR — the Practical Take

### You are always wrong. The question is: wrong in what way, and by how much?

Every VaR number is an estimate of an estimate of an approximation. It is not the "true" VaR of the "true" process — there is no such thing. The true process doesn't have a VaR parameter. VaR is a property of a distribution, and the true process isn't a distribution. 

So you're not estimating a true parameter. You're computing a number that would be the quantile *if* the process were stationary and *if* the future resembled the past and *if* your sample was representative. None of these "ifs" are true. But that doesn't mean VaR is useless — it means you need to understand what it's actually telling you.

### VaR is a measurement, not a prediction

Think of VaR like a thermometer, not a weather forecast. A thermometer tells you the current temperature — it's a measurement. It doesn't predict tomorrow's temperature, though you might use today's reading to inform your guess.

Historical VaR tells you: "If the next 252 days look like the last 252 days, then the 5th percentile of returns is −2.1%." It's a description of the recent past, projected forward as a baseline. It's not claiming to predict the future. It's saying: "This is what normal looks like. If tomorrow is worse than this, it's an unusual day."

### Three things you can actually estimate

| What | How | How much to trust it |
|------|-----|---------------------|
| The unconditional distribution of returns over the recent past | Empirical CDF from the window | Reasonably well, if the window is long enough and the process is approximately stationary over it |
| The unconditional moments of that distribution | Sample moments | Mean and variance: fairly well. Skewness and kurtosis: much less well — use as directional signals |
| Whether tomorrow will look like yesterday | Breach rates over the backtest period | You can test this: if breaches cluster or exceed the expected rate, the "tomorrow = yesterday" assumption is violated |

---

## 8. An Analogy That Might Help

Imagine you're standing outside a factory. Every day at 4 PM, a number comes out on a screen. You record the numbers for a year: 252 numbers.

You don't know what's inside the factory. You don't know what machines are running, what raw materials they're using, who's operating them, or whether the factory was recently retooled. All you see are the numbers.

You compute the average (0.04), the standard deviation (1.2), the skewness (−0.6), the kurtosis (6.2). You note that the numbers seem to come in clusters — calm weeks followed by wild weeks. You notice that extreme negative numbers are more common than extreme positive ones.

You can do useful things with this information. You can say: "95% of the time, the number is above −2.1%." You can monitor whether the variability is rising. You can flag days when the number is unusually negative.

But you cannot open the factory door. You cannot see the machines. You cannot know whether the factory has changed its production process. You cannot predict when a machine will break.

**The factory is the true return-generating process. The numbers on the screen are the observed returns. Everything you compute — moments, distributions, VaR — is an attempt to infer the properties of the factory from the numbers on the screen, without ever opening the door.**

---

## 9. The Map Is Not the Territory

This is the deepest point, and it's worth sitting with:

| The territory | The map |
|--------------|---------|
| The true return-generating process | Any model of it |
| Reality | Our description of reality |
| What actually produces returns | What we assume produces returns |
| Infinitely complex | Finitely parameterised |
| Non-stationary, evolving | Usually assumed stationary |
| Has feedback, memory, interaction | Often assumed i.i.d. |

The map is useful. Without it, you can't navigate. But the map is not the territory, and the most dangerous thing you can do is forget the difference.

When a VaR model has worked well for three years (breach rates close to 5%), the temptation is to believe the model *is* the process. It's not. It's a map that happened to be accurate during a period when the territory was stable. When the territory shifts — a new crisis, a new regime, a new market structure — the old map becomes misleading.

**A good risk manager uses the map but never confuses it with the territory. A great risk manager watches for signs that the territory has changed.**

---

## 10. Where This Shows Up In Your Phase 1 Work

| Phase 1 decision | What it implicitly assumes about the process |
|-----------------|---------------------------------------------|
| Using a 252-day window | The process is approximately stationary over the past year |
| Using decay weighting (λ=0.94) | The process is non-stationary — recent observations are more relevant |
| Monitoring correlation dynamics | The process's second-moment structure changes over time |
| The combined method (equal + decay) | The process has both a stable long-run component and a time-varying short-run component |
| The escalation ladder (green → red) | The process can shift between regimes, and you need rules for when to act |
| Vol scaling (returns divided by trailing vol) | The process's volatility changes, but its *standardised* shape (higher moments) is stable |

Each of these is a practical response to the gap between the simple model (i.i.d. stationary) and the complex reality (non-stationary, time-varying volatility, shifting correlations).

---

## 11. Questions to Test Your Understanding

1. **"The true process is unobservable." Does this mean we know nothing about it? If not, what *can* we know?**

2. **You say the process can change over time. If it changed yesterday, how long would it take your 252-day empirical distribution to fully reflect the new process?** (Hint: 252 days. For the first 100 days after the change, your distribution is a mix of old-regime and new-regime observations.)

3. **If the true process has memory (volatility clusters), and you treat returns as i.i.d., what specific thing goes wrong with your VaR estimate?** (Hint: after a volatility spike, your VaR based on the past 252 days — which mostly contains calm days — will be too low. The clustering means large moves aren't independent; they come in waves.)

4. **Why doesn't the true process have a "true VaR"?** (VaR is a property of a distribution. The process isn't a distribution — it's a mechanism that *generates* a distribution at each point in time, conditional on the past. The concept of "the 5th percentile of the process" only makes sense if you specify: the 5th percentile of what? The unconditional distribution? Tomorrow's conditional distribution?)

5. **A quant says: "My model is well-calibrated — the 95% VaR has been breached 5.1% of the time over 5 years." Is the model correct? Or just lucky? How would you tell?** (Think about: what happened during those 5 years? Was it a stable period? Did the model pass Christoffersen's conditional coverage test — were breaches randomly distributed, or clustered?)

---

## What's Next

This is the philosophical foundation. Everything that follows builds on it:

- **The normal distribution deep dive** — the simplest possible model of the process: i.i.d. draws from $N(\mu, \sigma^2)$. Why it's the starting point, what it gets right, and everything it gets wrong.
- **Estimators and their properties** — now that you know you're estimating properties of an approximation of an unobservable process, how do you judge whether an estimator is any good? Bias, variance, consistency, and why Bessel's correction ($n-1$) exists.
- **Stationarity deep dive** — the single most important assumption in time series work. What it means, how to test it, and what to do when it's violated (which, in finance, is always).
