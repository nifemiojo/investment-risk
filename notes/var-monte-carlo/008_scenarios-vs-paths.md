# Scenarios vs Paths: The Distinction That Matters

**Date:** 2026-07-10
**Topic:** When one scenario means one draw, and when one scenario means a sequence of draws

---

## The Distinction

| Term | What It Is | When You Use It |
|---|---|---|
| **Scenario** (or draw) | One simulated outcome from a distribution | Simulating from a distribution for a single-period VaR |
| **Path** | A sequence of simulated outcomes linked by a process | Simulating a process over multiple periods |

---

## When They're the Same

For a **1-day VaR from a distribution,** one scenario = one path = one day's return. No distinction.

```
10,000 scenarios = 10,000 independent daily returns
```

Each scenario is just one random draw. Sort them, read the percentile. Done.

---

## When They're Different

For a **10-day VaR from a process,** one path is a sequence of 10 daily returns, where each day's return depends on the previous day's state.

One path looks like:

```
Day 1: r₁ = μ + σ₁·ε₁
Day 2: r₂ = μ + σ₂·ε₂    ← σ₂ depends on r₁
Day 3: r₃ = μ + σ₃·ε₃    ← σ₃ depends on r₂
...
Day 10: r₁₀ = μ + σ₁₀·ε₁₀  ← σ₁₀ depends on r₉
```

The 10-day return for this path is: $R_{\text{10-day}} = r_1 + r_2 + ... + r_{10}$

Then you generate 10,000 such paths → 10,000 ten-day returns → sort → read percentile.

```
10,000 paths = 10,000 × 10 = 100,000 individual daily draws
```

---

## Why This Matters

### Computational Cost

10,000 paths of a 10-day GARCH process = 100,000 individual simulations, each requiring the GARCH volatility update. That's 100× more work than 10,000 scenarios from a distribution.

If you're simulating a 1-year horizon at daily frequency: 10,000 paths × 252 days = 2.52 million individual draws. Non-trivial.

### The √t Trap

Parametric VaR for 10-day horizon: 1-day VaR × √10. This assumes:

$$r_1, r_2, ..., r_{10} \text{ are independent and identically distributed}$$

If they're not — if there's autocorrelation or volatility clustering — the √10 scaling is wrong. Monte Carlo with paths captures the actual dependence structure. The 10-day VaR from simulated paths may be higher or lower than √10 × 1-day VaR, depending on the process.

### The Difference Between "Simulating a Distribution" and "Simulating a Process" Revisited

| | Simulating a Distribution | Simulating a Process |
|---|---|---|
| **1-day VaR** | 10,000 scenarios (draws) | 10,000 scenarios (each = 1 step of the process) |
| **10-day VaR** | 10,000 scenarios of 10-day returns (draw from the 10-day distribution) OR just √t scale | 10,000 paths of 10 days each (100,000 total draws, each dependent) |
| **Where the work is** | One draw per scenario | Length-of-horizon draws per path, each dependent on the prior |

---

## In Practice

For a simple distribution with independent returns, you never simulate paths. You either:
- Simulate 1-day returns and √t scale
- Or simulate directly from the h-day distribution (e.g., r₁₀₋day ~ N(10·μ, 10·σ²) if normal)

For a process, you **must** simulate paths. The 10-day return isn't a draw from a simple distribution — it's the sum of 10 dependent draws. You can't shortcut this.

---

## Check-In

Now that the terminology is precise: when I said "10,000 scenarios" in the algorithm, I was talking about the 1-day case from a distribution. For a 10-day GARCH process, you'd need 10,000 paths of 10 days each.

Does the distinction make sense? And does it clarify why the computational cost of Monte Carlo can be significant — it's not just "10,000 draws," it's "10,000 × horizon-length draws" when simulating a process?