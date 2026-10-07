# Why the Expectation of a Sum Is the Sum of the Expectations

A slow build-up of why $\mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y]$ — the fact doing most of the work in the expected-return decomposition. Concrete example first, then the general version.

---

## 1. Start concrete: two dice

You roll two dice.

- $X$ = the first die.
- $Y$ = the second die.
- $S = X + Y$ = the total.

From the previous doc, each die has $\mathbb{E}[X] = \mathbb{E}[Y] = 3.5$ (we worked that out: $(1+2+3+4+5+6)/6$).

The claim we're testing: $\mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y] = 3.5 + 3.5 = 7$.

Does the total of two dice really average 7? Yes — that's a famous fact. But let's actually *see why*, because the "why" is the whole lesson.

---

## 2. The average is a "grand total divided by the count"

There are 36 equally likely pairs $(X, Y)$, each with probability $\frac{1}{36}$.

The average of $S$ is just:

$$\mathbb{E}[S] = \frac{\text{sum of all 36 values of } (X+Y)}{36}$$

Now — and this is the key move — **split that grand total into two piles.**

**Pile 1: the X's.** Across the 36 pairs, the first die shows 1 in six pairs, 2 in six pairs, 3 in six pairs… all the way to 6 in six pairs. So the X's contribute:

$$6\cdot1 + 6\cdot2 + 6\cdot3 + 6\cdot4 + 6\cdot5 + 6\cdot6 = 6(1+2+3+4+5+6) = 6 \times 21 = 126$$

**Pile 2: the Y's.** Identical, by symmetry: $126$.

So the grand total is $126 + 126 = 252$, and:

$$\mathbb{E}[S] = \frac{252}{36} = 7$$

But notice what we just did. Splitting the total into two piles is the same as splitting the fraction:

$$\frac{252}{36} = \frac{126}{36} + \frac{126}{36} = 3.5 + 3.5$$

**The X-pile's average is $\mathbb{E}[X]$ and the Y-pile's average is $\mathbb{E}[Y]$.** That's the entire reason. The rule $\mathbb{E}[X+Y] = \mathbb{E}[X] + \mathbb{E}[Y]$ isn't a law of probability — it's just the fact that **adding up a sum, you're free to collect the $x$'s and the $y$'s separately.** Addition can be regrouped.

---

## 3. The general version, step by step

Let me write the same idea in symbols, slowly. An expectation is a weighted average: multiply each outcome by its probability, add everything up.

$$\mathbb{E}[X+Y] = \sum_{\text{all outcomes}} (x + y) \cdot P(x, y)$$

Here $P(x,y)$ just means "the probability of getting the pair $(x, y)$."

**Step 1 — multiply the probability into both terms.** The $x$ and the $y$ both sit inside the same bracket, both get multiplied by the same probability:

$$\sum (x + y) P = \sum \big(x\,P + y\,P\big)$$

**Step 2 — split one big sum into two sums.** Adding is adding; the order and grouping don't change the total:

$$\sum (x\,P + y\,P) = \sum x\,P + \sum y\,P$$

**Step 3 — recognise each sum for what it is.** $\sum x\,P$ means "each $x$, weighted by the total chance that $x$ happens" — and that's *by definition* $\mathbb{E}[X]$. Same for $y$. So:

$$\mathbb{E}[X+Y] = \mathbb{E}[X] + \mathbb{E}[Y]$$

That's it. Three steps, each one just shuffling addition around.

---

## 4. The surprising part: no independence required

Here's the thing that makes this rule so powerful, and it's worth pausing on.

Notice we **never once** used any assumption about whether $X$ and $Y$ are related. We didn't need to know if the first die influences the second. The regrouping works regardless.

To feel this, glue the two dice together so they always show the same number. Now there are only 6 outcomes — $(1,1), (2,2), \dots, (6,6)$ — each with probability $\frac{1}{6}$.

$$\mathbb{E}[X+Y] = \frac{(1+1)+(2+2)+\dots+(6+6)}{6} = \frac{2+4+6+8+10+12}{6} = \frac{42}{6} = 7$$

Same answer. $3.5 + 3.5 = 7$. The rule holds **even when $X$ and $Y$ are perfectly locked together.**

This is the whole reason your return decomposition needs no "correlation" term:

$$\mathbb{E}[r_p] = \mathbb{E}[w_S r_S + w_I r_I] = w_S \mathbb{E}[r_S] + w_I \mathbb{E}[r_I]$$

It doesn't matter whether stocks and bonds move together or move opposite each other. The *expected* portfolio return is always just the weighted average of the expected asset returns. No correction term. Done.

---

## 5. And a peek at why risk is different

Keep this "regrouping" idea in your back pocket, because it's exactly what *breaks* when we turn to variance.

Variance involves **squaring**, and squaring does not regroup the way adding does:

$$(a + b)^2 = a^2 + b^2 + 2ab$$

That leftover $2ab$ is the cross-term you *can't* get rid of — and it's why variance needs a covariance correction while expected value doesn't. Same two-asset portfolio, two very different answers: the mean splits cleanly, the variance doesn't.

---

**Try this to lock it in:** Using only the two facts we have now — $\mathbb{E}[X+Y] = \mathbb{E}[X] + \mathbb{E}[Y]$ and $\mathbb{E}[cX] = c\,\mathbb{E}[X]$ — write out $\mathbb{E}[w_S r_S + w_I r_I]$ step by step, and at each step say which fact you used and why. (Where I'd go after that: *why does the squaring break it?* — which is exactly what the 007 doc walks through.)
