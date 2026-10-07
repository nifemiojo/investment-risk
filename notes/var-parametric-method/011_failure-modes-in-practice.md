# Parametric VaR Failure Modes: What It Actually Looks Like in Practice

**Date:** 2026-07-07
**Topic:** Concrete failure narratives — what breaks, how, and the impact

---

## Why This Matters

Limitations are abstract. Failure modes are concrete. The difference:

> **Limitation:** "The normality assumption is wrong."
> **Failure mode:** "Your VaR said -1.2%. You lost -4.8%. Your hedge at -1.2% was 4x too small. The desk is down £2M and the CRO is standing at your desk."

Let's walk through the real ones.

---

## Failure Mode 1: The Calm-Before-Storm Trap

### What It Looks Like

```
Month 1-6:  Markets calm. Vol hovers at 12%.
            EWMA σ̂ drifts down to 11%.
            95% parametric VaR: -0.9%
            Position limits: "You can risk up to £1M per desk"
            Desk loads up. Life is good.

Month 7, Day 1:  Shock hits. Overnight gap down 4%.
                 Your VaR model, still using yesterday's σ̂, says: "95% VaR = -0.9%"
                 Reality: You just lost 4.4x your VaR.
                 
Month 7, Day 2:  EWMA σ̂ jumps to 28%.
                 VaR jumps to -2.3%.
                 Position limits: "You must reduce risk NOW."
                 Forced selling into a falling market.
```

### The Mechanism

Parametric VaR (even with EWMA) is **backward-looking**. It estimates volatility from what already happened. When a shock arrives, it takes 1–2 days for EWMA to catch up. By then, the loss has already happened.

### The Impact

- **Double hit:** You're overexposed when the shock hits (VaR was too low), then forced to deleverage when VaR spikes (VaR is now too high).
- **Procyclicality:** The model amplifies the cycle — expands risk in calm, contracts risk in stress.
- **At Spreadex:** Your autohedge using yesterday's σ̂ hedges at -0.9%, but the actual move is -4%. Hedge is 4x undersized.

---

## Failure Mode 2: The Correlation Collapse

### What It Looks Like

```
Pre-crisis model:
  Assets: 60% equity (σ₁ = 1.2%), 40% bonds (σ₂ = 0.4%)
  Correlation from past 252 days: ρ̂ = -0.15
  Portfolio σ = √(0.6²×1.2² + 0.4²×0.4² + 2×0.6×0.4×(-0.15)×1.2×0.4)
             = √(0.5184 + 0.0256 - 0.0173)
             = √0.5267 = 0.726%
  95% VaR = -1.195%

Crisis hits:
  Correlation jumps to ρ = +0.65 (both selling off)
  Portfolio σ = √(0.5184 + 0.0256 + 2×0.6×0.4×0.65×1.2×0.4)
             = √(0.5184 + 0.0256 + 0.1498)
             = √0.6938 = 0.833%
  True 95% VaR = -1.370%
  
  But wait — equity σ also spiked to 2.5%:
  Portfolio σ = √(0.6²×2.5² + 0.4²×0.8² + 2×0.6×0.4×0.65×2.5×0.8)
             = √(2.25 + 0.1024 + 0.624) = √2.976 = 1.725%
  True VaR = -2.838%
  
  Your model still says: -1.195%
  Reality: -2.838%
  You're under-hedged by 2.4x.
```

### The Mechanism

The portfolio variance formula has three terms: equity variance, bond variance, and the covariance term. In a crisis, **all three blow up simultaneously** — equity vol spikes, bond vol spikes, and the correlation flips from negative to positive. The model, using pre-crisis estimates, sees none of this.

### The Real-World Example: March 2020

```
Model (based on Jan 2020 data):
  60/40 portfolio VaR: -1.2%

March 16, 2020 reality:
  S&P 500: -12.0%
  Long bonds: -3.2%  (yes, bonds went DOWN with stocks)
  Portfolio: -8.5%
  
  VaR breach: 7.1x the predicted threshold
```

### The Impact

- Diversification benefit was the **foundation** of the risk model. When it disappeared, every number downstream was wrong.
- Risk limits that relied on "diversified portfolio VaR" were suddenly too wide by 2–3x.

---

## Failure Mode 3: The Window Cliff

### What It Looks Like

```
Day 252 in your window:  October 2022, a -4.1% day (biggest in the sample)
Day 253 (new day):       A calm +0.3% day

Morning of Day 253:
  Window is now days 2–253. The -4.1% day just dropped out.
  σ̂ drops from 1.4% to 1.15%.
  VaR drops from -2.30% to -1.89%.
  
  Risk dashboard: "VaR decreased 18% — risk environment improving!"
  Reality: Nothing changed. A bad day aged out of the window.
```

### The Reverse Cliff

```
You're in a crisis. 252 days ago was a calm period.
Each day, a calm day drops out and a crisis day enters.
σ̂ climbs relentlessly. VaR widens.
  
  Every morning, the risk limit tightens.
  You're forced to reduce positions.
  Every afternoon, more selling.
  The model itself is driving the deleveraging cascade.
```

### The Mechanism

Equal-weighted windows create artificial discontinuities. A single observation entering or leaving can shift VaR by 15–20%. The model signals a change in risk when the underlying risk hasn't changed — only the window has.

### The Impact

- **False signals:** "Risk is decreasing" when it's just a data artifact.
- **Procyclical pressure:** The window effect amplifies the boom-bust cycle. VaR shrinks as crisis days age out → risk limits widen → more risk taken → next crisis is worse.

---

## Failure Mode 4: Silent Model Drift

### What It Looks Like

```
Quarter 1:  Breaches: 12 out of 63 days = 19.0%  (expected: 5%)
Quarter 2:  Breaches: 8 out of 64 days = 12.5%   (expected: 5%)
Quarter 3:  Breaches: 6 out of 64 days = 9.4%    (expected: 5%)

Nobody is tracking this. The VaR number is reported daily.
Risk committee looks at the number, nods, moves on.

By the time someone notices, the model has been understating risk 
by 2–4x for nine months. The desk has been running with 
effectively no risk control.
```

### The Mechanism

Parametric VaR produces a number every day. The number looks authoritative. But if nobody backtests — comparing predicted breaches to actual breaches — the model can be catastrophically wrong for months without detection.

### The Kupiec Test (What They Should Have Been Running)

The standard backtest: count breaches and test whether the observed breach rate matches the expected rate.

Under the null hypothesis (model is correct), the number of breaches follows a binomial distribution:

$$P(\text{breaches} = k) = \binom{n}{k} \cdot \alpha^k \cdot (1-\alpha)^{n-k}$$

**Terms:**
- $n$: number of days in the backtest period
- $k$: number of observed breaches
- $\alpha$: expected breach rate (e.g., 0.05 for 95% VaR)

For $n = 252$ and $\alpha = 0.05$, you expect about 12.6 breaches. If you see 20+, the model is probably broken. If you see 30+, it's definitely broken.

The **traffic light system** from Basel:
- 🟢 Green: 0–4 breaches in 250 days (model OK)
- 🟡 Yellow: 5–9 breaches (monitor closely)
- 🔴 Red: 10+ breaches (model broken, recalibrate)

### The Impact

- The model was wrong for months. Every decision made using it — position limits, hedging, capital allocation — was based on bad numbers.
- The cleanup: unwind oversized positions, explain to the regulator, rebuild trust with the desk.

---

## Failure Mode 5: The Mean Misdirection

### What It Looks Like

```
Portfolio: heavy tech exposure, rode the 2023 rally
μ̂ (from past 252 days): +0.12% daily  (massive bull run)

95% parametric VaR = μ̂ - 1.645×σ̂ = 0.12% - 1.645×1.5% = 0.12% - 2.47%
                   = -2.35%

But if we set μ̂ = 0:
  VaR = 0 - 2.47% = -2.47%

The positive mean is hiding 0.12% of risk. Over 252 days, 
the cumulative effect is meaningful but the daily effect seems tiny.
```

### Worse: When the Mean Is Wrong

```
μ̂ = +0.12% but the true μ turns negative next quarter:
  True VaR should be: -0.05% - 2.47% = -2.52%
  Your VaR says: -2.35%
  
  You think you're hedged for -2.35%.
  You're actually facing -2.52%.
  The difference compounds over time.
```

### The Mechanism

The mean is estimated with huge error — its standard error is $\sigma/\sqrt{n} \approx 0.08\%$ for typical equity data. The estimate can be positive when the true mean is negative, or vice versa.

Including $\hat{\mu}$ adds noise without adding much signal for short horizons.

### The Impact

- For 1-day VaR: small error. The vol term dominates.
- For 10-day VaR: the mean term is 10× larger. The error matters.
- For regulatory capital (10-day 99% VaR): using a noisy $\hat{\mu}$ can meaningfully understate risk.

---

## Failure Mode 6: Procyclical Amplification

### The Full Cycle

```
PHASE 1: CALM
  Vol low → VaR low → Risk limits wide → More risk taken
  More risk → More leverage → System more fragile
  
PHASE 2: SHOCK
  Vol spikes → VaR spikes → Risk limits narrow → Forced selling
  Forced selling → Prices fall further → Vol spikes higher → VaR widens more
  ┌─────────────────────────────────────────┐
  │         THE POSITIVE FEEDBACK LOOP      │
  │  VaR ↑ → Sell → Price ↓ → Vol ↑ → VaR ↑│
  └─────────────────────────────────────────┘

PHASE 3: AFTERMATH
  Vol eventually falls → VaR falls → Limits expand → Cycle begins again
```

### The Mechanism

Parametric VaR is **procyclical by design**. It measures recent volatility. When markets are calm, it says risk is low (so you take more risk). When markets are stressed, it says risk is high (so you sell). This is exactly backwards from what a stabilizing risk system would do.

### Real Example: August 2007 "Quant Quake"

```
Pre-crisis: Hedge funds running statistical arbitrage
            Vol low, VaR low, leverage high (6-8x)

August 7-10, 2007:
  One fund liquidates → prices move → VaR spikes at other funds
  → Other funds get margin calls → forced to sell
  → More price moves → VaR spikes further
  → Cascade of forced deleveraging
  → Models that were uncorrelated all sold the same things
  
Result: Quant funds lost 5-30% in 3 days.
        All driven by the same VaR-based risk limits triggering simultaneously.
```

### The Impact

- The risk model that was supposed to protect against losses **caused** them.
- Systemic risk: when everyone uses similar VaR models, they all get the same signal to sell at the same time.
- This is why regulators now require **stressed VaR** (SVaR) — VaR calibrated to a period of stress — alongside regular VaR, to provide a counter-cyclical anchor.

---

## Failure Mode 7: The Precision Illusion

### What It Looks Like

```
Risk report:  "95% 1-Day Parametric VaR: -1.29741%"
                                   ^^^^^^^^
                                   Six decimal places!
                                   Looks incredibly precise.

Reality:
  Change the window from 252 to 504 days:  VaR changes by 0.15%
  Change λ from 0.94 to 0.97 in EWMA:     VaR changes by 0.22%  
  Use Student's t instead of normal:       VaR changes by 0.40%
  Use Cornish-Fisher adjustment:           VaR changes by 0.35%
  
The number should be reported as: "VaR ≈ -1.3% (±0.4%)"
But it's reported as: -1.29741%
```

### The Mechanism

The math is deterministic — given inputs, the output is exact to machine precision. This creates the illusion of precision. But every input is an estimate with uncertainty, and every modeling choice is debatable. The output precision is fake.

### The Impact

- Decision-makers treat the number as exact. "We're within limits" or "We're over limits" based on a number with ±30% uncertainty.
- Model risk is invisible. Nobody sees the alternative VaR that would have been produced with different (equally defensible) assumptions.

---

## Summary: The Failure Mode Map

| Failure Mode | Root Cause | Early Warning Sign | Typical Impact |
|---|---|---|---|
| Calm-before-storm | Backward-looking vol | VaR shrinking during calm | 3-5x underestimation at shock |
| Correlation collapse | Diversification disappears | Correlation matrix unstable | 2-3x underestimation |
| Window cliff | Hard cutoff in rolling window | VaR jumping on calm days | False signals, procyclicality |
| Silent drift | No backtesting | Breach rate drifting from 5% | Months of undetected error |
| Mean misdirection | Noisy μ̂ estimate | μ̂ bouncing between + and - | Hides 5-15bp of daily risk |
| Procyclical amplification | VaR-based limits | Position swings with VIX | Systemic selling cascades |
| Precision illusion | Deterministic math | Too many decimal places | Overconfidence in bad numbers |

---

## The Practitioner's Posture

The practitioners who survive these failure modes share a stance:

1. **Don't trust the number.** It's an estimate with wide error bars.
2. **Watch the inputs, not the output.** Is σ̂ behaving? Is the correlation matrix stable? Are breaches at expected frequency?
3. **Triangulate.** Run multiple VaR models (normal, t, Cornish-Fisher, EWMA, GARCH). If they agree, great. If they diverge, something's wrong — investigate.
4. **Backtest religiously.** The Kupiec test takes 5 lines of code. Run it weekly.
5. **Stress test separately.** Parametric VaR answers "normal days." Use scenarios for "bad days."

---

## Check-In

Which of these failure modes is most likely to bite at Spreadex — a dealer with multi-asset exposure, autohedging, and daily position limits — and why?
