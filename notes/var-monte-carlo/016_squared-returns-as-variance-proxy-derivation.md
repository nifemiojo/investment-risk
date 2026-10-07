# Squared Returns as a Proxy for Variance: Full Derivation

**Date:** 2026-07-10
**Topic:** Why $r_t^2$ is an unbiased estimate of $\sigma_t^2$ — step-by-step with no skipped steps

---

## The Setup

The ARCH/GARCH framework decomposes the return into two pieces:

$$r_t = \sigma_t \cdot z_t, \quad z_t \sim N(0,1)$$

**Terms:**
- $r_t$: the return on day t (what we observe)
- $\sigma_t$: the volatility (standard deviation) on day t (what we want to know but can't directly observe)
- $z_t$: a random draw from a standard normal distribution — the "standardized shock"

---

## Step 1: What Is Random and What Isn't?

This is the part that usually causes confusion. Let me be explicit about timing.

**At the start of day t, before the market opens:**

$\sigma_t$ is already determined. It's computed from yesterday's return and yesterday's variance:

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2 + \beta \cdot \sigma_{t-1}^2$$

Everything on the right side ($r_{t-1}$, $\sigma_{t-1}^2$) is known from yesterday. So $\sigma_t$ is a **known number** at the start of day t. It's not random.

**During day t:**

$z_t$ is drawn from N(0,1). This is the **random** part. We don't know what $z_t$ will be until the market closes. It could be +2.1 or −0.3 or any value from the standard normal distribution.

**After the market closes:**

We observe $r_t = \sigma_t \cdot z_t$. This is the product of a known number ($\sigma_t$) and a random draw ($z_t$).

---

## Step 2: Taking the Expectation — Which Terms?

We want to know: what is the expected value of $r_t^2$?

$$E[r_t^2] = E[(\sigma_t \cdot z_t)^2] = E[\sigma_t^2 \cdot z_t^2]$$

Now the key question: **which terms do we take the expectation of?**

The expectation operator $E[\cdot]$ only applies to **random variables.** Things that are already known are constants — they come out of the expectation.

$\sigma_t$ is known at the start of day t. It's a constant. $\sigma_t^2$ is a constant too.

$z_t$ is random. $z_t^2$ is random.

So:

$$E[\sigma_t^2 \cdot z_t^2] = \sigma_t^2 \cdot E[z_t^2]$$

We pull $\sigma_t^2$ out of the expectation because it's a constant. We keep $E[z_t^2]$ because $z_t$ is random.

---

## Step 3: What Is $E[z_t^2]$?

$z_t \sim N(0,1)$. This means:
- $E[z_t] = 0$ (mean is zero)
- $\text{Var}(z_t) = 1$ (variance is one)

Now, the definition of variance:

$$\text{Var}(z_t) = E[z_t^2] - (E[z_t])^2$$

Plug in what we know:

$$1 = E[z_t^2] - (0)^2$$
$$1 = E[z_t^2] - 0$$
$$E[z_t^2] = 1$$

**Terms:**
- $\text{Var}(z_t)$: the variance of the standard normal — equals 1
- $E[z_t^2]$: the expected value of the squared random variable
- $(E[z_t])^2$: the square of the expected value — equals 0² = 0

So $E[z_t^2] = 1$. The expected value of a squared standard normal draw is 1.

---

## Step 4: Putting It Together

$$E[r_t^2] = \sigma_t^2 \cdot E[z_t^2] = \sigma_t^2 \cdot 1 = \sigma_t^2$$

The expected value of the squared return equals the true variance.

---

## What This Means

$\sigma_t^2$ is the true variance. We can't observe it directly.

$r_t^2$ is the squared return. We can observe it.

On any given day, $r_t^2$ will not equal $\sigma_t^2$. If $z_t = 2.0$, then $r_t^2 = \sigma_t^2 \cdot 4$ — four times the true variance. If $z_t = 0.1$, then $r_t^2 = \sigma_t^2 \cdot 0.01$ — one hundredth of the true variance.

But **on average, across many days,** $r_t^2$ equals $\sigma_t^2$. The errors cancel out.

This is what "unbiased" means.

---

## Step 5: What Is an Unbiased Estimate?

An estimator is **unbiased** if its expected value equals the true value of the thing it's estimating.

**Example: Estimating a population mean**

You have a population with true mean $\mu$. You take a sample of size $n$ and compute the sample mean:

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

$E[\bar{x}] = \mu$. The sample mean is an **unbiased estimator** of the population mean. Any single sample mean might be off, but the expected value across all possible samples equals the truth.

**Example: $r_t^2$ as an estimator of $\sigma_t^2$**

The true thing we want to estimate is $\sigma_t^2$ (today's variance). Our estimator is $r_t^2$ (today's squared return).

$$E[\text{estimator}] = E[r_t^2] = \sigma_t^2 = \text{true value}$$

So $r_t^2$ is unbiased. But it's **very noisy** — any single observation can be far from the truth. The variance of the estimator itself is large.

---

## Step 6: Your Insight — Indirect Observation

You said:

> "Indirectly it is trying to observe or depend on yesterday's variance but through the observed return."

Yes. The ARCH model says:

$$\sigma_t^2 = \omega + \alpha \cdot r_{t-1}^2$$

It doesn't use $\sigma_{t-1}^2$ directly (ARCH(1) doesn't — GARCH adds it back via $\beta$). Instead, it uses $r_{t-1}^2$, which is an observable proxy for the unobservable $\sigma_{t-1}^2$.

The logic chain:

1. We want to know $\sigma_{t-1}^2$ (yesterday's true variance) — **unobservable**
2. We can observe $r_{t-1}$ (yesterday's return) — **observable**
3. $r_{t-1}^2$ is an unbiased estimate of $\sigma_{t-1}^2$ — **on average, it's right**
4. So we use $r_{t-1}^2$ as a stand-in for $\sigma_{t-1}^2$ in the variance equation

The GARCH model improves on this by using BOTH the noisy proxy ($r_{t-1}^2$) AND the previous period's modeled variance ($\sigma_{t-1}^2$). The $\beta$ term smooths out the noise in the squared return proxy.

---

## Check-In

Let me test whether this landed:

1. **Why do we take the expectation of $z_t^2$ but not $\sigma_t^2$?** Because $\sigma_t$ is known at the start of day t (it's computed from past data) — it's a constant. $z_t$ is the only random thing.

2. **Why does $E[z_t^2] = 1$?** Because $\text{Var}(z) = E[z^2] - (E[z])^2$, and for N(0,1), variance = 1 and mean = 0.

3. **What does "unbiased" mean?** The estimator's expected value equals the true value. $r_t^2$ on average equals $\sigma_t^2$, even though any single observation is noisy.

Does each step make sense?