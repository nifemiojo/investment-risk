For **historical VaR**, there are several legitimate decomposition approaches, and they answer slightly different questions.

The key constraint is this:

$$
\text{VaR}_\alpha
$$

under historical simulation is an **empirical quantile**, so unlike parametric VaR it is not naturally a smooth function of portfolio weights. That makes decomposition less canonical.

## The main options

| Method                                  | Core question                                                                       | Main strength                                | Main weakness                                        |
| --------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------- | ---------------------------------------------------- |
| **VaR-scenario attribution**            | What positions caused the loss on the scenario that defines VaR?                    | Very intuitive                               | Depends heavily on one scenario                      |
| **Marginal VaR via finite differences** | How does VaR change if I slightly change one position?                              | Decision-relevant                            | Can be unstable around quantile switches             |
| **Component VaR from marginal VaR**     | How much of current VaR can be attributed to each position?                         | Gives an additive-style decomposition        | Sensitive to estimation method                       |
| **Incremental VaR**                     | What happens if I remove or resize a position?                                      | Very actionable                              | Contributions do not generally add to total VaR      |
| **Conditional/tail attribution**        | What does each asset contribute across bad portfolio scenarios?                     | More stable than single-scenario attribution | Moves toward Expected Shortfall rather than pure VaR |
| **Shapley allocation**                  | How should total VaR be fairly allocated across positions considering interactions? | Handles diversification/interactions well    | Computationally expensive                            |

Let’s walk through each.

---

# 1. VaR-scenario attribution

Suppose you have daily historical returns for $T$ days.

Portfolio P&L under historical scenario $t$ is:

$$
L_t = -\sum_{i=1}^{N} x_i\, r_{i,t}
$$

where:

* $x_i$ = exposure to asset $i$
* $r_{i,t}$ = historical return of asset $i$ on scenario $t$
* $L_t$ = portfolio loss

Sort all portfolio losses.

Suppose the 99% VaR is determined by scenario $t^*$:

$$
\text{VaR}_{99} = L_{t^*}
$$

Then because portfolio P&L is additive:

$$
L_{t^*} = \sum_i L_{i,t^*}
$$

you can simply say:

$$
\boxed{\text{VaR}_i^{\text{scenario}} = L_{i,t^*}}
$$

### Example

Portfolio VaR:

$$
\text{£1m}
$$

On the VaR scenario:

| Asset       |      P&L |
| ----------- | -------: |
| US equities |   -£600k |
| EM equities |   -£300k |
| Treasuries  |   +£100k |
| Credit      |   -£200k |
| Total       | **-£1m** |

So you get an exact decomposition:

$$
600 + 300 - 100 + 200 = 1000
$$

### Interpretation

> “On the historical scenario currently defining the 99% VaR, US equities generated 60% of the loss.”

Very interpretable.

But importantly:

$$
\boxed{\text{scenario attribution} \neq \text{general risk contribution}}
$$

because another nearby scenario may have a completely different composition.

---

# 2. Finite-difference marginal VaR

This is closer to the economic idea of risk contribution.

Start with:

$$
\text{VaR}(\mathbf{x})
$$

Then perturb one exposure:

$$
x_i \rightarrow x_i + \epsilon
$$

and recalculate the **entire historical VaR**.

Approximate:

$$
\text{MVaR}_i \approx \frac{\text{VaR}(\mathbf{x} + \epsilon\, e_i) - \text{VaR}(\mathbf{x})}{\epsilon}
$$

where $e_i$ changes only asset $i$.

### Example

Current portfolio:

$$
\text{VaR} = \text{£1,000,000}
$$

Increase Asset A from £10m to £10.1m:

$$
\text{VaR} = \text{£1,006,000}
$$

Then:

$$
\text{MVaR}_A \approx \frac{6{,}000}{100{,}000} = 0.06
$$

Interpretation:

> Around the current portfolio, another £1 of Asset A exposure adds about 6p of VaR.

### Why this captures diversification

Because you aren't calculating Asset A independently.

You are rerunning:

$$
\text{VaR}(\text{whole portfolio})
$$

with Asset A slightly changed.

So its relationship with every other asset is automatically reflected in the historical scenarios.

---

# 3. Component VaR from marginal VaR

Once you've estimated marginal VaR, you can form:

$$
\text{CVaR}_i = x_i \, \text{MVaR}_i
$$

This attempts to answer:

> “How much of current portfolio VaR can we attribute to position $i$?”

Under smooth homogeneous VaR functions, Euler's theorem gives:

$$
\text{VaR}_P = \sum_i \text{CVaR}_i
$$

Historical VaR complicates this because the empirical quantile isn't smoothly differentiable everywhere.

So a practical implementation may produce:

$$
\sum_i \text{CVaR}_i \approx \text{VaR}_P
$$

rather than exactly.

That means you need to be careful about claiming an exact additive decomposition unless your chosen estimator guarantees it.

---

# 4. Incremental VaR

This is probably the most useful one for rebalancing.

Instead of asking about an infinitesimal change, ask about an actual proposed change.

For removing a position:

$$
\text{IVaR}_i = \text{VaR}(P) - \text{VaR}(P_{-i})
$$

More generally for some trade $\Delta x_i$:

$$
\text{IVaR}_i(\Delta x_i) = \text{VaR}(\mathbf{x} + \Delta x_i e_i) - \text{VaR}(\mathbf{x})
$$

### Example

Current portfolio:

$$
\text{VaR} = \text{£1.0m}
$$

Remove Asset A:

$$
\text{VaR} = \text{£820k}
$$

Then Asset A's incremental effect is:

$$
\text{£1.0m} - \text{£820k} = \text{£180k}
$$

So:

> Removing Asset A reduces portfolio VaR by £180k.

Now suppose removing Treasuries gives:

$$
\text{VaR}(P - \text{Treasuries}) = \text{£1.1m}
$$

Then:

$$
\text{IVaR}_{\text{Treasuries}} = \text{£1.0m} - \text{£1.1m} = -\text{£100k}
$$

Meaning Treasuries currently reduce portfolio VaR by about £100k.

That is extremely useful information for a PM.

---

# But incremental VaRs don't add

This is important.

Suppose:

$$
\text{IVaR}_A = \text{£180k}
$$

and:

$$
\text{IVaR}_B = \text{£300k}
$$

You cannot generally conclude:

$$
A + B = \text{£480k}
$$

of portfolio VaR.

Why?

Because diversification effects overlap.

Removing A changes B's relationship to the remaining portfolio.

So:

$$
\text{VaR}(P) - \text{VaR}(P_{-A})
$$

and:

$$
\text{VaR}(P) - \text{VaR}(P_{-B})
$$

are both **counterfactual portfolio comparisons**, not slices of an additive pie.

This distinction is fundamental:

> Component VaR is primarily an **allocation** concept.

> Incremental VaR is primarily a **decision-impact** concept.

---

# 5. Conditional attribution around the VaR boundary

Instead of relying on exactly one VaR observation, you can examine several scenarios around the quantile.

Suppose your 99% quantile falls around observations 9–11.

You might average asset P&Ls across:

$$
t \in \{t_8, t_9, t_{10}, t_{11}, t_{12}\}
$$

or apply kernel weights so scenarios closest to the VaR threshold receive more weight.

Conceptually:

$$
\text{Contribution}_i = \sum_t w_t L_{i,t}
$$

where:

$$
\sum_t w_t = 1
$$

and $w_t$ is concentrated near the VaR boundary.

This is sometimes useful because raw historical VaR has a nasty problem:

> A single observation can determine the decomposition.

Smoothing produces a more stable estimate.

But now you are making an additional modelling choice:

* how many scenarios?
* what bandwidth?
* what kernel?
* symmetrical around VaR or only worse than VaR?

So the result becomes estimator-dependent.

---

# 6. Tail attribution / Expected Shortfall-style contribution

If your actual objective is understanding:

> “What positions create losses when the portfolio is in trouble?”

then I'd seriously consider not decomposing VaR itself.

Instead take all scenarios worse than VaR.

Suppose:

$$
\mathcal{T} = \{ t : L_t \geq \text{VaR}_{99} \}
$$

Then asset $i$'s tail contribution could be:

$$
C_i = \frac{1}{|\mathcal{T}|} \sum_{t \in \mathcal{T}} L_{i,t}
$$

And because:

$$
L_t = \sum_i L_{i,t}
$$

you get:

$$
\text{ES} = \sum_i C_i
$$

under a straightforward historical ES calculation.

This gives a clean interpretation:

> “Across the portfolio's worst 1% of historical scenarios, emerging-market equities contribute an average £320k of loss.”

This is generally much more robust than:

> “EM contributed £210k on the one historical observation defining VaR.”

---

# 7. Shapley-value VaR attribution

This is conceptually very interesting.

Suppose you have three assets:

$$
A, B, C
$$

Portfolio VaR reflects not only individual risks but also **interactions**:

$$
\text{diversification effects}
$$

The question becomes:

> How should those interaction effects be allocated fairly?

Shapley values come from cooperative game theory.

For every possible ordering in which assets could be added to the portfolio, calculate the marginal contribution of an asset when it joins.

Then average across all orderings.

Conceptually:

$$
\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(N-|S|-1)!}{N!} \left[ \text{VaR}(S \cup \{i\}) - \text{VaR}(S) \right]
$$

You don't need to memorise that formula.

The intuition is much simpler:

> Measure Asset A's incremental VaR in every possible portfolio context, then average it.

This handles the fact that:

$$
\text{Contribution}(A)
$$

depends on what else is already in the portfolio.

And Shapley allocations satisfy:

$$
\sum_i \phi_i = \text{VaR}(P) - \text{VaR}(\emptyset)
$$

so you get an additive allocation.

### Downside

For $N$ positions, exact calculation requires evaluating:

$$
2^N
$$

portfolio subsets.

That's impossible for large portfolios.

You therefore use Monte Carlo sampling of permutations.

For a 5–20 asset research portfolio, though, it's a very interesting method to implement.

---

# What I'd actually expose to a PM

I wouldn't select one decomposition and pretend it contains the whole truth.

I'd separate **three different views**.

## A. Historical scenario attribution

```text
99% VaR: £1.0m
Defining scenario: 16-Mar-2020

US Equity        £600k
EM Equity        £300k
Credit           £200k
Treasuries      -£100k
```

Question answered:

> What happened in this VaR scenario?

---

## B. Risk contribution

```text
Estimated historical component VaR

US Equity        £480k
EM Equity        £280k
Credit           £170k
Treasuries        £70k
```

Question:

> Which positions are structurally contributing to our estimated VaR?

Here you need to disclose how it was estimated.

---

## C. Rebalancing impact

```text
Trade                    New VaR    ΔVaR

Sell £2m US Equity       £840k     -£160k
Sell £2m EM Equity       £900k     -£100k
Sell £2m Treasuries      £1.08m    +£80k
Buy £2m Treasuries       £930k     -£70k
```

Question:

> What can I actually do about the risk?

For a PM workflow, this third one is probably the most operationally useful.

---

# A useful hierarchy

I'd think of the methods like this:

$$
\boxed{\text{Scenario attribution}}
$$

answers **what happened?**

$$
\boxed{\text{Marginal/component VaR}}
$$

answers **what is driving risk locally?**

$$
\boxed{\text{Incremental VaR}}
$$

answers **what happens if I trade?**

$$
\boxed{\text{Tail / ES attribution}}
$$

answers **what drives losses across severe scenarios?**

$$
\boxed{\text{Shapley attribution}}
$$

answers **how should total risk and diversification effects be allocated fairly?**

There isn't one universally correct historical-VaR decomposition because you're asking different economic questions.

For the kind of rebalancing decision system you're building, I'd implement **scenario attribution + incremental VaR first**, then add marginal/component VaR. Those first two are easier to explain to a PM and directly connect the risk measure to actual portfolio decisions.
