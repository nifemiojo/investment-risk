# Distributions vs Processes: The Fundamentals

**Date:** 2026-07-10
**Topic:** What a distribution is, what it means to sample from it, and how a process is different

---

## Starting Simple: A Fair Coin

### The Distribution

A distribution is just a **list of possible outcomes and their probabilities.**

For a fair coin:

| Outcome | Probability |
|---------|------------|
| Heads   | 0.5        |
| Tails   | 0.5        |

That's it. That's the entire distribution. No formulas, no parameters — just two outcomes and two numbers that sum to 1.

### Sampling From the Distribution

**Sampling** means: pick one outcome at random, where each outcome is chosen with its stated probability.

If I sample from this distribution once, I get either Heads or Tails. I can't predict which — I only know the probabilities.

If I sample 10 times, I might get:

```
H, T, T, H, H, H, T, H, T, H  → 6 Heads, 4 Tails
```

Not exactly 5 and 5. The distribution says 50/50, but any finite sample will deviate. This is **sampling error**. The larger the sample, the closer the proportion gets to the true probabilities (Law of Large Numbers).

---

## A Distribution for Returns

Instead of Heads/Tails, let's define a distribution for daily returns. I'll use a discrete one first so we can see it:

| Daily Return | Probability |
|-------------|------------|
| −2.0%       | 0.05       |
| −1.0%       | 0.20       |
| 0.0%        | 0.50       |
| +1.0%       | 0.20       |
| +2.0%       | 0.05       |

This is a distribution. It says: on any given day, there's a 5% chance of a −2% return, a 20% chance of −1%, and so on.

### Sampling From This Distribution

Sampling means randomly picking one return according to these probabilities. One draw = one day's return.

If I sample 5 times, I might get:

```
+1.0%, 0.0%, −1.0%, 0.0%, +2.0%
```

That's 5 simulated daily returns. If I sort them from worst to best:

```
−1.0%, 0.0%, 0.0%, +1.0%, +2.0%
```

The worst of 5 is the 20th percentile. With 5 observations, the 5th percentile isn't even observable — you need at least 20 observations to have a data point at the 5th percentile. This is why Monte Carlo uses thousands of draws.

---

## The Normal Distribution: Same Idea, Continuous

The normal distribution is the same concept, but with infinitely many possible outcomes. Instead of a table, it's described by a formula:

$$f(r) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(r-\mu)^2}{2\sigma^2}}$$

**Terms:**
- $f(r)$: the probability density at return $r$ — how likely returns near $r$ are
- $\mu$: the center (mean)
- $\sigma$: the spread (standard deviation)

But conceptually, it's still just "a list of outcomes and probabilities" — the list is just continuous rather than discrete.

**Sampling from a normal distribution** means: the computer generates a random number where values near μ are most likely, and values far from μ are rare. The exact algorithm doesn't matter for our purposes (it's typically Box-Muller or the Ziggurat method). What matters is: each sample is an independent draw — one daily return.

---

## So Far: The Key Insight

A distribution is a **static object.** It describes what outcomes are possible and how likely they are. It has no concept of time, no concept of yesterday, no concept of sequence.

Sampling from a distribution means: draw one outcome according to those probabilities. Each draw is independent — the distribution doesn't change between draws.

If I sample 10,000 returns from N(0.05%, 1.2%²), sort them, and take the 5th percentile, I get (approximately) the parametric VaR. The only difference from the formula is sampling error.

---

## Now: What Is a Process?

A process is a distribution **that changes over time based on what happened before.**

Here's the simplest possible process:

$$r_t = \phi \cdot r_{t-1} + \epsilon_t, \quad \epsilon_t \sim N(0, \sigma^2)$$

**Terms:**
- $r_t$: return today
- $r_{t-1}$: return yesterday
- $\phi$: how much of yesterday's return carries over (e.g., 0.3 means 30% persistence)
- $\epsilon_t$: a fresh random shock drawn from N(0, σ²)

### Simulating a Process (Not Just Sampling)

To simulate this process for 5 days:

1. **Day 1:** No yesterday yet. Start with $r_0 = 0$. Draw $\epsilon_1$ from N(0, σ²). Say $\epsilon_1 = +0.8\%$. Then $r_1 = 0.3 \cdot 0 + 0.8\% = +0.8\%$.

2. **Day 2:** $r_1 = +0.8\%$. Draw $\epsilon_2 = -0.3\%$. Then $r_2 = 0.3 \cdot 0.8\% + (-0.3\%) = 0.24\% - 0.3\% = -0.06\%$.

3. **Day 3:** $r_2 = -0.06\%$. Draw $\epsilon_3 = +1.1\%$. Then $r_3 = 0.3 \cdot (-0.06\%) + 1.1\% = -0.018\% + 1.1\% = +1.082\%$.

4. **Day 4:** $r_3 = +1.082\%$. Draw $\epsilon_4 = -0.5\%$. Then $r_4 = 0.3 \cdot 1.082\% + (-0.5\%) = 0.325\% - 0.5\% = -0.175\%$.

5. **Day 5:** $r_4 = -0.175\%$. Draw $\epsilon_5 = +0.2\%$. Then $r_5 = 0.3 \cdot (-0.175\%) + 0.2\% = -0.053\% + 0.2\% = +0.147\%$.

The sequence: +0.8%, −0.06%, +1.08%, −0.18%, +0.15%.

### The Critical Difference

In a distribution, each draw is independent. The probability of +2% on day 5 is the same whether day 4 was +5% or −5%.

In a process, **today's return is a function of yesterday's return.** A big positive day makes tomorrow more likely to be positive (if φ > 0). The distribution you're effectively sampling from *changes* depending on what just happened.

---

## Visual Summary

| | Distribution | Process |
|---|---|---|
| **What it is** | A fixed set of outcomes and probabilities | A rule for how outcomes evolve over time |
| **Sampling** | Each draw is independent | Each draw depends on previous draws |
| **Example** | "Daily returns are N(0.05%, 1.2%²)" | "Today's return = 0.3 × yesterday's + random shock" |
| **Time** | Has no concept of time | Time is built in — $r_t$ is defined relative to $r_{t-1}$ |
| **VaR implication** | One VaR number for all days | Tomorrow's VaR depends on today's return |

---

## Check-In

Let me test whether this landed. I'll give you three scenarios — tell me whether each is a **distribution** or a **process**:

1. "Daily SPY returns follow a Student's t-distribution with 4 degrees of freedom, mean 0.05%, scale 1.2%."

2. "Daily volatility is 1.2% normally, but after a day where the return is more negative than −2%, volatility doubles to 2.4% for the next 5 trading days."

3. "The S&P 500 has returned an average of 10% per year with a standard deviation of 15% per year, and annual returns are approximately lognormal."

Distribution or process?