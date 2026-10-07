Yes — that is a good refined mental model, with one important qualification: **volatility and VaR are related but not interchangeable views of portfolio risk**.

## 1. Both describe uncertainty in portfolio returns

### Portfolio volatility

Volatility asks:

> How widely do portfolio returns tend to vary around their average?

It is a measure of the overall dispersion of returns. For a portfolio, it reflects:

- each asset’s own volatility;
- the portfolio weights;
- correlations and covariances between assets.

So portfolio volatility is fundamentally a **distribution-wide, structural measure**.

### VaR

VaR asks:

> At a specified confidence level and horizon, how large a loss might we expect not to exceed under the chosen model or historical sample?

For example:

> One-day 95% VaR is £1 million.

This means that, under the chosen methodology, approximately 5% of one-day outcomes are expected to be worse than a £1 million loss. It does **not** mean that £1 million is the maximum possible loss.

VaR is therefore a **threshold or quantile measure**, focused on a particular part of the loss distribution.

The full definition needs at least:

- confidence level, such as 95% or 99%;
- horizon, such as one day or ten days;
- methodology, such as historical, parametric, or Monte Carlo;
- portfolio valuation and scenario conventions.

So “the portfolio’s VaR” is incomplete unless those conventions are known.

## 2. The relationship between them

Under a simple normal-return model, VaR can be expressed using volatility:

$$
\text{VaR} \approx z_\alpha \times \sigma_p \times V
$$

where:

- $\sigma_p$ is portfolio volatility;
- $V$ is portfolio value;
- $z_\alpha$ is the relevant normal-distribution tail multiplier for the chosen confidence level.

Under that model, higher volatility generally produces higher VaR.

But this relationship is not universal. Historical or simulation-based VaR also depends on:

- skewness;
- fat tails;
- volatility clustering;
- changing correlations;
- the particular historical scenarios in the window.

Two portfolios can have similar volatility but different VaR because their tails differ. Conversely, VaR can change because the historical window changes even when the portfolio’s structural covariance relationships have barely changed.

So a useful summary is:

> **Volatility describes the scale of typical variation across the distribution. VaR describes a selected loss boundary in the distribution.**

## 3. Both can support attribution, but the meaning differs

Your statement that both can be decomposed and attributed is directionally right, but the decomposition methods are not identical.

### Volatility attribution

Volatility has a clean structural decomposition based on covariance.

For asset $i$, its component contribution to portfolio volatility is:

$$
\text{Component Volatility}_i
=
\frac{w_i \operatorname{Cov}(r_i,r_p)}{\sigma_p}
$$

where:

- $w_i$ is the asset’s portfolio weight;
- $r_i$ is the asset return;
- $r_p$ is the portfolio return;
- $\operatorname{Cov}(r_i,r_p)$ measures how the asset co-moves with the portfolio;
- $\sigma_p$ is portfolio volatility.

These contributions sum exactly to portfolio volatility.

This answers:

> Where does the portfolio’s current structural risk live?

It naturally captures diversification. An asset can have a **negative contribution** if it reduces overall portfolio risk.

For example, bonds may have positive standalone volatility but a negative contribution to a multi-asset portfolio if they tend to offset equity risk.

### VaR attribution

VaR is a quantile, so it does not have the same universally clean additive decomposition.

For **parametric VaR**, if VaR is a fixed multiple of volatility, then component VaR can be derived from component volatility:

$$
\text{Component VaR}_i
=
z_\alpha \times
\text{Component Volatility}_i
\times V
$$

That is a model-based decomposition and inherits the assumptions of the parametric model.

For **historical VaR**, the VaR threshold is based on observed portfolio losses. A simple breakdown of the loss on the VaR scenario can tell you:

> What made up that particular observed loss?

If the portfolio lost 2% on the VaR day, then the asset-level contributions to that day’s loss are simply the weighted asset returns on that day.

But that is not necessarily the same as:

> Where does the portfolio’s general tail risk structurally come from?

The VaR scenario may be unusual, and the identity of the VaR scenario can change when the historical window rolls forward.

So for historical VaR, it is useful to distinguish:

- **structural risk contribution**: covariance-based volatility contribution;
- **VaR-scenario loss composition**: what made up the selected historical loss;
- **tail composition**: what assets contributed across several tail observations.

Those answer different questions.

## 4. Attribution of the current level versus attribution of change

There is another useful distinction in your formulation.

### Current-state attribution

This asks:

> Why is the current risk measure at this level?

For volatility, component contributions answer this directly.

For VaR, the answer depends on the methodology. You might examine:

- parametric component VaR;
- the historical scenarios near the VaR boundary;
- the composition of losses across the tail;
- portfolio weights and covariance structure.

### Change attribution

This asks:

> Why did the risk measure change between two dates?

For volatility, you might compare changes in:

- portfolio weights;
- individual asset volatilities;
- correlations;
- the covariance estimation window;
- portfolio value.

For historical VaR, it is particularly important to separate:

1. **weight effect** — what would VaR have been if only the portfolio weights had changed?
2. **window effect** — what would VaR have been if only the historical scenario window had changed?
3. potentially, an interaction effect depending on the bridge methodology.

A simple counterfactual bridge is:

```text
V00 = VaR(previous weights, previous scenario window)
V10 = VaR(current weights,  previous scenario window)
V11 = VaR(current weights,  current scenario window)

weight effect = V10 - V00
window effect = V11 - V10
total change  = V11 - V00
```

This lets you say something defensible such as:

> VaR increased mainly because the portfolio weights changed, holding the previous scenario window constant.

That is stronger than saying:

> VaR increased because bonds became riskier,

unless you have actually isolated that effect.

## A compact mental model

I would phrase your model like this:

> **Portfolio volatility and VaR are headline measures of portfolio risk. Volatility measures the scale of return dispersion across the distribution, while VaR measures a specified loss quantile under a stated methodology. Both can be analysed cross-sectionally to understand what drives the current level and longitudinally to understand what drove a change. However, volatility has a clean covariance-based component decomposition, whereas VaR decomposition is methodology-dependent. Historical VaR should usually be analysed through scenario and tail composition, rather than treated as if it had a universally additive asset-level decomposition.**

And in terms of the decision workflow:

| Question | Most suitable view |
|---|---|
| How much structural risk does the portfolio carry? | Portfolio volatility |
| Where does current structural risk live? | Component volatility contribution |
| How large might a specified tail loss be? | VaR |
| What made up one observed bad day? | Scenario loss contribution |
| What is happening across the tail? | Tail composition |
| Why did historical VaR change? | Weight/window counterfactual bridge |
| What happens if we change a position? | Marginal risk or proposed-trade analysis |

The central idea is that **“attribution” does not mean one universal calculation**. It means decomposing a particular risk question in a way that matches the mathematical nature of the headline measure and the investment decision being supported.
