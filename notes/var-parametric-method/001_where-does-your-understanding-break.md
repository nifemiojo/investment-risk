# Where Does Your Understanding Break? The Core Puzzle of Parametric VaR

**Date:** 2026-07-07
**Topic:** Finding the first hazy concept before diving into parametric VaR

---

## What You Already Know

From session 006, you've seen the parametric formula:

$$\text{VaR}_{95\%} = \mu - (z_{0.05} \times \sigma)$$

You know it assumes returns follow a normal distribution. You've seen it produce a different answer from historical VaR on the same 60/40 data:

| Method | 95% VaR |
|---|---|
| Historical | -0.848% |
| Parametric | -1.296% |

And you know *why* they diverged: fat tails, skewness, kurtosis — the real data isn't normal.

---

## But Here's the Real Question

You know the formula. But do you know **why the formula works**?

Let me probe with a concrete scenario.

**Imagine:** You have 252 days of SPY returns. Instead of sorting them and picking the 13th worst (historical method), you instead compute just two numbers: the mean and the standard deviation. Then you plug them into $\mu - z \times \sigma$ and it spits out a VaR number.

**The puzzle:** How can two numbers (mean and vol) replace 252 data points? What gives us the right to collapse all that information?

---

## Three Hazy Spots to Identify

Before I explain anything, tell me which of these feels haziest to you:

**1. The Z-score — what is it and where does it come from?**

You've seen $z_{0.05} = -1.6449$. But why that number? Why not -2 or -1? What does -1.6449 actually *mean* in terms of probability?

**2. The normal distribution jump — why does assuming normality let us skip the sorting?**

Historical VaR sorts 252 points and picks position 13. Parametric VaR uses $\mu$ and $\sigma$ with no sorting at all. What's the logical connection? How does the normality assumption give us a shortcut?

**3. The formula itself — why subtract $z \times \sigma$ from the mean?**

Why subtraction? Why multiplication? Why not addition or division? What's the geometric/intuitive meaning of $\mu - z\sigma$?

---

Pick the one that feels haziest — or tell me if all three are hazy, or if something else entirely. That's where we'll drill.
