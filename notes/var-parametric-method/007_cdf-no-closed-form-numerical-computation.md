# How Do We Actually Get Z-Scores and Probabilities? The CDF, Its Inverse, and Why There's No Formula

**Date:** 2026-07-07
**Topic:** Where the numbers come from — the standard normal CDF, why it's not invertible, and what "numerically computed" means

---

## The Question You're Asking

You've accepted that $z_{0.05} = -1.6449$ and $\Phi(-1.6449) = 0.05$. But where do these numbers actually *come from*? How does a computer or a table produce them?

This is a genuinely important question because it's the difference between *using* a tool and *understanding* it.

---

## Part 1: The PDF of the Standard Normal

The standard normal probability density function (PDF) is:

$$\phi(z) = \frac{1}{\sqrt{2\pi}} e^{-z^2/2}$$

**Terms:**
- $\phi(z)$: the PDF of the standard normal — the height of the bell curve at point $z$
- $z$: any real number (the point on the x-axis)
- $e$: Euler's number (≈ 2.71828)
- $\pi$: the circle constant (≈ 3.14159)

This is the bell curve formula. It tells you how *dense* the probability is at each point $z$.

```
φ(z)
 │
 │        ___
 │      /     \
 │    /         \        φ(0) = 1/√(2π) ≈ 0.399
 │  /             \      φ(-1.6449) = (1/√(2π))·e^(-1.6449²/2) ≈ 0.103
 │/   ░░░░░░░░░░░░░\
─┼──────────────────┼──
-∞   -1.6449    0   +∞
```

The PDF gives the *height*. The CDF gives the *area under the curve*.

---

## Part 2: The CDF — Area Under the Curve

The cumulative distribution function (CDF) $\Phi(z)$ is the integral of the PDF from $-\infty$ to $z$:

$$\Phi(z) = \int_{-\infty}^{z} \phi(t) \, dt = \int_{-\infty}^{z} \frac{1}{\sqrt{2\pi}} e^{-t^2/2} \, dt$$

**Terms:**
- $\Phi(z)$: the CDF — probability that a standard normal random variable is $\leq z$
- $\int_{-\infty}^{z}$: the definite integral from negative infinity to $z$
- $t$: a dummy variable of integration (same role as $z$, just renamed to avoid confusion)

**In words:** To find the probability of being below $z$, we integrate the bell curve from $-\infty$ up to $z$. The area under the PDF curve between $-\infty$ and $z$ IS the probability.

```
φ(t)
 │
 │        ___                 ┌─────────────────┐
 │      /     \               │   ░░░░░ = area   │
 │    /         \             │   = Φ(z)         │
 │  /   ░░░░░░░░░\            │   = probability  │
 │/░░░░░░░░░░░░░░░\           │   = P(Z ≤ z)     │
─┼─────────────────┼──        └─────────────────┘
-∞                 z
 ←──── area = Φ(z) ────→
```

---

## Part 3: Why There's No Closed Form

### What is a "closed form" formula?

A **closed form** expression is one that uses only:
- Elementary functions: polynomials, exponentials, logs, trig functions, roots
- In a **finite** combination (no infinite sums, no limits)

Examples of closed forms:
- $x^2 + 3x - 5$ (polynomial)
- $\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ (quadratic formula)
- $\ln(1 + x)$

### Why doesn't $\Phi(z)$ have one?

The integral:

$$\int e^{-t^2/2} \, dt$$

**has no elementary antiderivative.** This is a proven mathematical fact — it's not that we haven't found one; it's that one *cannot exist* using only elementary functions.

The function $e^{-t^2/2}$ looks simple, but its integral is fundamentally different from integrals like $\int e^t \, dt = e^t$ or $\int t^n \, dt = t^{n+1}/(n+1)$. The Gaussian integral is in a different category.

### What is the error function (erf)?

Since the Gaussian integral is so important, mathematicians defined a **special function** for it:

$$\text{erf}(x) = \frac{2}{\sqrt{\pi}} \int_0^x e^{-t^2} \, dt$$

The normal CDF can be expressed in terms of erf:

$$\Phi(z) = \frac{1}{2}\left[1 + \text{erf}\left(\frac{z}{\sqrt{2}}\right)\right]$$

But erf itself is not an elementary function — it's defined *by* the integral. Saying "$\Phi(z)$ = ½[1 + erf(z/√2)]" is just giving a name to the thing we can't compute in closed form.

---

## Part 4: What "Numerically Computed" Means

If there's no formula, how do we get $\Phi(1.6449) = 0.95$ or $\Phi^{-1}(0.05) = -1.6449$?

### Method 1: Series Expansion (the mathematical approach)

The exponential function can be expanded as an infinite series:

$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$$

Substituting $x = -t^2/2$:

$$e^{-t^2/2} = 1 - \frac{t^2}{2} + \frac{t^4}{8} - \frac{t^6}{48} + \cdots$$

Integrate term by term:

$$\Phi(z) = \frac{1}{2} + \frac{1}{\sqrt{2\pi}} \left(z - \frac{z^3}{6} + \frac{z^5}{40} - \frac{z^7}{336} + \cdots\right)$$

This is an **infinite series**. You can approximate $\Phi(z)$ by taking enough terms. For $z = 1.6449$, you might need 20-30 terms for good accuracy, and the series converges slowly for large $z$.

### Method 2: Rational Approximations (the practical approach)

In practice, neither scipy nor statistical tables use series expansions directly. They use **rational approximations** — ratios of polynomials carefully fitted to the true function.

For example, one widely-used approximation for $\Phi(z)$ (from Abramowitz & Stegun, formula 26.2.17):

$$\Phi(z) \approx 1 - \frac{1}{2}\left(1 + c_1 z + c_2 z^2 + c_3 z^3 + c_4 z^4\right)^{-4}$$

where $c_1, c_2, c_3, c_4$ are carefully chosen constants. This approximation is accurate to about 7 decimal places.

### Method 3: For the Inverse CDF (going from probability to z)

The inverse CDF $\Phi^{-1}(p)$ is even harder — there's no series to directly invert. Instead, numerical methods are used:

1. **Rational approximations** directly fitted to $\Phi^{-1}$
2. **Root-finding:** For a given $p$, find $z$ such that $\Phi(z) - p = 0$ using Newton's method or bisection. This works because $\Phi(z)$ is monotonic (always increasing).

```python
# Inside scipy.stats.norm.ppf, conceptually:
def ppf(p):
    # Use a rational approximation fitted to Φ⁻¹
    # For the tails, use a different approximation (asymptotic expansion)
    # For the middle, use a polynomial approximation
    return z
```

---

## Part 5: The Concrete Pipeline

So when you call `norm.ppf(0.05)` in Python, here's what happens:

```
INPUT: p = 0.05

1. Check: is p in the middle (0.025 to 0.975) or in the tails?
   → 0.05 is in the lower tail

2. Use the tail approximation formula:
   (a rational function fitted to the asymptotic behavior of Φ⁻¹)

3. Compute: z ≈ -1.6448536269514729

4. Return z

OUTPUT: -1.6449
```

And `norm.cdf(-1.6449)`:

```
INPUT: z = -1.6449

1. Check: is z positive or negative?
   → negative, use symmetry: Φ(-z) = 1 - Φ(z)

2. For positive 1.6449, use rational approximation to Φ

3. Compute: Φ(1.6449) ≈ 0.950015

4. By symmetry: Φ(-1.6449) = 1 - 0.950015 = 0.049985 ≈ 0.05

OUTPUT: 0.05
```

---

## Part 6: What This Means for You

The key takeaways:

1. **There is no simple formula.** $\Phi(z)$ and $\Phi^{-1}(p)$ are computed by approximation algorithms, not by plugging numbers into a closed-form expression.

2. **This is normal in mathematics.** Many important functions have no closed form: $\int e^{-x^2} dx$, $\int \frac{\sin x}{x} dx$, the gamma function $\Gamma(x)$ for non-integer $x$. We define special functions for them and compute them numerically.

3. **The approximations are extremely accurate.** The rational approximations used by scipy are accurate to machine precision (about 15 decimal places). For any practical purpose, `norm.ppf(0.05)` IS the true value.

4. **The historical tables** (the "standard normal table" you find in textbooks) were computed by hand using series expansions — a monumental effort before computers existed. Today, it's a single line of code.

---

## The Deep Point

When we say "the parametric method assumes normality," we're not just assuming a shape — we're choosing a distribution whose CDF has no closed form. This is a curiosity, not a practical problem, because numerical methods solve it perfectly.

But it's worth knowing: the numbers you trust ($z_{0.05} = 1.6449$) are the output of clever approximation algorithms, not the result of plugging into a simple formula. The formula *defines* the CDF (as an integral), but doesn't give you a way to *compute* it directly.

---

## Check Your Understanding

**Q1:** Why can't we just write $\Phi(z) = \text{[some formula]}$ and plug in $z$?

**Q2:** If $\Phi(z)$ has no closed form, how did people compute the standard normal tables before computers?

**Q3:** What's the relationship between $\text{erf}(x)$ and $\Phi(z)$? Is erf a "solution" to the problem or just a renaming?