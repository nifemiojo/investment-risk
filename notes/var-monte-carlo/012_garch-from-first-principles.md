# GARCH From First Principles

**Date:** 2026-07-10
**Topic:** What GARCH is, why it exists, and how it captures volatility clustering

---

## The Problem GARCH Solves

You already know this problem. You described it yourself with the oil shock example:

> "The whole period has elevated vol, the volatility is not evenly distributed across the sample"

Here's what that looks like with real numbers. Suppose daily returns over 20 days:

```
Day  1: +0.3%    Day  6: -2.8%    Day 11: -3.1%    Day 16: -0.5%
Day  2: -0.5%    Day  7: +2.1%    Day 12: -2.9%    Day 17: +1.6%
Day  3: +0.1%    Day  8: -3.4%    Day 13: +3.3%    Day 18: -2.7%
Day  4: -0.2%    Day  9: -0.9%    Day 14: -3.8%    Day 19: +0.7%
Day  5: +0.6%    Day 10: +1.2%    Day 15: +2.5%    Day 20: -3.5%
```

Visually: calm for 5 days, then wild swings. If you compute the standard deviation over all 20 days, you get one number — say 2.1%. But that 2.1% is too high for days 1–5 (they're clearly calmer) and too low for days 11–14 (they're clearly more volatile).

The parametric approach says: "Volatility is σ̂ = 2.1%, and it's the same every day."

GARCH says: "Volatility *changes*. It was low on days 1–5, then spiked on day 6, stayed elevated, and might spike again. Let me model how it evolves."

---

## Step 1: The Simplest Volatility Model — ARCH(1)

ARCH = **A**uto**R**egressive **C**onditional **H**eteroskedasticity. Let's break that down:

- **Heteroskedasticity:** variance is not constant (hetero = different, skedastic = variance)
- **Conditional:** today's variance depends on past information
- **AutoRegressive:** it regresses on its own past values (specifically, past shocks)

The ARCH(1) model:

$$r_t = \mu + \epsilon_t, \quad \epsilon_t = \sigma_t \cdot z_t, \quad z_t \sim N(0,1)$$

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2$$

**Terms:**
- $r_t$: return on day t
- $\mu$: average return (usually small, often set to 0 for short horizons)
- $\epsilon_t$: the unexpected part of the return (the "shock")
- $\sigma_t^2$: the variance *today* (conditional on yesterday's information)
- $z_t$: a standard normal random variable — the "pure randomness"
- $\omega$: baseline variance — the minimum variance when there's no shock
- $\alpha$: how much yesterday's squared return feeds into today's variance
- $r_{t-1}^2$: yesterday's squared return

---

## Step 2: What ARCH(1) Does — A Concrete Walkthrough

Let me set $\omega = 0.0001$ (so baseline daily vol ≈ 1%), $\alpha = 0.3$, $\mu = 0$.

**Day 1:** No yesterday yet. Start with $\sigma_1^2 = \omega = 0.0001$. So $\sigma_1 = 1.0\%$.

Draw $z_1 \sim N(0,1)$. Say $z_1 = +0.5$. Then:
$$r_1 = 0 + 0.01 \cdot 0.5 = +0.005\%$$
$$\sigma_2^2 = 0.0001 + 0.3 \cdot (0.005)^2 = 0.0001 + 0.3 \cdot 0.000025 = 0.0001075$$
$$\sigma_2 \approx 1.04\%$$

Volatility barely changed. A +0.5% day is normal.

**Day 2:** $\sigma_2 = 1.04\%$. Draw $z_2 = -2.8$. Big negative shock.
$$r_2 = 0 + 0.0104 \cdot (-2.8) = -2.91\%$$
$$\sigma_3^2 = 0.0001 + 0.3 \cdot (-0.0291)^2 = 0.0001 + 0.3 \cdot 0.000847 = 0.000354$$
$$\sigma_3 \approx 1.88\%$$

Volatility nearly doubled — from 1.04% to 1.88%. One big day spikes tomorrow's expected vol.

**Day 3:** $\sigma_3 = 1.88\%$. Draw $z_3 = +0.3$. Modest day.
$$r_3 = 0 + 0.0188 \cdot 0.3 = +0.56\%$$
$$\sigma_4^2 = 0.0001 + 0.3 \cdot (0.0056)^2 = 0.0001 + 0.3 \cdot 0.000031 = 0.000109$$
$$\sigma_4 \approx 1.04\%$$

Volatility drops back. The +0.56% day was small, so tomorrow's expected vol returns to baseline.

**The pattern:** Big shock → tomorrow's vol spikes. Small shock → tomorrow's vol decays back to baseline. This is volatility clustering — not as a description, but as a *generating mechanism*.

---

## Step 3: The Limitation of ARCH(1)

ARCH(1) says: only yesterday's shock matters. But in reality, volatility is *persistent* — it stays elevated for days or weeks after a shock, not just one day.

In the ARCH(1) example above, volatility spiked to 1.88% on day 3 but dropped back to 1.04% on day 4 — just two days after the shock. Real volatility doesn't decay that fast.

---

## Step 4: GARCH(1,1) — Adding Persistence

GARCH = **G**eneralized ARCH. The generalization: add yesterday's *variance* as a predictor of today's variance.

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \sigma_{t-1}^2$$

**Terms:**
- $\sigma_t^2$: variance today
- $\omega$: baseline variance (the floor)
- $\alpha$: reaction to yesterday's shock — how much new information matters
- $r_{t-1}^2$: yesterday's squared return (the new shock)
- $\beta$: persistence — how much of yesterday's variance carries over
- $\sigma_{t-1}^2$: yesterday's variance

The $\beta$ term is the key. It says: "even if today's return is zero, volatility stays elevated because yesterday's volatility was high."

### Walkthrough With Persistence

Same parameters as before: $\omega = 0.0001$, $\alpha = 0.10$, now add $\beta = 0.85$.

**Day 1:** $\sigma_1^2 = 0.0001$, $\sigma_1 = 1.0\%$. Draw $z_1 = -2.8$.
$$r_1 = -2.8\%$$
$$\sigma_2^2 = 0.0001 + 0.10 \cdot (-0.028)^2 + 0.85 \cdot 0.0001 = 0.0001 + 0.000078 + 0.000085 = 0.000263$$
$$\sigma_2 \approx 1.62\%$$

**Day 2:** $\sigma_2 = 1.62\%$. Draw $z_2 = +0.3$ (quiet day).
$$r_2 = 0 + 0.0162 \cdot 0.3 = +0.49\%$$
$$\sigma_3^2 = 0.0001 + 0.10 \cdot (0.0049)^2 + 0.85 \cdot 0.000263 = 0.0001 + 0.000002 + 0.000224 = 0.000326$$
$$\sigma_3 \approx 1.81\%$$

Volatility actually **increased** from 1.62% to 1.81% even though day 2 was quiet. Why? Because 85% of yesterday's elevated variance ($0.85 \times 0.000263$) persisted. The quiet day added almost nothing ($\alpha \cdot r^2 \approx 0$), but $\beta$ carried the old volatility forward.

**Day 3-10 (all quiet days):** With no further shocks, variance decays at rate $\beta = 0.85$ per day:

$$0.000326 \rightarrow 0.000277 \rightarrow 0.000236 \rightarrow 0.000200 \rightarrow 0.000170 \rightarrow 0.000145 \rightarrow 0.000123 \rightarrow 0.000105$$

After 8 quiet days, vol is back near baseline. The half-life of a volatility shock is:

$$\text{Half-life} = \frac{\ln(0.5)}{\ln(\beta)} = \frac{-0.693}{\ln(0.85)} = \frac{-0.693}{-0.163} \approx 4.3 \text{ days}$$

**Terms:**
- Half-life: how many days it takes for the elevated variance to decay halfway back to baseline
- With $\beta = 0.85$: ~4.3 days
- With $\beta = 0.95$: ~13.5 days (more persistent)
- With $\beta = 0.99$: ~69 days (very persistent — near-integrated GARCH)

---

## The Intuition in One Table

| Parameter | What It Controls | Typical Range |
|---|---|---|
| $\omega$ | Baseline variance when nothing is happening | Very small (e.g., 0.000001–0.0001) |
| $\alpha$ | How much new shocks matter — the "news" coefficient | 0.05–0.20 |
| $\beta$ | How much old volatility persists — the "memory" coefficient | 0.80–0.95 |
| $\alpha + \beta$ | Total persistence — if close to 1, shocks decay very slowly | Usually 0.95–0.995 |

---

## Check-In

The core idea: GARCH replaces "volatility is a fixed number" with "volatility is a number that evolves based on recent shocks and its own past."

The three parameters have clear interpretations:
- $\omega$: the floor — vol can't go below this
- $\alpha$: how jumpy vol is in response to new shocks
- $\beta$: how sticky vol is — how long elevated vol persists

**Does this make sense?** And the key question: once you've estimated $\omega$, $\alpha$, and $\beta$ from data, you can simulate from this process. Each simulated path will have its own pattern of calm periods and volatile clusters. **Does it click now why Monte Carlo + GARCH gives you something parametric VaR can't?**