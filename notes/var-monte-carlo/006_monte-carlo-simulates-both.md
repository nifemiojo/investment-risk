# Monte Carlo Simulates Both Distributions and Processes

**Date:** 2026-07-10
**Topic:** Clarifying that Monte Carlo works for both — and when each is useful

---

## Yes, Both

Monte Carlo is just a simulation engine. You can feed it either:

### 1. A Distribution

```python
# Sample 10,000 independent draws from a normal distribution
simulated_returns = np.random.normal(loc=0.0005, scale=0.012, size=10000)
```

Each draw is independent. Day 1,487 doesn't care about day 1,486. This converges to the parametric VaR. The only reason to do this is if the distribution's quantile is hard to compute analytically.

### 2. A Process

```python
# Simulate a GARCH(1,1) process for 10,000 paths of 10 days each
for path in range(10000):
    sigma = current_sigma  # start from today's vol
    for day in range(10):
        epsilon = np.random.normal(0, 1)
        r = mu + sigma * epsilon           # return today
        sigma_sq = omega + alpha * r**2 + beta * sigma**2  # update vol
        sigma = sqrt(sigma_sq)
```

Each day's return depends on the previous day's volatility, which depends on the previous day's return. The sequence matters.

---

## The Difference in One Table

| | Simulating a Distribution | Simulating a Process |
|---|---|---|
| **What you specify** | Distribution + parameters (e.g., N(μ, σ²), t(ν)) | An equation for how $r_t$ evolves |
| **Draws** | Independent | Dependent (today depends on yesterday) |
| **What you get** | A sample of returns you can sort to find VaR | A sample of paths you can sort to find VaR |
| **When useful** | Distribution has no closed-form quantile | The data-generating process has memory |
| **Converges to** | The true quantile of that distribution | The quantile of the *process* — which no formula gives you |

---

## The Key Insight

You asked the right question. Monte Carlo is the **universal fallback:** if you can write down the rule for how returns are generated — whether it's a simple distribution or a complex process with memory — you can simulate it, sort the outcomes, and read the quantile.

The engine doesn't care whether the rule is simple or complex. It just runs the rule many times and aggregates the results.

The trade-off is:
- **Parametric:** fast, simple, but limited to what you can reduce to a formula
- **Monte Carlo:** flexible, can model anything you can code, but costs computation and introduces sampling error

---

## Check-In

Now that we've clarified the basics, let me return to the question I asked earlier about your three scenarios. Which of these are distributions and which are processes?

1. "Daily SPY returns follow a Student's t-distribution with 4 degrees of freedom, mean 0.05%, scale 1.2%."

2. "Daily volatility is 1.2% normally, but after a day where the return is more negative than −2%, volatility doubles to 2.4% for the next 5 trading days."

3. "The S&P 500 has returned an average of 10% per year with a standard deviation of 15% per year, and annual returns are approximately lognormal."

And for each one: **could you compute VaR from it with a parametric formula? Would Monte Carlo add anything?**