# Expected Value and the Linearity of Expected Return

An introduction to expected value, built around the expected-return decomposition in the portfolio variance derivation (`E[r_p]` in Step 1). No prior stats assumed.

---

## 1. What "expected value" is

A **random variable** is just a number whose value you don't know yet, but where you know how likely each possible value is. In the variance file, `r_S` is "the return of the stock asset over the next period." You don't know it yet — it's random. But it has a *distribution*: a set of possible outcomes, each with a probability.

The **expected value** of a random variable is the *probability-weighted average* of its possible outcomes.

Think of it as the answer to: "if I could replay this situation a huge number of times, what would the outcomes average out to?"

**Example — a fair six-sided die.** Call the result $X$. The possible values are 1, 2, 3, 4, 5, 6, each with probability $\frac{1}{6}$.

The expected value is:

$$\mathbb{E}[X] = 1\!\cdot\!\tfrac{1}{6} + 2\!\cdot\!\tfrac{1}{6} + 3\!\cdot\!\tfrac{1}{6} + 4\!\cdot\!\tfrac{1}{6} + 5\!\cdot\!\tfrac{1}{6} + 6\!\cdot\!\tfrac{1}{6} = \frac{21}{6} = 3.5$$

Two things worth noticing right away:

1. **Each outcome is multiplied by its probability**, then everything is added up. That's the entire machinery. Nothing more to it.
2. **3.5 is not a possible roll.** You can never roll a 3.5. Expected value is a *center of mass*, not necessarily an actual outcome — and definitely not "the most likely" outcome or a guarantee. For a die every value is equally likely, yet the expected value is 3.5.

That last point matters a lot in finance. An expected return of 5% does **not** mean "you'll get 5%." It means "if this same situation played out many times, the average would tend toward 5%."

---

## 2. The notation, spelled out

When you see $\mathbb{E}[X]$:

- $\mathbb{E}$ is the "expectation operator" — the fancy letter E just stands for **E**xpected value.
- The thing inside the brackets is what we're taking the expectation *of*.
- Read $\mathbb{E}[X]$ out loud as "the expected value of $X$."

So in the variance file, $\mathbb{E}[r_S]$ reads "the expected value of the stock return" — i.e. the stock's average return. $\mathbb{E}[r_p]$ is "the expected value of the portfolio return."

The word **mean** and the phrase **expected value** mean the exact same thing. The file uses them interchangeably ("the mean (expected value) of $r_p$").

---

## 3. The two facts that make the portfolio math work

To go from $\mathbb{E}[w_S r_S + w_I r_I]$ to $w_S \mathbb{E}[r_S] + w_I \mathbb{E}[r_I]$, we use three tiny rules. Each is almost obvious once you say it in words.

**Fact 1 — the expectation of a constant is the constant.**

If $c$ is a fixed number (not random), then $\mathbb{E}[c] = c$. If something never varies, its "average" is just itself.

**Fact 2 — a constant factor comes out.**

$\mathbb{E}[c \cdot X] = c \cdot \mathbb{E}[X]$. Because each outcome gets multiplied by $c$, the whole average gets multiplied by $c$ too. (Double every die roll and the average goes from 3.5 to 7.)

**Fact 3 — the expectation of a sum is the sum of the expectations.**

$\mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y]$.

This is the big one. It holds **no matter how $X$ and $Y$ are related** — whether they move together, opposite, or are completely independent. Averaging commutes with adding.

Together, Facts 2 and 3 are called **linearity of expectation**. It's the single most important property you'll use over and over.

---

## 4. Applying it to the portfolio

Your portfolio return is a weighted sum of two asset returns:

$$r_p = w_S r_S + w_I r_I$$

Here:

- $r_p$ = the portfolio's return (random — unknown yet)
- $r_S$ = the stock asset's return (random)
- $r_I$ = the bond asset's return (random)
- $w_S$, $w_I$ = the **weights** — what fraction of your money is in each asset. These are *fixed numbers you chose*, not random. E.g. $w_S = 0.4$ means 40% of the portfolio is stocks.

Now take the expected value of both sides:

$$\mathbb{E}[r_p] = \mathbb{E}[w_S r_S + w_I r_I]$$

Apply **Fact 3** (expectation of a sum is the sum of expectations):

$$\mathbb{E}[r_p] = \mathbb{E}[w_S r_S] + \mathbb{E}[w_I r_I]$$

Apply **Fact 2** to each piece (the weights are constants, so they slide out):

$$\mathbb{E}[r_p] = w_S \mathbb{E}[r_S] + w_I \mathbb{E}[r_I]$$

That's the whole decomposition. In plain English:

> **The expected portfolio return is the weighted average of the expected asset returns.**

Each asset's average return, multiplied by its weight, added together.

---

## 5. A concrete number to anchor it

Say your portfolio is 40% stocks and 60% bonds:

- $w_S = 0.4$, and you expect stocks to return $\mathbb{E}[r_S] = 8\%$ on average.
- $w_I = 0.6$, and you expect bonds to return $\mathbb{E}[r_I] = 3\%$ on average.

Then:

$$\mathbb{E}[r_p] = (0.4)(8\%) + (0.6)(3\%) = 3.2\% + 1.8\% = 5\%$$

The portfolio's expected return is 5% — sitting between the two, weighted toward bonds because you hold more bonds.

---

## 6. Why this matters for what you're reading

The variance file spends its energy on **variance**, not expected return, and there's a sharp reason for that:

- **Expected return combines linearly** — a simple weighted average. Done. No extra terms.
- **Variance does not combine linearly** — because it involves *squaring* (remember $\text{Var}(X) = \mathbb{E}[(X - \mathbb{E}[X])^2]$), and $(a+b)^2 = a^2 + b^2 + 2ab$, not just $a^2 + b^2$. The leftover $2ab$ is exactly where the covariance cross-term comes from.

So the same two facts (linearity) that make the return side trivially clean are *unavailable* to you on the risk side. Expected value is linear; risk is not. That asymmetry — returns add up, risks don't — is one of the deepest ideas in the whole subject, and it's the reason that file has to walk through the squaring step so carefully.

---

One question to check it's landing: in Step 1 of the variance file, the line says the $w$'s are "constants — expectation passes right through them." Which of the three facts above is that sentence pointing at?
