# The Z-Score Is NOT a Probability — It's a Distance

**Date:** 2026-07-07
**Topic:** What the Z-score actually is, and why the formula is μ − z×σ not something else

---

## The Hazy Concept You Identified

> "the z score is some std dev normalised probability or something, not sure?"

That's exactly right to flag. Let's make it crystal clear.

---

## The Z-Score: A Ruler, Not a Probability

**A Z-score is a distance measured in standard deviations from the mean.**

That's it. It's a ruler — not a probability.

### Concrete Example

```
SPY daily returns: μ = +0.05%, σ = 1.2%

Question: "What return is 2 standard deviations below the mean?"

Answer: μ − 2σ = 0.05% − 2(1.2%) = 0.05% − 2.4% = −2.35%

The Z-score here is 2.
It means "2 standard deviations below."
```

The Z-score is just the **number of σ units** you move from the mean.

### Three Different Things — Don't Confuse Them

| Concept | What It Is | Example |
|---|---|---|
| **Z-score** | Distance from mean in σ units | $z = 1.6449$ |
| **CDF(z)** | Probability of being below that z | $\Phi(-1.6449) = 0.05$ |
| **The return value x** | The actual return at that distance | $x = \mu - 1.6449\sigma$ |

The Z-score is the *input* to the CDF, not the CDF itself. The CDF translates distance → probability.

---

## Where Does z = 1.6449 Come From?

It comes from the **standard normal distribution**: a normal distribution with $\mu = 0$ and $\sigma = 1$.

```
Standard Normal N(0,1):

          ___
        /     \
      /         \                    Area to the left
    /             \                  of this line = 5%
   /   ░░░░░░░░░░░░\                ─────────────────
──┼───┼─────────────┼──
 -2   -1.6449       0
      ↑
      This is z₀.₀₅ = −1.6449
```

For $N(0,1)$, the value at which the CDF equals 0.05 is $z = -1.6449$.

In notation: $\Phi(-1.6449) = 0.05$

**Translation:** In a standard normal, 5% of the probability mass sits below -1.6449. The number -1.6449 is the *position* on the x-axis, not the probability itself.

---

## Deriving the Parametric VaR Formula — Step by Step

Now let's derive the formula from first principles. You have a nice intuition — let me make it rigorous.

### Step 1: What Are We Trying to Find?

We want the return $r^*$ such that:

$$P(r \leq r^*) = 0.05$$

**Terms:**
- $r$: tomorrow's return (a random variable)
- $r^*$: the threshold return we're solving for (the VaR)
- $0.05$: the confidence complement (5% for 95% confidence)

### Step 2: Assume Normality

We assume $r \sim N(\mu, \sigma^2)$.

**Terms:**
- $r \sim N(\mu, \sigma^2)$: returns follow a normal distribution with mean $\mu$ and variance $\sigma^2$

### Step 3: Standardize — Convert to Z-Score Space

Any normal random variable can be converted to standard normal by:

$$z = \frac{r - \mu}{\sigma}$$

**Terms:**
- $z$: the standardized return (now follows $N(0,1)$)
- $r$: the original return
- $\mu$: the mean of the original distribution
- $\sigma$: the standard deviation of the original distribution

This transformation does two things:
1. **Centers** the distribution at 0 (subtract $\mu$)
2. **Scales** it so 1 unit = 1 standard deviation (divide by $\sigma$)

### Step 4: Apply the CDF in Standardized Space

We want:

$$P(r \leq r^*) = 0.05$$

Standardize both sides:

$$P\left(\frac{r - \mu}{\sigma} \leq \frac{r^* - \mu}{\sigma}\right) = 0.05$$

The left side is now a standard normal random variable. In $N(0,1)$, the value below which 5% of the mass falls is:

$$\frac{r^* - \mu}{\sigma} = z_{0.05}$$

where $z_{0.05} = -1.6449$ (from the standard normal table).

### Step 5: Solve for $r^*$

$$\frac{r^* - \mu}{\sigma} = z_{0.05}$$

$$r^* - \mu = z_{0.05} \cdot \sigma$$

$$r^* = \mu + z_{0.05} \cdot \sigma$$

Since $z_{0.05} = -1.6449$:

$$r^* = \mu + (-1.6449) \cdot \sigma$$

$$r^* = \mu - 1.6449 \cdot \sigma$$

### This is the Parametric VaR Formula

$$\text{VaR}_{95\%} = \mu - 1.6449 \cdot \sigma$$

Or more generally for confidence level $\alpha$:

$$\text{VaR}_{1-\alpha} = \mu - z_{\alpha} \cdot \sigma$$

**Terms:**
- $\text{VaR}_{1-\alpha}$: the Value at Risk at $(1-\alpha)$ confidence level (e.g., 95%)
- $\mu$: the mean of daily returns
- $z_{\alpha}$: the **absolute value** of the Z-score at the $\alpha$ quantile (positive number, e.g., 1.6449 for $\alpha = 0.05$)
- $\sigma$: the standard deviation of daily returns

> **Notation note:** Some texts write $\text{VaR} = \mu + z_{\alpha}\sigma$ where $z_{\alpha} = -1.6449$ (keeping the negative sign). Same result. I'll use $z_{\alpha}$ as the positive value and show the subtraction explicitly — it's more intuitive: "start at the mean, move left by z standard deviations."

---

## The Intuition You Were Reaching For

You said: *"we are taking the std dev scaled by z score from mean"*

That's exactly right. The formula says:

$$\text{VaR} = \underbrace{\mu}_{\text{start here}} - \underbrace{z_{\alpha}}_{\text{how many σ to move}} \times \underbrace{\sigma}_{\text{size of each step}}$$

| Component | Meaning |
|---|---|
| $\mu$ | Your starting point (expected return) |
| $z_{\alpha}$ | How many standard deviations you need to move to capture $\alpha$% of the left tail |
| $\sigma$ | How big each standard deviation "step" is for this asset |
| $z_{\alpha} \cdot \sigma$ | Total distance you move left from the mean |

---

## Concrete Numerical Example

Using your 60/40 portfolio data:

$$\mu = 0.0447\%, \quad \sigma = 0.8162\%, \quad z_{0.05} = 1.6449$$

$$\text{VaR} = 0.0447\% - (1.6449 \times 0.8162\%)$$
$$= 0.0447\% - 1.342\%$$
$$= -1.297\%$$

**Interpretation in words:** "Start at the mean return of +0.0447%. Move left by 1.6449 standard deviations, where each standard deviation is 0.8162%. You arrive at -1.297%. Under the normal distribution assumption, only 5% of days have returns worse than this."

---

## The Two-Step Translation

The parametric method does two things:

```
Step 1: Confidence → Z-score
  95% confidence → 5% left tail → z = 1.6449
  (This is pure math — standard normal CDF table)

Step 2: Z-score → Return
  1.6449 standard deviations below the mean for this specific asset
  = μ − 1.6449 × σ
  (This uses YOUR data's μ and σ)
```

Step 1 is the same for every asset. Step 2 uses your specific data.

---

## Check Your Understanding

**Q1:** If you want 99% confidence VaR, what Z-score do you use? (Hint: what z gives CDF = 0.01 in the standard normal?)

**Q2:** If SPY has μ = 0.04%, σ = 1.2%, what's the 99% parametric VaR? (z₀.₀₁ ≈ 2.326)

**Q3:** Why does a higher confidence level (99% vs 95%) produce a larger Z-score? What does "larger Z-score" mean geometrically on the bell curve?

---

Does the Z-score feel solid now? Or is the CDF translation ($\Phi(z) = p$) still hazy?
