# 017 — Can Correlation Signals Build More Reactive VaR Systems?

**Date:** 2026-07-22
**Topic:** Using correlation as a leading indicator to improve VaR responsiveness and breach consistency

---

## The problem we're solving

You've established that correlation shifts *lead* VaR shifts. The 252-day rolling VaR takes months to absorb a new correlation regime. During that lag:

- VaR is understated (portfolio risk is higher than reported)
- Breaches spike above the expected rate
- The risk system is reporting yesterday's risk for today's portfolio

The question: can we use the correlation signal to make VaR more reactive — producing a number that reflects the *current* correlation regime rather than a stale blend of old and new?

---

## Why this is hard for historical VaR specifically

With parametric VaR, you'd just update the correlation matrix. The formula is explicit:

$$\sigma_p = \sqrt{w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\rho\sigma_1\sigma_2}$$

Plug in today's ρ instead of the trailing 252-day ρ, recompute, done.

Historical VaR doesn't have this knob. The correlation is baked into the portfolio return series — you can't "update ρ" without changing the returns themselves. So we need approaches that work *around* this constraint.

---

## Approach A: Correlation-triggered window switching

**The idea:** When correlation is stable (ratio ≈ 1), use the standard 252-day window. When correlation is shifting (ratio diverges), switch to a shorter window.

**Mechanism:**

```
if |correlation_ratio - 1| > threshold:
    var_window = 60   # fast adaptation
else:
    var_window = 252  # stable estimate
```

**Why it could work:** The 60-day window adapts to correlation shifts in ~30 days instead of ~126 days. It directly addresses the lag.

**Why it might not:** The 60-day window is noisier during calm periods. When you switch, VaR can jump discontinuously — a 60-day VaR and a 252-day VaR can differ by 20-30% even in stable regimes. That jump may be hard to explain to traders or risk committees ("VaR didn't change because risk changed — it changed because we changed the window").

**The trade-off:**

| | 252-day window | 60-day window | Switched |
|---|---------------|---------------|----------|
| Calm period accuracy | Good (stable) | Noisy (overreacts) | Good (stays at 252) |
| Crisis responsiveness | Poor (slow) | Good (fast) | Good (switches to 60) |
| VaR continuity | Smooth | Smooth | **Jumpy at switch points** |
| Explainability | Simple | Simple | **"Why did VaR jump?"** |

---

## Approach B: Correlation-adjusted VaR blend

**The idea:** Don't switch windows. Instead, blend the portfolio VaR toward the naive sum in proportion to how much the correlation has shifted.

**Mechanism:**

$$\text{VaR}_{\text{adjusted}} = \alpha \times \text{VaR}_{\text{portfolio}} + (1 - \alpha) \times \text{VaR}_{\text{naive}}$$

Where α is a function of the correlation ratio:

$$\alpha = \max\left(0, \; 1 - \beta \times |\text{ratio} - 1|\right)$$

- When ratio ≈ 1 (stable correlation): α ≈ 1 → VaR_adjusted ≈ portfolio VaR (no adjustment)
- When ratio ≫ 1 (correlation rising fast): α → 0 → VaR_adjusted → naive sum (full stress)
- β controls how aggressively you adjust (β = 1 means ratio = 2 pushes α to 0)

**Why this is elegant:** It's continuous — no jumps. The adjustment scales smoothly with the signal strength. And it has a clear interpretation: "We compute VaR normally, then add a correlation stress adjustment that grows as the correlation regime shifts."

**Why it needs care:** It introduces a new parameter β. And at α = 0, you're reporting the naive sum — which may be too conservative in many regimes. The naive sum is a worst case, not a central estimate.

**The trade-off:**

| | Portfolio VaR only | Correlation-adjusted |
|---|-------------------|---------------------|
| Calm period | VaR = reliable | VaR ≈ same (α ≈ 1) |
| Correlation rising | VaR understated | VaR rises smoothly toward naive sum |
| Breach consistency | Spikes during shifts | More consistent |
| Parameter burden | None | One new parameter (β) |
| Conservatism | Low | Higher — edges toward naive sum |

---

## Approach C: Decay-weighted VaR + correlation monitoring (the lightweight option)

**The idea:** You've already built decay-weighted VaR (λ = 0.94). It gives more weight to recent returns — which implicitly gives more weight to the recent correlation regime. Pair it with the correlation ratio as a *monitoring signal* rather than an *adjustment mechanism*.

**Mechanism:**

1. Compute decay-weighted portfolio VaR (already done — use `decay_var` or `rolling_decay_var`)
2. Compute the correlation ratio as a separate monitoring metric
3. When the ratio diverges, the decay VaR will adapt faster than equal-weighted VaR — but it still lags
4. The ratio tells you *how much to discount the VaR number* rather than *what number to use instead*

**Practical workflow:**

| Correlation ratio | Decay VaR | Interpretation | Action |
|-------------------|-----------|----------------|--------|
| ≈ 1 | Trust it | Correlation stable | Standard monitoring |
| 1.5 - 2.0 | Partially trust | Correlation shifting | Flag to traders; consider naive sum as supplementary |
| > 2.0 or < 0 | Don't trust | Regime change | Use naive sum for position limits until ratio stabilises |

**Why this is practical:** No new code. No new parameters. No jumps. Just pairing two existing numbers — decay VaR + correlation ratio — and letting the risk manager apply judgment.

**The trade-off:** It puts the burden on the human to interpret. Not fully automated. But for a risk manager who's already checking multiple signals (multi-window VaR, breach rates, diversification benefit), adding one more signal is natural — it's more information, not a system change.

---

## Which approach fits your context?

### Spreadex (live trading risk)

You need a number that's reactive enough to protect the book but stable enough that traders don't ignore it. Approach C (decay VaR + correlation monitoring) is probably the right starting point — it uses infrastructure you've already built, and the human-in-the-loop judgment is appropriate for a trading desk where the risk manager is actively monitoring.

The correlation ratio becomes: "Should I override the system VaR with a stress number?" A simple rule: ratio > 2 → show naive sum alongside VaR in the dashboard.

### FINBOURNE / institutional (reported VaR to committees)

You can't change the VaR methodology mid-quarter without explaining it. Approach B (correlation-adjusted blend) gives you a framework to say: "Our core VaR methodology is historical simulation. We apply a correlation stress adjustment when the trailing correlation diverges significantly from long-run averages. This adjustment is transparent, rule-based, and documented."

Institutional investors value explainability over pure reactivity. A rule-based adjustment with one parameter (β) is defensible.

### Your own toolkit development

Build all three approaches as experiments and compare them. The question is empirical: which approach produces breach rates closest to the expected rate across different correlation regimes? That's a backtest — and it's exactly the kind of analysis that demonstrates you understand not just how to compute VaR, but how to make it *useful*.

---

## The deeper principle

The single most valuable pattern across everything you've built:

> **Track the disagreement between methods, not just the methods themselves.**

- Multi-window VaR: the divergence between 252d and 60d is the signal
- Diversification benefit: the gap between portfolio VaR and naive sum is the signal
- Correlation ratio: the divergence between fast and slow estimates is the signal
- Decay vs equal-weighted: the gap between them tells you how much the recent regime differs

Every reactive system built on this principle follows the same structure: **stable baseline + fast detector + blend rule.** The stable baseline gives you continuity. The fast detector tells you when the baseline is stale. The blend rule tells you how much to adjust.

---

## Concrete next step: a correlation-adjusted VaR experiment

The simplest experiment to validate this idea:

1. Compute rolling 252-day portfolio VaR (the baseline)
2. Compute rolling correlation ratio (the detector)
3. Compute the naive sum (the stress ceiling)
4. Define a simple blend: when ratio > 1.5, VaR_adjusted = 0.5 × VaR_portfolio + 0.5 × naive_sum
5. Backtest: compare breach rates of VaR_adjusted vs VaR_portfolio across different correlation regimes

If the adjusted VaR produces breach rates closer to 5% during correlation shift periods without being too conservative during calm periods, the approach has merit.

This could be Notebook 14.5 or 15 — a natural bridge between the dashboard (Notebook 14) and the n-asset generalisation.

---

## Check-in

1. Does the "stable baseline + fast detector + blend rule" framework make the approaches feel like variations on a single idea rather than three unrelated options?
2. Which approach feels most natural for your Spreadex context — the human-in-the-loop monitoring (C) or the automated blend (B)?
3. Want to build the correlation-adjusted VaR experiment as the next notebook?
