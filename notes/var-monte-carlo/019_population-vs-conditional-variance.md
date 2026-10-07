# Population vs Sample, Conditional vs Unconditional: The Variance Question

**Date:** 2026-07-10
**Topic:** What "population variance" means in a GARCH world — and why it's different from classical statistics

---

## Question 1: The Notation Confusion

You're right. In classical statistics:

- $\sigma^2$: population variance (the true, fixed, unknown parameter)
- $s^2$ or $\hat{\sigma}^2$: sample variance (our estimate from data)

In GARCH, the notation reuses $\sigma_t^2$ to mean something different: the **conditional variance** at time t — the variance of $r_t$ given all information up to time t−1. It's not a fixed population parameter. It changes every day.

I should have been more careful. Let me use clearer notation from here:

| Notation | Meaning |
|---|---|
| $\sigma^2_{\text{uncond}}$ | Unconditional variance — the variance of returns if you ignore time (the "long-run average" variance) |
| $\sigma_t^2$ | Conditional variance at time t — the variance of $r_t$ given what happened up to t−1 |
| $\hat{\sigma}_t^2$ | Modeled/estimated conditional variance from GARCH |

---

## Question 2: Why $\sigma_t$ Is Deterministic at the Start of Day t

Your understanding is correct:

$$\hat{\sigma}_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \hat{\sigma}_{t-1}^2$$

At the start of day t, everything on the right is known:
- $r_{t-1}$: yesterday's return — observed
- $\hat{\sigma}_{t-1}^2$: yesterday's modeled variance — computed from the day before

So $\hat{\sigma}_t$ is deterministic. It's a number. The only random thing on day t is $z_t$.

---

## Question 3: GARCH Uses Both the Proxy and the Modeled Variance

Yes. The GARCH(1,1) equation:

$$\hat{\sigma}_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \hat{\sigma}_{t-1}^2$$

- $\alpha \cdot r_{t-1}^2$: the "news" — yesterday's squared return as a noisy proxy for yesterday's true conditional variance
- $\beta \cdot \hat{\sigma}_{t-1}^2$: the "memory" — yesterday's modeled variance, which is a smoothed estimate

GARCH blends a noisy observation ($r_{t-1}^2$) with a smoothed model ($\hat{\sigma}_{t-1}^2$). This is similar to how exponential smoothing blends the latest observation with the previous smoothed value.

---

## Question 4: The Estimator Itself Has a Distribution

Yes. $r_t^2$ is a random variable. Its distribution depends on the true $\sigma_t^2$.

Since $r_t = \sigma_t \cdot z_t$ and $z_t \sim N(0,1)$:

$$r_t^2 = \sigma_t^2 \cdot z_t^2$$

$z_t^2$ follows a chi-squared distribution with 1 degree of freedom ($\chi^2_1$). So:

$$r_t^2 \sim \sigma_t^2 \cdot \chi^2_1$$

The $\chi^2_1$ distribution has mean 1 and variance 2. So:

$$E[r_t^2] = \sigma_t^2 \cdot 1 = \sigma_t^2$$
$$\text{Var}(r_t^2) = \sigma_t^4 \cdot 2 = 2\sigma_t^4$$

This is why $r_t^2$ is such a noisy proxy. If $\sigma_t = 1\%$, then $\sigma_t^2 = 0.0001$, and $\text{Var}(r_t^2) = 2 \times 10^{-8}$. The standard deviation of the estimator is $\sqrt{2} \times \sigma_t^2 \approx 1.41 \times 0.0001 = 0.000141$ — which is larger than the thing being estimated ($0.0001$).

The estimator is unbiased but has enormous variance. Any single $r_t^2$ tells you very little about $\sigma_t^2$. That's why GARCH smooths it with the $\beta$ term.

---

## Question 5: Does $\hat{\sigma}_{t-1}^2$ Carry Information About $\sigma_t^2$?

Yes — and this is the $\beta$ term. $\hat{\sigma}_{t-1}^2$ is your best estimate of yesterday's conditional variance. Since volatility is persistent ($\beta$ is typically 0.85–0.95), yesterday's variance is the best predictor of today's variance — better than the noisy squared return alone.

The GARCH equation can be rewritten to make this clearer:

$$\hat{\sigma}_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \hat{\sigma}_{t-1}^2$$

If $\alpha$ is small (say 0.05) and $\beta$ is large (say 0.90), then 90% of today's variance estimate comes from yesterday's smoothed estimate, and only 5% comes from the latest noisy observation. The model is saying: "I trust my smoothed estimate more than I trust the latest squared return."

---

## Question 6: Is There a Single Population Variance?

This is the deepest question, and the answer is: **it depends on which variance you're asking about.**

### The Unconditional Variance

If you take a long series of GARCH-generated returns and compute the sample variance (ignoring time), it converges to:

$$\sigma^2_{\text{uncond}} = \frac{\omega}{1 - \alpha - \beta}$$

**Terms:**
- $\sigma^2_{\text{uncond}}$: the unconditional (long-run) variance
- $\omega$: the baseline
- $\alpha + \beta$: total persistence

This is a single number. It's the "population variance" in the classical sense — the variance of the marginal distribution of returns if you don't condition on time.

For example, if $\omega = 0.00001$, $\alpha = 0.05$, $\beta = 0.90$:

$$\sigma^2_{\text{uncond}} = \frac{0.00001}{1 - 0.05 - 0.90} = \frac{0.00001}{0.05} = 0.0002$$

$$\sigma_{\text{uncond}} \approx 1.41\%$$

### The Conditional Variance

$\sigma_t^2$ is a different thing. It's the variance of $r_t$ **given the specific history up to t−1.** It's not a population parameter — it's a time-varying quantity that describes the current state.

After a crash, $\sigma_t^2$ might be $0.0006$ (σ ≈ 2.45%). After a calm period, $\sigma_t^2$ might be $0.00012$ (σ ≈ 1.10%). Both are "true" conditional variances — they just apply to different days.

### The Distinction

| | Unconditional Variance | Conditional Variance |
|---|---|---|
| **What it is** | Long-run average variance, ignoring time | Variance today, given what happened yesterday |
| **Is it static?** | Yes — a single number | No — changes every day |
| **Relevant for** | Long-horizon average risk | Tomorrow's risk given today's state |
| **GARCH notation** | $\frac{\omega}{1-\alpha-\beta}$ | $\sigma_t^2$ |

### What $r_t^2$ Estimates

$r_t^2$ is an unbiased estimate of $\sigma_t^2$ (the conditional variance), not $\sigma^2_{\text{uncond}}$:

$$E[r_t^2 \mid \text{past}] = \sigma_t^2$$

But if you average $r_t^2$ over a very long sample, it converges to $\sigma^2_{\text{uncond}}$:

$$\lim_{n \to \infty} \frac{1}{n}\sum_{t=1}^{n} r_t^2 = \sigma^2_{\text{uncond}}$$

So $r_t^2$ is carrying information about both: today's conditional variance (in expectation), and the long-run unconditional variance (when averaged over time).

---

## The Key Insight

Classical statistics says: "There is a true fixed variance. We estimate it from data."

GARCH says: "Variance changes over time. At any given moment, there's a true conditional variance — but it's a moving target. We track it using a model that blends recent observations with a smoothed estimate."

The "population" in GARCH is not a fixed distribution. It's a **conditional distribution** that shifts based on history. $r_t^2$ estimates the variance of today's conditional distribution, not some eternal fixed parameter.

---

## Check-In

That was a lot. Let me test the key distinction:

1. **What is $\sigma^2_{\text{uncond}}$ in a GARCH world?** The long-run average variance — what the sample variance converges to over a very long sample.

2. **What is $\sigma_t^2$?** The variance of today's return, given yesterday's return and yesterday's variance. It changes every day.

3. **Which one does $r_t^2$ estimate?** $\sigma_t^2$ — the conditional variance. But averaged over time, it converges to $\sigma^2_{\text{uncond}}$.

Does this clear up the population/sample/conditional confusion?