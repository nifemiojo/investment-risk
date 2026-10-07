Expectation is linear because **an expectation is fundamentally a probability-weighted average**, and weighted averages preserve addition and scalar multiplication.

## 1. Start with a concrete example

Suppose tomorrow's returns on two assets are:

| State | Probability |   $X$ |  $Y$ |
| ----- | ----------: | ----: | ---: |
| Good  |       $0.6$ | $10\%$ | $4\%$ |
| Bad   |       $0.4$ | $-5\%$ | $1\%$ |

Calculate their expectations separately.

$$
E[X] = 0.6(0.10) + 0.4(-0.05) = 4\%
$$

So $E[X] = 4\%$.

For $Y$:

$$
E[Y] = 0.6(0.04) + 0.4(0.01) = 2.8\%
$$

So $E[Y] = 2.8\%$.

Now define $Z = X + Y$.

In each state:

| State | Probability | $X+Y$ |
| ----- | ----------: | ----: |
| Good  |       $0.6$ | $14\%$ |
| Bad   |       $0.4$ | $-4\%$ |

Therefore:

$$
E[X + Y] = 0.6(0.14) + 0.4(-0.04) = 6.8\%
$$

But:

$$
E[X] + E[Y] = 4\% + 2.8\% = 6.8\%
$$

So:

$$
\boxed{E[X + Y] = E[X] + E[Y]}
$$

The important question is **why this must always happen**.

---

## 2. Expectation is just weighted averaging

Suppose there are states $1, 2, \dots, n$.

Each state has probability $p_1, p_2, \dots, p_n$, and $X$ takes values $X_1, X_2, \dots, X_n$.

Then expectation is:

$$
E[X] = \sum_i p_i X_i
$$

Likewise:

$$
E[Y] = \sum_i p_i Y_i
$$

Now consider $X + Y$. In state $i$, its value is $X_i + Y_i$.

Therefore:

$$
E[X + Y] = \sum_i p_i (X_i + Y_i)
$$

Distribute $p_i$:

$$
E[X + Y] = \sum_i \left(p_i X_i + p_i Y_i\right)
$$

Now split the sum:

$$
E[X + Y] = \sum_i p_i X_i + \sum_i p_i Y_i
$$

But these are exactly the definitions of $E[X]$ and $E[Y]$:

$$
\boxed{E[X + Y] = E[X] + E[Y]}
$$

So there is not really a mysterious probability theorem hiding here.

It follows from ordinary arithmetic:

$$
a(b + c) = ab + ac
$$

and:

$$
\sum_i (a_i + b_i) = \sum_i a_i + \sum_i b_i
$$

Expectation inherits this structure because expectation itself is a weighted sum.

---

# 3. Scaling works for the same reason

Suppose $Z = aX$ where $a$ is a constant.

Then:

$$
E[aX] = \sum_i p_i (a X_i)
$$

Because $a$ is constant:

$$
E[aX] = a \sum_i p_i X_i
$$

Therefore:

$$
\boxed{E[aX] = a\,E[X]}
$$

Combine this with the addition property:

$$
\boxed{E[aX + bY] = a\,E[X] + b\,E[Y]}
$$

This is what we mean when we say **expectation is a linear operator**.

More generally:

$$
\boxed{E\!\left[\sum_i a_i X_i\right] = \sum_i a_i\,E[X_i]}
$$

---

# 4. The intuition: averaging before or after adding gives the same result

Forget probability for a moment.

Suppose $X = (1, 3, 5)$ and $Y = (10, 20, 30)$.

The average of $X$ is:

$$
\bar{X} = \frac{1 + 3 + 5}{3} = 3
$$

The average of $Y$ is:

$$
\bar{Y} = \frac{10 + 20 + 30}{3} = 20
$$

So $\bar{X} + \bar{Y} = 23$.

Now add the observations first: $X + Y = (11, 23, 35)$.

The average is $\frac{11 + 23 + 35}{3} = 23$.

Same answer.

So:

$$
\text{average}(X + Y) = \text{average}(X) + \text{average}(Y)
$$

Expectation is simply a **probability-weighted version of averaging**.

That is the main intuition.

---

# 5. Independence is not required

This is a very important point.

The result:

$$
E[X + Y] = E[X] + E[Y]
$$

holds whether $X$ and $Y$ are:

* independent,
* positively correlated,
* negatively correlated,
* perfectly correlated,
* or even literally the same random variable.

For example, suppose $Y = X$. Then:

$$
E[X + Y] = E[2X] = 2\,E[X]
$$

And:

$$
E[X] + E[Y] = E[X] + E[X] = 2\,E[X]
$$

So it still works.

## Why doesn't dependence matter?

Because expectation of a **sum** only requires us to add values state by state and average them.

Dependence matters when variables are **multiplied together**.

For example, $E[XY]$ generally does not equal $E[X]E[Y]$:

$$
\boxed{E[XY] \neq E[X]E[Y]}
$$

But under conditions such as independence:

$$
E[XY] = E[X]E[Y]
$$

So this distinction is worth remembering:

$$
\boxed{E[X + Y] = E[X] + E[Y] \quad \text{always}}
$$

whereas:

$$
\boxed{E[XY] = E[X]E[Y] \quad \text{not always}}
$$

---

# 6. Why this is so useful for portfolios

Suppose portfolio return is:

$$
r_p = w_1 r_1 + w_2 r_2 + \cdots + w_n r_n
$$

Take expectation:

$$
E[r_p] = E[w_1 r_1 + w_2 r_2 + \cdots + w_n r_n]
$$

Using linearity:

$$
E[r_p] = w_1 E[r_1] + w_2 E[r_2] + \cdots + w_n E[r_n]
$$

Therefore:

$$
\boxed{E[r_p] = \sum_i w_i\,E[r_i]}
$$

So the expected portfolio return is just the weighted average of the individual expected returns.

Notice what is **not** present: $\operatorname{Cov}(r_i, r_j)$.

There are no covariance terms in expected portfolio return.

Correlation between assets does not affect the algebra of expected return.

But it **does** affect portfolio variance.

---

# 7. Why covariance appears in variance but not expectation

Portfolio variance is:

$$
\operatorname{Var}(r_p) = E\!\left[\left(r_p - E[r_p]\right)^2\right]
$$

The important thing here is the square.

If $r_p = w_1 r_1 + w_2 r_2$, then squaring produces:

$$
(w_1 r_1 + w_2 r_2)^2
$$

which expands to:

$$
w_1^2 r_1^2 + 2 w_1 w_2 r_1 r_2 + w_2^2 r_2^2
$$

The cross-product $r_1 r_2$ is where the relationship between the variables becomes relevant.

That is why covariance appears:

$$
\operatorname{Var}(r_p) = \sum_i \sum_j w_i w_j \operatorname{Cov}(r_i, r_j)
$$

A useful mental distinction is:

> **Addition preserves linearity. Multiplication introduces interaction between variables.**

That is why expected return is simple while portfolio variance has covariance terms.

---

# 8. The deeper mathematical reason

For a continuous random variable, expectation can be thought of as an integral.

Very loosely:

$$
E[X] = \int X\,dP
$$

Therefore:

$$
E[aX + bY] = \int (aX + bY)\,dP
$$

Integration is itself linear:

$$
\int (aX + bY)\,dP = a \int X\,dP + b \int Y\,dP
$$

Therefore:

$$
\boxed{E[aX + bY] = a\,E[X] + b\,E[Y]}
$$

So at a deeper level:

$$
\boxed{\text{Expectation is linear because integration is linear}}
$$

But integration itself can be understood as the limiting version of a weighted sum.

So conceptually:

$$
\text{weighted sums} \rightarrow \text{integrals} \rightarrow \text{expectation}
$$

They all inherit the same linear structure.

---

# 9. A consequence you'll see everywhere

Consider the deviation of a random variable from its mean: $X - E[X]$.

What is its expectation?

Using linearity:

$$
E[X - E[X]] = E[X] - E[E[X]]
$$

But $E[X]$ is a constant. If $\mu = E[X]$, then:

$$
E[\mu] = \mu
$$

Therefore:

$$
E[X - E[X]] = E[X] - E[X] = 0
$$

So:

$$
\boxed{E[X - \mu] = 0}
$$

This is why deviations from the mean balance out in expectation.

That result ends up underneath variance, covariance, regression, portfolio mathematics, and many other statistical identities.

---

# 10. The mental model to keep

I would compress the whole idea to:

$$
\boxed{\text{Expectation} = \text{probability-weighted averaging}}
$$

And averaging respects addition and scaling.

So:

$$
\boxed{E[aX + bY] = a\,E[X] + b\,E[Y]}
$$

The key is that **you can either combine the random variables first and then average, or average them separately and then combine the averages**.

You get the same answer.

That property is exactly what we mean by **linearity of expectation**.

And this gives us the foundation for the covariance identity you were looking at:

$$
\sum_j w_j \operatorname{Cov}(r_i, r_j) = \operatorname{Cov}(r_i, r_p)
$$

because covariance inherits linearity from expectation.