# Strengths of Historical VaR

**Date:** 2026-07-06
**Topic:** What historical VaR gets right — and why it survives despite its flaws

---

## The Core Strength in One Sentence

**Historical VaR makes no assumptions about the shape of the return distribution.**

That single property cascades into every advantage it has over parametric approaches.

---

## Strength 1: No Distribution Assumption (Non-Parametric)

Parametric VaR assumes returns are normally distributed. Real returns are not.

```
Normal assumption says:
  - 95% VaR = μ - 1.645σ
  - 99% VaR = μ - 2.326σ
  - A -5σ event happens once every 7,000 years

Real markets say:
  - A -5σ event happens every few years
  - Tails are fat — extreme events are much more common than normal predicts
  - Skew is real — crashes are bigger than rallies
```

Historical VaR doesn't care. If −7% days happen 3 times in your 252-day sample, the method sees them and puts them in the tail. It doesn't dismiss them as "impossible under the normal distribution."

---

## Strength 2: Fat Tails Are Automatically Captured

Every feature of the empirical distribution — fat tails, skew, kurtosis, multimodality — flows through to the VaR estimate. You don't have to model any of it.

**Concrete comparison:**

Imagine your 252-day sample includes the COVID crash. You have daily returns of −8%, −6%, −5%, and dozens of −3% to −4% days.

| Method | 95% VaR | 99% VaR |
|---|---|---|
| Parametric (normal, σ = 2%) | −3.3% | −4.7% |
| Historical (actual data) | −4.1% | −6.8% |

The parametric VaR says "your worst day in 100 is −4.7%." The actual data says your worst day in 100 is closer to −7%. Historical VaR sees the fat tails that the normal distribution refuses to acknowledge.

This gap — between what the normal distribution predicts and what actually happens — is why regulators increasingly prefer methods that don't assume normality.

---

## Strength 3: No Estimation Error on Parameters

Parametric VaR requires estimating $\mu$ (mean return) and $\sigma$ (standard deviation). Both estimates come with error — you're estimating two numbers from noisy data and then plugging them into a formula.

Historical VaR has zero parameters. Nothing to estimate. The "model" *is* the data.

This matters because estimation error compounds:
- Estimate $\sigma$ wrong → VaR wrong
- $\mu$ is notoriously hard to estimate precisely (signal-to-noise ratio of daily returns is terrible)
- Both estimates assume stationarity too, so you haven't escaped that problem

Historical VaR sidesteps all of this. The only "choice" is the window size — and that's transparent, not buried inside a parameter estimation step.

---

## Strength 4: Explainability

You can show a risk manager or a trader exactly where the VaR number came from:

> "Our 95% 1-day VaR is −4.1%. That means on the 13th worst day in the last year, we'd lose 4.1% or more. The worst day was −8.2% on March 16, 2020."

Every number has a date and a story attached to it. This is not true of parametric VaR, where the answer is "1.645 times an estimated standard deviation" — a number that emerged from a formula, not from history.

For a dealer operation like Spreadex, where traders need to trust the risk numbers they're hedging against, this explainability is not a nice-to-have. It's the difference between "I'll act on this" and "I'll ignore this."

---

## Strength 5: Implicit Correlation Capture (Multi-Asset)

When you calculate historical VaR on portfolio returns (not individual asset returns), all correlation effects are automatically embedded. You don't need to estimate a covariance matrix.

If stocks and bonds both crashed together on 3 days in your sample, those days are in the tail of portfolio returns. If they usually move in opposite directions, that diversification shows up too. No correlation matrix. No estimation error on 1,000+ pairwise correlations. The data speaks.

This is a big deal for multi-asset portfolios (which is what Spreadex has — equities, FX, futures, commodities, crypto). Estimating a full covariance matrix across all those asset classes is error-prone and fragile. Historical VaR on portfolio-level returns avoids the problem entirely.

---

## Strength 6: Easy to Backtest

Backtesting VaR means counting how often actual losses exceed the VaR estimate. A 95% VaR should be breached on roughly 5% of days.

With historical VaR, the backtest is straightforward: compare each day's actual return to that day's VaR estimate (calculated from the prior 252 days). Count the breaches. If the breach rate is far from 5%, something is wrong — either the window is wrong, the regime changed, or the method is failing.

No model diagnostics. No distribution tests. Just counting.

---

## Summary: When Historical VaR Wins

| Scenario | Historical VaR | Parametric VaR |
|---|---|---|
| Fat-tailed returns | ✅ Captures automatically | ❌ Underestimates tail risk |
| Skewed returns | ✅ Captured in data | ❌ Normal is symmetric |
| Multi-asset portfolio | ✅ Correlation in data, no matrix | ❌ Full covariance matrix needed |
| Explaining to non-technical audience | ✅ "13th worst day" | ❌ "1.645 sigma" |
| Small, weird samples | ✅ No assumptions to violate | ❌ Normal assumption can't hold |
| Stable, normal-ish returns | ⚠️ Works fine, not better | ✅ Works fine, simpler formula |
| Regime changes | ❌ Both fail | ❌ Both fail |

---

## The Honest Assessment

Historical VaR is not the most sophisticated method. It's not the most theoretically elegant. But it is:

- **Robust** — fewer ways to be wrong than parametric methods
- **Transparent** — every number traceable to an actual day
- **Non-parametric** — lets the data speak, fat tails and all
- **Simple** — easy to implement, backtest, and explain

For a first implementation, for a production risk dashboard, and for building intuition about what your portfolio's tail actually looks like — it's the right place to start.

---

## Ready to Code

You now have the full picture:
- 001: Core idea
- 002: Percentile conventions
- 002b: Indexing clarification
- 003: Convention choice + sample size
- 004: Why 252 days
- 005: Sample size trade-offs
- 006: Production mitigations
- 007: Strengths (this file)

The method, its assumptions, its failure modes, its mitigations, and its strengths — all on the table. Next step is implementation. Ready?
