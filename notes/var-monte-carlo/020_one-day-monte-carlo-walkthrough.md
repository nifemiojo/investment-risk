# 1-Day Monte Carlo VaR: Concrete Walkthrough

**Date:** 2026-07-10
**Topic:** Walking through two 1-day VaR calculations — calm day vs post-crash day — with both formula and simulation

---

## The Setup

We have a GARCH(1,1) model already estimated:

$$\hat{\sigma}_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \hat{\sigma}_{t-1}^2$$

$$\omega = 0.00001, \quad \alpha = 0.08, \quad \beta = 0.88, \quad \mu = 0$$

**Terms:**
- $\hat{\sigma}_t^2$: modeled conditional variance for day t
- $r_{t-1}$: yesterday's observed return
- $\hat{\sigma}_{t-1}^2$: yesterday's modeled variance
- $\omega, \alpha, \beta$: estimated GARCH parameters

Position: £1,000,000. We want 95% 1-day VaR.

---

## Day A: After a Calm Period

**Yesterday's data:**

$$r_{\text{yesterday}} = +0.3\% = 0.003$$
$$\hat{\sigma}_{\text{yesterday}}^2 = 0.00012 \quad (\hat{\sigma}_{\text{yesterday}} = 1.10\%)$$

### Step 1: Compute Today's σ

$$\hat{\sigma}_{\text{today}}^2 = 0.00001 + 0.08 \cdot (0.003)^2 + 0.88 \cdot 0.00012$$
$$= 0.00001 + 0.08 \cdot 0.000009 + 0.000106$$
$$= 0.00001 + 0.00000072 + 0.000106$$
$$= 0.000117$$

$$\hat{\sigma}_{\text{today}} = \sqrt{0.000117} = 1.08\%$$

Yesterday was quiet (+0.3%), so today's volatility is low: 1.08%.

### Step 2: The Formula (Parametric GARCH VaR)

$$\text{VaR}_{0.05} = 0 + 0.0108 \cdot (-1.6449) = -1.78\%$$

$$\text{£VaR} = £1{,}000{,}000 \cdot 0.0178 = £17{,}800$$

One formula, one number. Done.

### Step 3: Monte Carlo Simulation

We simulate 10,000 tomorrows, all starting from today's $\hat{\sigma}_{\text{today}} = 0.0108$:

```
Simulated return 1:   0.0108 × (+0.43) = +0.46%
Simulated return 2:   0.0108 × (-0.87) = -0.94%
Simulated return 3:   0.0108 × (+1.21) = +1.31%
Simulated return 4:   0.0108 × (-2.05) = -2.21%
Simulated return 5:   0.0108 × (-0.17) = -0.18%
...
Simulated return 9999:  0.0108 × (+0.55) = +0.59%
Simulated return 10000: 0.0108 × (-1.68) = -1.81%
```

Sort these 10,000 returns. The 500th worst (5th percentile) is approximately **−1.77%**.

$$£\text{VaR (Monte Carlo)} \approx £17{,}700$$

**Monte Carlo ≈ Formula.** The £100 difference is sampling noise. With more simulations, they'd converge to the same number: £17,800.

---

## Day B: After a Crash

**Yesterday's data (market just had a bad day):**

$$r_{\text{yesterday}} = -3.5\% = -0.035$$
$$\hat{\sigma}_{\text{yesterday}}^2 = 0.00015 \quad (\hat{\sigma}_{\text{yesterday}} = 1.22\%)$$

### Step 1: Compute Today's σ

$$\hat{\sigma}_{\text{today}}^2 = 0.00001 + 0.08 \cdot (-0.035)^2 + 0.88 \cdot 0.00015$$
$$= 0.00001 + 0.08 \cdot 0.001225 + 0.000132$$
$$= 0.00001 + 0.000098 + 0.000132$$
$$= 0.000240$$

$$\hat{\sigma}_{\text{today}} = \sqrt{0.000240} = 1.55\%$$

The crash ($-$3.5%) spikes today's volatility from 1.22% to 1.55%.

### Step 2: The Formula

$$\text{VaR}_{0.05} = 0 + 0.0155 \cdot (-1.6449) = -2.55\%$$

$$£\text{VaR} = £25{,}500$$

### Step 3: Monte Carlo Simulation

10,000 draws, all using $\hat{\sigma}_{\text{today}} = 0.0155$:

```
Simulated return 1:   0.0155 × (-0.33) = -0.51%
Simulated return 2:   0.0155 × (-1.89) = -2.93%
...
```

Sort. 500th worst ≈ **−2.54%**. £VaR ≈ £25,400.

**Again, Monte Carlo ≈ Formula.**

---

## What This Shows

### GARCH Changes the VaR — and That Matters

| | σ_today | 1-Day 95% VaR |
|---|---|---|
| **After calm day** | 1.08% | £17,800 |
| **After crash** | 1.55% | £25,500 |
| **Ignoring GARCH (full-sample σ̂ = 1.30%)** | 1.30% | £21,400 |

GARCH makes the VaR **conditional** — it's £17,800 after calm, £25,500 after a crash. The fixed-σ̂ parametric VaR says £21,400 regardless. That's the value: GARCH gives you **state-dependent risk**, not an average.

### But Monte Carlo Doesn't Add Anything for the 1-Day Calculation

For both days, the formula and the simulation give the same answer. 10,000 draws of $z \sim N(0,1)$ multiplied by a fixed $\sigma_{\text{today}}$ just converges to $\sigma_{\text{today}} \cdot z_{0.05}$. The simulation is doing unnecessary work.

### So What Is Monte Carlo For?

Monte Carlo is the mechanism for computing the quantile **when no formula exists.** For 1-day GARCH with normal shocks, a formula exists. For:

- **10-day GARCH:** no formula — you must simulate
- **GARCH with non-normal shocks where the quantile isn't known:** you must simulate
- **Multi-asset with copula:** no closed-form joint quantile — you must simulate
- **Portfolio with options:** P&L is nonlinear — you must simulate

The GARCH model provides the **time-varying volatility estimate.** Monte Carlo provides the **computation method for the quantile when you can't just plug into a formula.** They solve different problems. GARCH gives you $\sigma_{\text{today}}$. Monte Carlo handles the cases where translating $\sigma_{\text{today}}$ into VaR isn't a one-line formula.

---

## The Corrected Summary

| What | Role | Needed for 1-Day? | Needed for 10-Day? |
|---|---|---|---|
| **GARCH model** | Provides time-varying $\sigma_t$ | Yes — changes VaR based on recent events | Yes — plus it governs how σ evolves over the path |
| **Monte Carlo simulation** | Computes quantile when no formula exists | No — formula $\sigma_t \cdot z_\alpha$ works | Yes — no formula for 10-day GARCH distribution |

---

## Check-In

Does walking through both days with actual numbers clear this up? The key separation: **GARCH = the model for how volatility changes. Monte Carlo = the tool for computing quantiles when the model is too complex for a formula.** For 1-day normal-shock GARCH, the model is simple enough that you don't need the tool.