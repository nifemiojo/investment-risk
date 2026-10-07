# Why Squared Returns? The ARCH Intuition

**Date:** 2026-07-10
**Topic:** Why ARCH models use $r_{t-1}^2$ rather than $r_{t-1}$

---

## The Core Reason: Variance Cares About Size, Not Sign

A +5% day and a −5% day are both large moves. Both signal that something happened — volatility is elevated. If the model used $r_{t-1}$ (not squared):

- $r_{t-1} = +5\%$ → today's variance goes **up**
- $r_{t-1} = -5\%$ → today's variance goes **down**

That's wrong. Negative returns don't reduce future volatility — they increase it, just like positive returns. Squaring strips the sign:

$$(+5\%)^2 = 0.0025$$
$$(-5\%)^2 = 0.0025$$

Same squared return → same effect on tomorrow's variance. The model only cares about *how big* the move was, not which direction.

---

## The Deeper Reason: Variance Is Naturally About Squares

Variance is defined as:

$$\sigma^2 = E[(r - \mu)^2]$$

It's the expected value of the squared deviation from the mean. So modeling variance in terms of squared returns isn't arbitrary — it follows directly from the definition of variance.

If you want to model how variance evolves, the natural input is the thing variance is made of: squared deviations.

---

## The Statistical Reason: $r_{t-1}^2$ Is a Proxy for the Unobservable Variance

Here's the subtle point. In the ARCH framework:

$$r_t = \sigma_t \cdot z_t, \quad z_t \sim N(0,1)$$

The true variance $\sigma_t^2$ is unobservable. But we can observe the return $r_t$. And:

$$r_t^2 = \sigma_t^2 \cdot z_t^2$$

Since $E[z_t^2] = 1$, the expected value of $r_t^2$ is $\sigma_t^2$:

$$E[r_t^2] = \sigma_t^2 \cdot E[z_t^2] = \sigma_t^2 \cdot 1 = \sigma_t^2$$

So $r_{t-1}^2$ is a *noisy but unbiased estimate* of yesterday's true variance. When the ARCH model uses $r_{t-1}^2$, it's saying: "I can't observe yesterday's variance directly, but I can observe yesterday's squared return, which is my best guess."

---

## Concrete Contrast

Using $r_{t-1}$ (wrong):

| Yesterday | Effect on Today's Vol |
|---|---|
| +4% | ↑ higher vol |
| −4% | ↓ lower vol |
| +0.1% | ≈ no change |
| −0.1% | ≈ no change |

Using $r_{t-1}^2$ (correct):

| Yesterday | Squared | Effect on Today's Vol |
|---|---|---|
| +4% | 0.0016 | ↑ higher vol |
| −4% | 0.0016 | ↑ higher vol (same) |
| +0.1% | 0.000001 | ≈ no change |
| −0.1% | 0.000001 | ≈ no change (same) |

Both large moves increase vol. Both small moves leave vol unchanged. Direction is irrelevant.

---

## Why Not Use |r_{t-1}|?

Good question. Absolute returns also capture magnitude without sign. Some models do use absolute returns — they're called "absolute value GARCH" or similar variants.

The reason squared returns are standard: they connect directly to the definition of variance ($E[r^2]$), they're mathematically more tractable (derivatives are clean), and they give more weight to extreme observations. A 5% move is 25× more influential than a 1% move when squared (0.0025 vs 0.0001), but only 5× more influential in absolute value. The squared version says "extreme events are much more informative about future volatility" — which matches empirical reality.

---

## Check-In

Three reasons:
1. **Sign doesn't matter:** A crash and a rally both signal elevated vol
2. **Definitional:** Variance is about squared deviations by definition
3. **Statistical:** $r_{t-1}^2$ is an unbiased proxy for the unobservable $\sigma_{t-1}^2$

Make sense?