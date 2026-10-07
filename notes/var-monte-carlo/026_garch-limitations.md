# GARCH: Limitations and Failure Modes

**Date:** 2026-07-10
**Topic:** What GARCH gets wrong, when it breaks, and how those breaks flow through to VaR estimates

---

## The Core GARCH Model (For Reference)

$$r_t = \mu + \sigma_t \cdot \epsilon_t, \quad \epsilon_t \sim D(0,1)$$

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \sigma_{t-1}^2$$

**Terms:**
- $\omega$: baseline variance (the floor)
- $\alpha$: reaction to new shocks (the "news" coefficient)
- $\beta$: persistence of past volatility (the "memory" coefficient)
- $\alpha + \beta$: total persistence — must be < 1 for stationarity

---

## Limitation 1: Symmetric Response to Shocks

### The Problem

Standard GARCH treats $r_{t-1}^2$ — a +5% day and a −5% day have identical effects on tomorrow's variance. But empirically, negative returns increase volatility **more** than positive returns of the same magnitude (the leverage effect).

### Why It Matters for VaR

After a rally, GARCH overestimates tomorrow's volatility. After a crash, GARCH underestimates it relative to reality. Your VaR is too conservative after good days and too optimistic after bad days.

### Quantified

For equity indices, the asymmetry is roughly: a −1% shock increases next-day variance 1.5× to 2× as much as a +1% shock. Standard GARCH misses this entirely.

### The Fix

GJR-GARCH adds a leverage term:

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \gamma \cdot r_{t-1}^2 \cdot I_{t-1} + \beta \cdot \sigma_{t-1}^2$$

where $I_{t-1} = 1$ if $r_{t-1} < 0$. The γ parameter captures the extra effect of negative returns.

---

## Limitation 2: Parameter Estimation Uncertainty

### The Problem

ω, α, and β are estimated from data via Maximum Likelihood Estimation (MLE). These estimates have standard errors. The problem is asymmetric:

- **β is estimated relatively precisely:** it governs persistence, and persistence shows up in many observations
- **α is estimated imprecisely:** it governs reaction to new shocks, and large shocks are rare by definition
- **ω is extremely imprecise:** it's very small and buried in the noise

### Why It Matters for VaR

$$\text{Long-run variance} = \frac{\omega}{1 - \alpha - \beta}$$

Small errors in $\alpha$ or $\beta$ create large errors in the long-run variance, because you're dividing by $(1 - \alpha - \beta)$, which is typically 0.02–0.10.

If $\alpha + \beta$ is estimated at 0.96 but the true value is 0.94:

$$\text{Estimated long-run } \sigma^2 = \frac{\omega}{0.04}$$
$$\text{True long-run } \sigma^2 = \frac{\omega}{0.06}$$

The true long-run variance is 33% **lower** than estimated. Your 10-day Monte Carlo VaR, which reverts toward the long-run variance, will be systematically too high.

### The Fix

- Report confidence intervals for all parameters
- Bootstrap the estimation to understand parameter uncertainty
- Use Bayesian methods that incorporate parameter uncertainty into the VaR distribution

---

## Limitation 3: The Stationarity Assumption

### The Problem

GARCH requires $\alpha + \beta < 1$ for the variance process to be stationary — it must revert to a long-run mean.

But in practice, $\alpha + \beta$ is often very close to 1 (0.97–0.995). This is called "near-integrated GARCH" or IGARCH. It means:

- Shocks to volatility decay **very** slowly
- The model is borderline non-stationary
- Small estimation errors can push $\alpha + \beta \geq 1$, which breaks the model mathematically

When $\alpha + \beta = 1$, the unconditional variance is infinite — the model says volatility has no long-run mean to revert to. This is almost certainly wrong, but it's what the data often suggests.

### Why It Matters for VaR

If you enforce stationarity ($\alpha + \beta < 1$), you may be forcing the model to forget volatility shocks faster than reality. Your 10-day VaR reverts to the long-run mean too quickly — it underestimates the persistence of crisis-level volatility.

If you don't enforce it, the model can produce explosive volatility paths in simulation — VaR numbers that grow without bound over the horizon.

### The Fix

- Component GARCH: splits volatility into a long-run component (slow-moving) and a short-run component (fast-moving)
- FIGARCH: fractionally integrated GARCH, allows for very slow decay without the mathematical problems of $\alpha + \beta = 1$

---

## Limitation 4: Single-Regime Assumption

### The Problem

Standard GARCH has ONE set of parameters for all market conditions. But markets have distinct regimes:

- **Calm:** low ω, moderate α, high β
- **Crisis:** high ω, high α, moderate β

GARCH averages across these regimes. The fitted parameters describe a market that doesn't exist — a blend of calm and crisis dynamics.

### Why It Matters for VaR

After a calm period, GARCH says "vol will stay low" (high β). After a crisis, GARCH says "vol will decay" (still the same β). But in reality:

- During calm, vol does stay low (this part GARCH gets right)
- During crisis, vol stays high longer than GARCH predicts (because crisis β is different from calm β)
- During the transition FROM calm TO crisis, GARCH is slow to react because it's still weighted toward the calm-regime β

The model is simultaneously too optimistic in crises and too slow to detect crisis onset.

### The Fix

- Markov-switching GARCH: two (or more) sets of GARCH parameters, with probabilities of switching between regimes
- This is the model that directly addresses your oil shock example

---

## Limitation 5: The Distribution of Shocks

### The Problem

Standard GARCH assumes $\epsilon_t \sim N(0,1)$. Even after accounting for time-varying volatility (via GARCH), the standardized residuals $\hat{\epsilon}_t = r_t / \hat{\sigma}_t$ typically have:

- **Kurtosis > 3:** fatter tails than normal — extreme returns happen more often
- **Negative skew:** crashes are more extreme than rallies

Using normal shocks when the residuals are fat-tailed means your VaR is too low. The model thinks a 4σ event happens once every 43 years. With fat-tailed residuals, it might happen every 2–3 years.

### Why It Matters for VaR

| Shock Distribution | 5th Percentile | 1st Percentile | VaR vs Normal |
|---|---|---|---|
| Normal | −1.645 | −2.326 | — |
| Student's t (ν=5) | −2.015 | −3.365 | 22% wider at 95%, 45% wider at 99% |
| Student's t (ν=3) | −2.353 | −4.541 | 43% wider at 95%, 95% wider at 99% |

The tail divergence grows with confidence level. At 99% VaR, using normal shocks when the data is t(3) underestimates VaR by nearly 100%.

### The Fix

- Use Student's t or skewed-t for the shock distribution
- Test the standardized residuals: if kurtosis > 3.5, normal is wrong
- Let the data choose: estimate ν as an additional parameter alongside ω, α, β

---

## Limitation 6: No Long Memory

### The Problem

GARCH(1,1) captures volatility persistence with a geometric decay at rate β. The half-life of a shock is $\ln(0.5)/\ln(\beta)$ — about 4–14 days for typical β values.

But empirical volatility shows **long memory:** a volatility shock from 6 months ago still has measurable effects today. GARCH(1,1) can't capture this — after 30 days, the shock has decayed to near zero.

### Why It Matters for VaR

After a prolonged volatile period (like the 2008 financial crisis or COVID), GARCH says "vol is back to normal" within weeks. Reality says "vol stays elevated for months." Your VaR normalizes too quickly after a crisis.

### The Fix

- FIGARCH (Fractionally Integrated GARCH): models very slow hyperbolic decay instead of fast geometric decay
- Component GARCH: adds a slow-moving long-run volatility component
- HAR models: model volatility at multiple horizons (daily, weekly, monthly) simultaneously

---

## Limitation 7: Structural Breaks

### The Problem

GARCH assumes the parameters (ω, α, β) are stable over the estimation window. But financial markets experience structural breaks:

- New regulations change market dynamics
- New participants change trading behavior
- Technology changes execution and information flow
- Monetary regime changes alter the volatility environment

A GARCH model calibrated on 2010–2019 data (low vol, QE era) breaks in 2022 (high vol, rate hiking cycle). The parameters that described the old regime are wrong for the new one.

### Why It Matters for VaR

If the estimation window spans a structural break, the parameters are a meaningless average of two different worlds. The model fits neither regime well.

If the estimation window is entirely pre-break and the forecast period is post-break, the model is simply wrong — it's forecasting from a world that no longer exists.

### The Fix

- **Shorter estimation windows** (but this increases parameter uncertainty — the classic bias-variance trade-off)
- **Rolling estimation:** re-estimate parameters monthly, track how they evolve
- **Structural break tests:** formally test whether parameters changed at known break points
- **Regime-switching models** that can adapt to new regimes without manual intervention

---

## Limitation 8: Omitted Risk Factors

### The Problem

GARCH models volatility as a function of only past returns and past volatility:

$$\sigma_t^2 = f(r_{t-1}^2, \sigma_{t-1}^2)$$

But volatility depends on other things too:

- **Macro announcements:** FOMC, NFP, CPI releases spike intraday vol
- **Liquidity conditions:** low liquidity → higher vol
- **Cross-asset spillovers:** VIX affects equity vol, which affects FX vol
- **Flows and positioning:** crowded trades unwind violently

GARCH sees the spike after it happens but has no way to anticipate it.

### Why It Matters for VaR

On FOMC day, actual volatility will be higher than GARCH predicts because GARCH doesn't know it's FOMC day. Your VaR is too low when you need it most.

### The Fix

- **GARCH-X:** add exogenous variables to the variance equation (e.g., a dummy for FOMC days)
- **Realized GARCH:** use intraday data (realized volatility) as an additional input
- **Hybrid approaches:** GARCH for the baseline, stress add-ons for known event risk

---

## Limitation 9: The ω Identification Problem

### The Problem

ω, α, and β are jointly estimated. There's a near-identification problem: many different combinations of (ω, α, β) produce similar in-sample fits.

For example, these two parameter sets can produce nearly identical conditional variance series:

- Set A: ω = 0.00002, α = 0.08, β = 0.88 (α+β = 0.96, long-run σ² = 0.0005)
- Set B: ω = 0.00001, α = 0.06, β = 0.90 (α+β = 0.96, long-run σ² = 0.00025)

Same α+β, very different long-run variance. The data often can't distinguish them.

### Why It Matters for VaR

The long-run variance determines where 10-day Monte Carlo paths converge. If you're off by a factor of 2 on the long-run variance, your 10-day VaR is systematically wrong — not by a little, but by √2 ≈ 41% even under normality.

### The Fix

- **Use long spans of data** to pin down ω (the long-run mean is better estimated with more data)
- **Bayesian priors** to regularize ω toward economically plausible values
- **Target the long-run variance:** set ω = (1−α−β) × sample variance, then only estimate α and β

---

## Limitation 10: One Size Fits All Assets

### The Problem

The same GARCH(1,1) specification is applied to equities, FX, commodities, bonds — but these assets have fundamentally different volatility dynamics:

- **Equities:** strong leverage effect (γ large in GJR-GARCH), volatility spikes on downside
- **FX:** more symmetric, volatility clusters around event risk
- **Commodities:** supply-shock driven, volatility can spike in both directions
- **Bonds:** volatility linked to macro cycles, term structure effects

A GARCH(1,1) with normal shocks is a poor model for equities (misses leverage effect) but might be adequate for FX.

### Why It Matters for Multi-Asset VaR

If you use the same GARCH specification for all assets in a Monte Carlo simulation, some assets will be well-modeled and others won't. The aggregation into portfolio VaR hides this — you can't see which asset's bad model is driving the overall error.

### The Fix

- **Asset-specific GARCH specifications:** GJR-GARCH for equities, standard GARCH for FX, etc.
- **Test specification choice:** does a more complex model improve out-of-sample VaR accuracy for this specific asset?

---

## Summary Table

| Limitation | Root Cause | VaR Impact | Primary Fix |
|---|---|---|---|
| Symmetric shocks | r² ignores sign | Overestimates after rallies, underestimates after crashes | GJR-GARCH |
| Parameter uncertainty | α, ω estimated imprecisely | Long-run variance off by 30%+ | Bootstrap, Bayesian methods |
| Stationarity | α+β forced < 1 when data says ≈ 1 | Crisis vol decays too fast in simulation | Component GARCH, FIGARCH |
| Single regime | One parameter set for all markets | Slow to detect crises, too optimistic in them | Markov-switching GARCH |
| Normal shocks | Residuals are fat-tailed | VaR 45–100% too low at 99% confidence | Student's t, skewed-t |
| No long memory | Geometric decay at rate β | Vol normalizes too fast after prolonged stress | FIGARCH, HAR |
| Structural breaks | Parameters assumed stable | Model describes a world that no longer exists | Rolling estimation, regime-switching |
| Omitted factors | Only past returns and vol as inputs | Doesn't anticipate event-driven vol spikes | GARCH-X, realized GARCH |
| ω identification | Many (ω,α,β) combos fit equally well | Long-run variance indeterminate | Target long-run variance |
| One size fits all | Same spec for all assets | Some assets well-modeled, others not | Asset-specific specifications |

---

## The Interaction With Monte Carlo

GARCH's limitations compound with Monte Carlo's limitations:

- **Parameter uncertainty** (GARCH) → amplified through 10,000 paths (Monte Carlo)
- **Wrong shock distribution** (GARCH) → thousands of draws from the wrong distribution (Monte Carlo)
- **Single-regime assumption** (GARCH) → all paths simulate from the same (wrong) world (Monte Carlo)
- **Structural breaks** (GARCH) → the simulation knows nothing about the new regime (Monte Carlo)

The combination is dangerous because the simulation's apparent comprehensiveness masks the fundamental fragility of the underlying model.

---

## Check-In

Ten GARCH limitations. The most practically important for a dealer like Spreadex are probably: **symmetric shocks** (equities have strong leverage effects), **single regime** (markets switch between calm and turbulent), and **normal shocks** (fat tails are real and VaR-critical at high confidence levels).

Which of these limitations would you expect to matter most for Spreadex's risk exposures?