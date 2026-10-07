Yes — your instinct is correct. **Volatility is not the same thing as risk.** It is a particular statistical summary of return dispersion that became extremely useful because it is mathematically convenient, estimable, and plugs neatly into portfolio construction.

And practitioners absolutely *have* decomposed it. Downside deviation, semivariance, expected shortfall, lower partial moments, drawdown measures, asymmetric volatility models, etc. all exist partly because of exactly the objection you're raising.

The interesting question is therefore not:

> "Why do professionals mistakenly think upside volatility is bad?"

It is more:

> **"Why is symmetric variance still such a useful primitive, despite being an imperfect model of investor risk?"**

## Start with a concrete example

Imagine two assets, both with average monthly return of $1\%$.

### Asset A

Its deviations from the mean are roughly:

$$
-2\%, -1\%, +1\%, +2\%
$$

Pretty symmetric.

### Asset B

Its deviations are more like:

$$
-1\%, -1\%, -1\%, +5\%
$$

Asset B has lots of small disappointments and occasional large upside jumps.

Variance sees **both positive and negative deviations**:

$$\n\operatorname{Var}(R) = E[(R-\mu)^2]\n$$

So that $+5\%$ upside surprise contributes heavily to measured volatility.

But suppose you're a long-only investor. You might reasonably say:

> "Why should a surprisingly good return count as risk?"

That's the central issue.

---

# 1. First small correction: volatility isn't expected squared deviation

Variance is:

$$
\sigma^2 = E[(R-\mu)^2]
$$

Volatility is its square root:

$$
\sigma = \sqrt{E[(R-\mu)^2]}
$$

where:

* $R$ = return,
* $\mu = E[R]$ = expected return,
* $\sigma^2$ = variance,
* $\sigma$ = volatility.

Your conceptual point remains unchanged, though.

The squaring means:

$$
(+10\%)^2=(-10\%)^2
$$

so variance deliberately discards the **direction** of the deviation.

---

# 2. Why did portfolio theory end up using variance?

A major reason is that variance solves a slightly different problem from the one you're imagining.

Modern portfolio theory isn't fundamentally saying:

> "Every upward movement is harmful."

It's saying:

> **"Returns are uncertain, and variance measures the scale of that uncertainty."**

That distinction matters.

Consider a pension fund expecting a portfolio to return $5\%$.

If it instead returns:

* $-15\%$, that's obviously problematic.
* $+25\%$, that's economically desirable.

But both outcomes tell you something about the **uncertainty of the return-generating process**.

Variance is measuring:

$$
\text{How far might realized returns move away from what I expect?}
$$

not necessarily:

$$
\text{How much economic pain might I experience?}
$$

Those are different concepts.

This gives us a useful mental model:

> **Volatility is primarily a measure of uncertainty, not a complete measure of investor harm.**

Sometimes uncertainty and risk align closely enough that volatility works well. Sometimes they don't.

---

# 3. Why symmetric volatility can nevertheless work surprisingly well

Suppose returns really were normally distributed:

$$
R \sim N(\mu,\sigma^2)
$$

The normal distribution is symmetric.

Knowing:

$$
\mu,\sigma
$$

completely specifies the distribution.

For example:

$$
P(R < \mu - 2\sigma)
$$

is approximately $2.3\%$.

So if downside and upside are structurally symmetric, measuring total dispersion indirectly tells you quite a lot about downside risk.

Higher:

$$
\sigma
$$

means:

* wider positive outcomes,
* **and wider negative outcomes**.

In that world, separating upside and downside provides relatively little additional information.

This is one reason variance-based frameworks are so elegant.

But financial returns aren't generally perfectly normal.

They exhibit:

* skewness,
* fat tails,
* volatility clustering,
* jumps,
* regime changes,
* asymmetric responses to shocks.

And that's exactly where your objection becomes much more important.

---

# 4. Your asymmetric example is real: two assets can have identical volatility but very different risk

Consider two return distributions.

### Strategy A

Most returns are modest, but occasionally:

$$
+30\%
$$

### Strategy B

Most returns are modest, but occasionally:

$$
-30\%
$$

They could potentially have:

$$
\sigma_A \approx \sigma_B
$$

while presenting completely different economic propositions.

Strategy A has **positive skew**.

Strategy B has **negative skew**.

Volatility compresses that difference away.

This matters enormously in real portfolios.

For example, strategies resembling:

* short-volatility strategies,
* carry strategies,
* credit,
* catastrophe insurance,
* certain relative-value strategies,

can exhibit:

$$
\text{small frequent gains} = +
\text{rare severe losses}
$$

Their volatility can look benign for long periods.

Meanwhile their true downside exposure can be substantial.

So the portfolio manager needs more information than $\sigma$.

---

# 5. Your idea already exists mathematically: semivariance

Instead of measuring deviations on both sides:

$$
E[(R-\mu)^2]
$$

we can measure only downside deviations.

For example:

$$
\text{Downside Semivariance} = E[\min(R-\mu,0)^2]
$$

Equivalently, conceptually:

```text
Return > mean
    ignore

Return < mean
    square downside deviation
```

Then:

$$
\text{Downside deviation} = \sqrt{\text{Downside Semivariance}}
$$

Now upside surprises contribute nothing to measured risk.

That aligns more closely with your intuition.

---

# 6. But even "below the mean" may not be what the investor actually cares about

There's another subtle problem.

Suppose the investor needs at least a $4\%$ return to meet liabilities.

Their concern isn't:

$$
R < E[R]
$$

Their concern is:

$$
R < 4\%
$$

This leads to the broader concept of a **lower partial moment**.

Define some target $T$.

Then:

$$\nLPM_n(T) = E[\max(T-R,0)^n]\n$$

For $n=2$:

$$\nLPM_2(T) = E[\max(T-R,0)^2]\n$$

This says:

> Measure the severity of outcomes below the investor's required threshold.

Now we've moved from a generic statistical definition of risk toward an **objective-aware definition of risk**.

That's much closer to how I think you should think about portfolio risk systems.

---

# 7. This connects directly to your wider interest in decision systems

Instead of asking:

> "What is portfolio risk?"

ask:

> **"What bad outcome is this investor trying to avoid?"**

For different investors, that's completely different.

A hedge fund might care about:

$$
P(\text{monthly loss} > 5\%)
$$

A pension scheme might care about:

$$
P(\text{assets}<\text{liabilities})
$$

A retiree might care about:

$$
P(\text{portfolio depletion before death})
$$

A leveraged strategy might care about:

$$
P(\text{margin call})
$$

A wealth-management client might care about:

$$
P(\text{drawdown}>20\%)
$$

Once you think this way, it becomes obvious why **no single scalar called "risk" can universally describe a portfolio**.

Volatility is simply one lens.

---

# 8. So why doesn't everyone just abandon volatility?

This is where the practical answer becomes important.

Because volatility has some extremely useful properties.

## A. It's easy to estimate

Given returns:

$$
r_1,r_2,\ldots,r_n
$$

you can estimate volatility straightforwardly.

More sophisticated downside quantities, particularly extreme-tail quantities, require much more data.

Suppose you care about a 99.9th-percentile loss.

That's roughly a:

$$
1/1000
$$

event.

With five years of daily data, you only have around:

$$
5\times252\approx1260
$$

observations.

There's very little empirical information about that tail.

Variance uses information from **every observation**.

That often makes it statistically more stable.

---

# 9. Variance interacts beautifully with portfolio mathematics

This is probably the strongest reason it remains fundamental.

For a portfolio:

$$
R_p = \sum_{i=1}^{n} w_iR_i
$$

variance is:

$$
\sigma_p^2 = w^\top\Sigma w
$$

where:

* $w$ = vector of portfolio weights,
* $\Sigma$ = covariance matrix.

For two assets:

$$
\sigma_p^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\sigma_1\sigma_2\rho_{12}
$$

That final term captures diversification.

This gives portfolio managers a very clean framework:

```text
individual asset risk
        +
co-movement between assets
        ↓
portfolio risk
```

And this is critical.

**Portfolio management isn't merely about asking how risky each asset is independently.**

It's about asking:

> What risk does this position contribute to the whole portfolio?

Variance/covariance makes this mathematically tractable.

---

# 10. This also produces one of the deepest ideas in portfolio management

An individually volatile asset can actually **reduce portfolio risk**.

Suppose Asset B has high standalone volatility but negative correlation with Asset A.

Adding B could lower:

$$
\sigma_p
$$

because:

$$
\operatorname{Cov}(A,B)<0
$$

That's why volatility shouldn't only be interpreted as:

> "How dangerous is this asset?"

A more useful interpretation is:

> **"How much uncertainty does this asset contribute conditional on everything else I own?"**

That leads naturally into:

* marginal risk contribution,
* component VaR,
* risk parity,
* covariance matrices,
* factor risk models.

Those are central tools in systematic portfolio construction.

---

# 11. Downside risk measures make portfolio optimisation harder

Suppose you replace variance with something like:

$$
P(R_p<T)
$$

Now the portfolio optimisation problem depends much more strongly on the **entire joint return distribution**.

You need to understand not just:

$$
\Sigma
$$

but potentially:

* skewness,
* kurtosis,
* tail dependence,
* nonlinear relationships,
* regime dependence.

That creates an estimation problem.

There is a general trade-off:

$$
\text{richer risk model}
\quad\leftrightarrow\quad
\text{more parameters to estimate}
$$

And every estimated parameter introduces error.

So a sophisticated risk measure may be conceptually superior but **operationally worse** if the inputs cannot be estimated reliably.

This is an important systematic-investing principle:

> **Model complexity should be judged against estimation error, not merely theoretical realism.**

---

# 12. There is another reason upside variance can matter

Upside variance isn't always irrelevant.

Imagine a liability-driven investor.

Suppose their portfolio unexpectedly rises $40\%$.

They may now:

* rebalance,
* de-risk,
* hedge newly created exposures,
* realize capital gains,
* alter asset allocation.

Extreme upside moves therefore still change the state of the portfolio.

Similarly, for an option portfolio, upside movement in the underlying can create enormous risk depending on:

* delta,
* gamma,
* vega,
* strike distribution.

So whether "up" means "good" depends heavily on the portfolio.

This relates directly to your options work.

For a short straddle:

$$
|\Delta S|\uparrow
$$

in **either direction** is dangerous.

There isn't meaningful "good upside volatility."

The relevant risk is magnitude of movement.

So symmetric volatility can be entirely appropriate.

---

# 13. This reveals something deeper: risk is position-dependent

Consider the same stock.

### Long investor

Large negative return:

bad.

Large positive return:

good.

### Short seller

Large negative return:

good.

Large positive return:

bad.

### Short straddle

Large negative return:

bad.

Large positive return:

bad.

### Long straddle

Large negative return:

good.

Large positive return:

good.

So the return distribution of the underlying isn't sufficient to define risk.

You need:

$$
\text{Market distribution} = +
\text{Position payoff} = +
\text{Investor objective}
$$

Then risk emerges from the combination.

That is a much stronger mental model than simply:

$$
\text{Risk}=\text{volatility}
$$

---

# 14. Practitioners therefore use a toolbox rather than a single measure

A mature risk system might include:

| Measure                  | What it answers                                             |
| ------------------------ | ----------------------------------------------------------- |
| Volatility               | How dispersed are returns?                                  |
| Downside deviation       | How variable are undesirable returns?                       |
| VaR                      | What loss threshold might be exceeded with probability $p$? |
| Expected Shortfall       | How bad are losses once we're in the tail?                  |
| Maximum drawdown         | How severe has peak-to-trough loss been?                    |
| Skewness                 | Is the distribution asymmetric?                             |
| Stress testing           | What happens under specific adverse scenarios?              |
| Scenario analysis        | What happens if particular risk factors move?               |
| Probability of shortfall | What's the probability of failing an objective?             |

You generally don't want:

$$
\boxed{\text{one risk number}}
$$

You want:

$$
\boxed{\text{a decision-relevant risk model}}
$$

---

# 15. This has an immediate implication for systematic portfolio tools

Suppose you're building a risk dashboard.

A weak design says:

```text
Portfolio volatility: 11.8%
```

A stronger one might say:

```text
Portfolio risk

Annualised volatility       11.8%
Downside deviation           7.1%
95% Expected Shortfall      -4.8%
1-year max drawdown         -9.6%
Probability of < 0 return   21%
```

But even that is just reporting.

A better **decision system** says:

```text
Objective
Avoid >10% portfolio drawdown.

Current probability
14%

Primary contributors
US equities              52%
Credit                   27%
EM equities              16%

Possible action
Reduce equity exposure 5%
Add defensive trend allocation

Estimated probability after rebalance
8%
```

Now risk measurement is actually serving a portfolio decision.

That's the direction I think is especially important for the systems you're interested in.

---

# 16. There is a beautiful connection here to options

Options are actually one way of **reshaping exactly the asymmetry you're talking about**.

Imagine equity returns:

```text
large downside     normal returns       large upside
      ↓                  ↓                   ↓
   painful              okay                good
```

Buy a protective put:

```text
large downside     normal returns       large upside
      ↓                  ↓                   ↓
    floored              okay                good
```

You've altered the return distribution.

Volatility alone may not fully capture the improvement.

The investor might happily accept:

$$
\sigma_{\text{new}} \approx \sigma_{\text{old}}
$$

if the new portfolio has:

$$
P(R<-20\%) \ll P_{\text{old}}(R<-20\%)
$$

That is one reason option-based portfolio construction gets so interesting.

You're not merely choosing **assets**.

You're designing the **shape of outcomes**.

---

# 17. The hierarchy I'd use mentally

Think of portfolio risk in four layers.

### Layer 1 — Dispersion

$$
\sigma
$$

"How uncertain are outcomes?"

Useful, simple, robust.

### Layer 2 — Distribution shape

Add:

$$
\text{skewness},\quad\text{kurtosis},\quad\text{downside deviation}
$$

"What kind of uncertainty?"

### Layer 3 — Tail outcomes

Use:

$$
VaR,\quad ES,\quad\text{stress scenarios}
$$

"What happens when things go badly?"

### Layer 4 — Investor objective

Ultimately:

$$
P(\text{failure})
$$

where failure might mean:

* insolvency,
* drawdown,
* missing a liability,
* breaching a mandate,
* failing to fund retirement.

This is ultimately the layer that matters.

---

## The key takeaway

Your intuition is essentially right:

$$
\boxed{\text{volatility}\neq\text{economic risk}}
$$

Volatility survives because it is a **very useful building block**:

* relatively easy to estimate,
* mathematically tractable,
* naturally incorporates covariance and diversification,
* useful when distributions are approximately symmetric,
* useful for measuring general uncertainty,
* and extremely convenient for optimisation.

But as soon as **distribution asymmetry matters to the investment objective**, variance alone is insufficient.

A more complete formulation is:

$$
\boxed{
\text{Risk} = f(
\text{return distribution},
\text{portfolio payoff},
\text{investment objective}
)
}
$$

That last formulation is especially important for systematic investing. It shifts the problem from **"calculate risk metrics"** to **"model the probability and severity of failing the client's objective."**

A very useful next hands-on project would be to take the **same two portfolios with identical annualised volatility but different skew**, then compare volatility, downside deviation, VaR, Expected Shortfall and drawdown. You'll see immediately which information each statistic preserves and which it destroys.
