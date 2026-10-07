# Monte Carlo VaR: Failure Modes and Limitations

**Date:** 2026-07-10
**Topic:** What happens when Monte Carlo VaR breaks — the specific ways it fails, why, and what practitioners do about it

---

## The Meta-Failure Mode

Every other VaR method has a clean failure story:

- **Historical VaR fails when:** the past stops looking like the future (regime change, window cliff)
- **Parametric VaR fails when:** the distributional assumption is wrong (fat tails, skew, vol clustering)

Monte Carlo's failure is more insidious because **the simulation itself doesn't fail** — it always produces a number. The failure is that the number is wrong in ways that are harder to detect.

> Historical VaR can be wrong. Parametric VaR can be wrong. But Monte Carlo VaR can be **precisely** wrong — and look convincing while doing it.

---

## Failure Mode 1: Garbage In, Garbage Out (Model Risk Amplification)

### What It Looks Like

You fit a GARCH(1,1) to 5 years of daily data. The parameters look reasonable: ω = 0.00001, α = 0.08, β = 0.88. You simulate 10,000 paths. The VaR is £25,500.

But α and β were estimated with error. The standard error on β is ±0.05. If β is actually 0.83 instead of 0.88, the 10-day VaR could be £21,000. If β is 0.93, it could be £31,000.

Monte Carlo doesn't just inherit model risk — it **amplifies** it. Every error in every parameter propagates through thousands of paths and compounds over the horizon. A small error in β becomes a large error in 10-day VaR.

### Why It's Dangerous

With parametric VaR, you plug in σ̂ and get one number. The formula is transparent — you can see exactly how σ̂ drives the result. With Monte Carlo, the parameter → VaR mapping is opaque. You can't trace "this VaR is high because β was estimated 2% too high."

### Mitigation

- **Parameter uncertainty analysis:** Don't just report the VaR — report the range of VaR under parameter uncertainty. "VaR is £25,500, with a 90% confidence interval of £21,000–£31,000 given estimation error."
- **Use longer estimation windows** to reduce parameter standard errors
- **Compare with simpler models:** If GARCH Monte Carlo VaR is wildly different from historical VaR, question the GARCH, not history

---

## Failure Mode 2: Sampling Error in the Tail

### What It Looks Like

You run 10,000 simulations. The 500th-worst outcome is −2.54%. You report 95% VaR = £25,400.

You run it again with a different random seed. The 500th-worst is −2.61%. VaR = £26,100.

You run it a third time. −2.48%. VaR = £24,800.

The true VaR (the one you'd get with infinite simulations) is £25,500. Your estimate bounces around with a standard error of roughly:

$$SE \approx \frac{\sigma \cdot f(z_\alpha)}{\sqrt{N \cdot \alpha \cdot (1-\alpha)}}$$

**Terms:**
- $SE$: standard error of the VaR estimate
- $\sigma$: the volatility
- $f(z_\alpha)$: the density at the quantile (how "thick" the tail is at that point)
- $N$: number of simulations
- $\alpha$: the tail probability (0.05 for 95% VaR)

For 10,000 paths at 95%: the standard error is about 3–5% of the VaR estimate. For 99% VaR, it's 8–12% — because you're estimating from only 100 tail observations instead of 500.

### Why It's Dangerous

You might adjust positions or hedges based on a VaR that moved £1,300 because of sampling noise, not because risk actually changed. Two analysts running the same model on the same data with different random seeds get different answers. This erodes trust.

### Mitigation

- **Use more paths for higher confidence levels:** 50,000+ for 99% VaR
- **Report the Monte Carlo standard error alongside the VaR**
- **Use variance reduction techniques:** antithetic variates, control variates, importance sampling
- **Fix the random seed for reproducibility** in production, but test sensitivity to the seed

---

## Failure Mode 3: The Calibration Illusion

### What It Looks Like

A GJR-GARCH with skewed-t shocks has 6 parameters. You estimate them from 1,260 daily observations (5 years). The model fits beautifully in-sample. You simulate 10,000 paths. The output looks authoritative.

But 1,260 observations to estimate 6 parameters is barely adequate. The parameters are noisy. And the 10,000 paths create an illusion of precision that has nothing to do with the quality of the inputs.

The signal-to-noise ratio is:

$$\frac{\text{Simulation paths}}{\text{Calibration observations}} = \frac{10{,}000}{1{,}260} \approx 8$$

You're generating 8× more simulated data than the real data the model was built on. The simulation doesn't add information — it just makes the existing (noisy) information look more precise.

### Why It's Dangerous

Users see 10,000 paths and assume the model is well-grounded. They don't see that all 10,000 paths are drawn from a distribution estimated from 1,260 noisy observations. The apparent precision is fake.

### Mitigation

- **Always report the estimation sample size alongside the number of paths**
- **Prefer simpler models** unless complexity demonstrably improves out-of-sample performance
- **Use rolling window validation:** fit on 2009–2013, test on 2014. Fit on 2010–2014, test on 2015. Does the VaR hold up?

---

## Failure Mode 4: Right Model, Wrong Regime

### What It Looks Like

You calibrate your GARCH model on 2019–2023 data. The model captures the COVID volatility spike well. You're confident. It's January 2026. The model says 95% 1-day VaR is £20,000.

Then an event hits that's different from anything in the calibration window — a sovereign debt crisis, a currency peg breaking, a geopolitical shock with financial contagion. The model simulates from a world of 2019–2023 dynamics. The actual market is behaving like 2008 or 1998. The VaR is wrong, and it's wrong when you need it most.

### Why It's Dangerous

Monte Carlo simulates from the world you told it about. It cannot simulate a crisis it hasn't been calibrated on. Historical VaR has the same problem, but it's honest about it — "here's what the last 252 days looked like." Monte Carlo pretends to generate a rich set of futures, but they're all futures that look like the past.

### Mitigation

- **Stress testing alongside Monte Carlo:** Run the portfolio through historical crisis scenarios (2008, 2020, 2022) regardless of what the model says
- **Regime-switching models:** Explicitly model calm and crisis regimes with transition probabilities
- **Reverse stress testing:** "What scenario would produce a loss of £X?" instead of "what loss does this scenario produce?"
- **Be explicit about the calibration window and its limitations**

---

## Failure Mode 5: The Correlation Breakdown

### What It Looks Like

Your portfolio has equities and bonds. In the 2019–2023 calibration window, the stock-bond correlation was −0.3 (bonds rallied when stocks fell). The Monte Carlo simulates from this negative correlation. The portfolio looks well-diversified. VaR is moderate.

Then inflation surprises. Stocks AND bonds sell off simultaneously. Correlation goes to +0.6. The diversification benefit vanishes. Your Monte Carlo VaR was calibrated on a world where bonds protected you — that world no longer exists.

### Why It's Dangerous

Diversification is the biggest driver of portfolio VaR. When correlations break, VaR can double or triple overnight. Monte Carlo with a fixed correlation matrix has no way to anticipate this. The model simulates 10,000 futures, but all of them assume the same correlation structure.

### Mitigation

- **Stress correlation matrix to 1:** "What's the VaR if all correlations go to 1?" (the undiversified VaR)
- **Regime-conditional correlations:** Estimate correlations separately for calm and stress periods
- **Rolling correlation monitoring:** Flag when realized correlations deviate from the model's assumption

---

## Failure Mode 6: The Full Revaluation Shortcut

### What It Looks Like

Full revaluation of 10,000 options under 10,000 scenarios is too slow. You use a delta-gamma approximation instead:

$$\text{P\&L} \approx \delta \cdot \Delta S + \frac{1}{2}\gamma \cdot (\Delta S)^2$$

This works fine for small moves. But for the 5th percentile scenarios — the ones that define your VaR — the moves are large. The delta-gamma approximation breaks down. Gamma itself changes with the underlying (it's not constant). Vega risk (vol changes) is completely ignored.

The VaR you get is an approximation of an approximation — simulated returns from an estimated process, valued with a quadratic shortcut.

### Why It's Dangerous

The scenarios that matter most for VaR are the extreme ones — exactly where the approximation is worst. You're using a cheap method precisely where accuracy matters most.

### Mitigation

- **Use delta-gamma-delta for the tail only:** Full revaluation for the worst 1% of scenarios, approximation for the rest
- **Add vega and cross-greeks to the approximation** if vol is a risk factor
- **Compare full revaluation VaR to delta-gamma VaR** periodically to quantify the approximation error
- **If the book is options-heavy, pay for the compute.** If it's mostly linear, don't use Monte Carlo at all.

---

## Failure Mode 7: The Backtesting Problem

### What It Looks Like

You compute a 10-day 95% Monte Carlo VaR. To backtest, you need non-overlapping 10-day periods. 5 years gives you ~126 non-overlapping 10-day windows. At 95%, you expect ~6 exceptions.

With 6 expected exceptions, observing anywhere from 2 to 12 isn't statistically surprising. You can't tell if the model is good or bad with any confidence.

For 99% VaR, you expect ~1 exception per 126 periods. You'd need decades of data to backtest meaningfully.

### Why It's Dangerous

You can run a bad model for years without the backtest catching it. By the time you have enough exceptions to reject the model statistically, you've already lost money. The backtest is too slow to protect you.

### Mitigation

- **Backtest 1-day VaR (more observations), then use the validated 1-day model to simulate 10-day paths**
- **Use overlapping windows** (accept the autocorrelation, but get more data points)
- **Backtest on multiple assets/portfolios simultaneously** to increase the sample
- **Don't rely on statistical tests alone — use judgment.** If the model missed 3 out of 4 recent stress events, it's broken, regardless of what the Kupiec test says.

---

## Failure Mode 8: The Explainability Gap

### What It Looks Like

A trader asks: "Why did VaR go up 15% today?"

With historical VaR: "A big down day from 9 months ago dropped out of the 252-day window." Transparent.

With parametric VaR: "Volatility increased from 1.2% to 1.4%." Transparent.

With Monte Carlo: "The GARCH β parameter, interacting with yesterday's −2% return, elevated the conditional volatility, which propagated through 10,000 paths with skewed-t innovations, and the 5th percentile moved from..." Not transparent.

### Why It's Dangerous

When people can't understand why a number changed, they stop trusting it. They override it with gut feel. The model becomes a compliance checkbox, not a decision tool.

### Mitigation

- **Decompose VaR changes:** "The VaR increase of 15% is driven by: 10% from higher current volatility (after yesterday's move), 3% from updated GARCH parameters (monthly recalibration), 2% from position changes."
- **Always show historical VaR alongside Monte Carlo** as a reality check
- **Build diagnostic dashboards** that show what's driving the VaR, not just the number

---

## Summary

| Failure Mode | Root Cause | Most Dangerous When | Primary Mitigation |
|---|---|---|---|
| **Garbage in, garbage out** | Model risk amplified by simulation | Model is complex, calibration window short | Parameter uncertainty bands |
| **Sampling error** | Finite paths, noisy tail | High confidence (99%), few paths | More paths, variance reduction |
| **Calibration illusion** | 10K paths from 1,260 data points | Complex models (6+ params) | Simpler models, rolling validation |
| **Wrong regime** | Model can't simulate unseen crises | Calm calibration window, looming risks | Stress tests, regime-switching |
| **Correlation breakdown** | Fixed correlation matrix | Diversified portfolios in crises | Stress correlations to 1 |
| **Approximation shortcuts** | Delta-gamma fails in the tail | Options-heavy books, large moves | Full reval for tail scenarios |
| **Backtesting gap** | Not enough non-overlapping periods | Long horizons, high confidence | Backtest 1-day, overlapping windows |
| **Explainability gap** | Black box between inputs and output | Trading desk adoption, limit setting | Decompose VaR changes |

---

## The Practitioner's Posture

The honest Monte Carlo practitioner says:

> "This model produces a number. That number is conditional on: (a) the process being correctly specified, (b) the parameters being accurately estimated, (c) the correlation structure being stable, (d) the future resembling the calibration period, and (e) the revaluation method being accurate in the tail. All five assumptions can break. Here are the specific ways they've broken in the past, and here's how we'd know if they're breaking now."

---

## Check-In

Eight failure modes. The thread running through all of them: **Monte Carlo looks more rigorous than it is.** The simulation creates an illusion of thoroughness that masks fundamental uncertainty about the model, the parameters, and the stability of the world.

Which of these failure modes feels most relevant to how VaR is used at Spreadex? The correlation breakdown (multi-asset dealer book)? The explainability gap (traders need to trust the number)? Something else?