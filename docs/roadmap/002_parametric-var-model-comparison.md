Yes — I think your pushback changes the recommendation.

My previous answer over-weighted **workflow coherence** and under-weighted the question:

> **What will make a technically strong hiring manager believe I can operate at the quantitative research / portfolio-risk boundary?**

For your situation, the answer is not simply “another report.”

# The career context changes the trade-off

You already have strong evidence of:

- software engineering;
- real-time systems;
- dealer and market-maker risk;
- multi-asset derivatives;
- production implementation;
- event-driven architecture;
- practical market knowledge.

Your likely perceived gaps are more on the buy-side side of the profile:

- statistical modelling of portfolio risk;
- portfolio construction and risk allocation;
- research methodology;
- model comparison and validation;
- working with changing market regimes;
- understanding how model choice affects portfolio decisions.

The career documents explicitly identify gaps around:

- signal research and backtesting;
- portfolio construction;
- research infrastructure;
- factor and premia modelling.

So the project should not merely demonstrate that you can build a clean workflow. It also needs to demonstrate that you can make and defend a **quantitative modelling choice**.

On that basis, a technically substantive parametric-risk slice has more value than I previously gave it.

---

# But “implement parametric VaR” is not enough

There is an important distinction between:

> **Add parametric VaR as another calculator**

and:

> **Investigate whether a different risk model would change the portfolio-monitoring decision**

The first risks becoming a methods checklist:

```text
Historical VaR ✓
Parametric VaR ✓
Monte Carlo VaR later ✓
```

That does not necessarily signal strong research ability.

The second is a proper quantitative investigation:

> **When portfolio risk is changing, does the choice between historical and parametric estimation change whether the PM should investigate?**

That gives you:

- a decision;
- competing model assumptions;
- implementation;
- empirical comparison;
- validation;
- regime analysis;
- model-risk discussion;
- a portfolio-management consequence.

That is much stronger technically and still fits the project’s decision-first philosophy.

---

# Revised comparison

| Question | Change-over-time first | Parametric model comparison first |
|---|---:|---:|
| Demonstrates workflow awareness | **High** | High if decision-linked |
| Demonstrates quantitative modelling | Medium | **High** |
| Demonstrates statistical understanding | Low–medium | **High** |
| Demonstrates model assumptions | Low | **High** |
| Demonstrates validation/research | Medium | **High** |
| Adds something not already present | Medium | **High** |
| Risk of looking like reporting glue | **Medium–high** | Low if properly scoped |
| Risk of becoming method collection | Low | Medium |
| Uses current covariance attribution work | Medium | **High** |
| Improves technical interview discussion | Medium | **High** |
| Directly advances the workflow | **High** | Medium–high |

The key point is that the project already has:

- a Risk Snapshot;
- historical VaR;
- point-in-time attribution;
- the beginnings of a Change Report concept.

Therefore, building the temporal report next would advance the workflow, but some of that work may be **integration and presentation** rather than a major new demonstration of technical ability.

Parametric modelling would add a genuinely new quantitative layer.

---

# Why parametric VaR is especially relevant here

There is already a methodological tension in the project:

- the Snapshot headline uses **historical VaR**;
- Attribution uses **covariance-based structural volatility**.

Your current attribution implementation calculates component contributions from the covariance matrix. The attribution design explicitly states that it does not decompose the historical VaR headline.

Introducing parametric VaR creates a more coherent technical story:

```text
Returns
    ↓
Covariance estimate
    ↓
Portfolio volatility
    ↓
Parametric VaR
    ↓
Component risk contribution
```

Now the portfolio-level risk number and its component contributions arise from the same model family.

That allows you to explain:

- what the covariance matrix estimates;
- why portfolio volatility depends on covariances, not just individual volatilities;
- how component contributions reconcile to total volatility;
- what normality assumes;
- how historical and parametric estimates differ;
- when the two methods disagree;
- which decision should be trusted, and why.

That is a much better technical interview surface than simply saying that you added a Change Report.

---

# The right scope: not basic parametric VaR

I would not recommend implementing a basic one-off normal VaR formula and declaring victory.

That is too standard:

```text
VaR = z × portfolio volatility
```

The technically credible version should be:

## Model comparison under historical market conditions

Compare at least:

1. **Historical VaR**
   - empirical quantile;
   - no distributional assumption;
   - sensitive to observations entering and leaving the window.

2. **Static parametric VaR**
   - covariance estimated from a rolling window;
   - normal-distribution assumption;
   - transparent and analytically attributable.

Optionally, later:

3. **Exponentially weighted parametric VaR**
   - more weight on recent observations;
   - responds faster to changing volatility;
   - introduces a decay parameter that needs justification.

The first two may be enough for the slice. EWMA could be a controlled extension if the comparison exposes a meaningful responsiveness problem.

---

# The decision-first framing

The artifact should answer:

> **Which risk estimate should support the PM’s investigation decision when the portfolio enters a changing market environment?**

The investigation is not trying to prove that one method is universally superior.

It should ask:

- Do historical and parametric VaR flag the same dates?
- Which method reacts faster to a volatility regime change?
- Which method produces more false investigation events?
- When do they disagree?
- Does the disagreement matter for the PM’s decision?
- Does the parametric model provide a more coherent risk attribution?
- What assumptions explain the difference?

The output could look like:

```text
Date: 14 March 2022

Historical VaR:   2.18%    91st percentile
Parametric VaR:   1.74%    72nd percentile

Historical model: INVESTIGATE
Parametric model: NO ACTION

Reason for disagreement:
The recent return distribution contains losses that are more extreme
than implied by the rolling normal covariance model.

Decision implication:
The model choice changes the investigation route. Historical VaR
provides a more conservative signal in this episode, but the result
does not establish that it is generally superior.
```

That is a much stronger case study than either:

> “Parametric VaR is more sophisticated”

or:

> “The portfolio’s risk increased over time.”

---

# Technical work this would require

A credible implementation would include:

## Model calculation

- rolling covariance estimation;
- portfolio volatility;
- normal quantile;
- parametric VaR;
- component volatility contributions;
- numerical reconciliation checks.

## Methodological decisions

- whether to include the sample mean;
- covariance degrees-of-freedom convention;
- rolling estimation window;
- treatment of missing observations;
- annualisation;
- confidence level;
- sign convention.

## Validation

- compare realised returns against each model’s VaR;
- calculate exception rates;
- examine clustered exceptions;
- inspect behaviour during calm and stressed periods;
- test synthetic portfolios with known covariance structures.

## Research analysis

- identify dates where the models disagree;
- classify disagreement by market environment;
- inspect volatility, correlation, and tail-shape changes;
- determine whether the difference changes the `investigate / no action` result.

That is technical, empirical, and decision-relevant.

---

# Where the temporal slice fits

I would not abandon change-over-time. I would change its role.

Instead of building:

```text
Snapshot
    ↓
Change Report
```

as the next standalone artifact, build:

```text
Historical VaR
        ┐
        ├──→ Model Comparison Over Time
Parametric VaR
        ┘
```

Then the temporal dimension becomes essential to the model comparison.

You are no longer just asking:

> “What changed between two dates?”

You are asking:

> “How did competing risk models behave as the portfolio moved through different market conditions?”

That gives you both signals:

```text
Technical signal:
I can implement, validate, and compare portfolio-risk models.

Workflow signal:
I understand how model disagreement affects a PM’s investigation decision.
```

The Change Report can then be the next artifact generated from the model-comparison work.

---

# Revised recommendation

I would now prioritise:

> **A decision-first comparison of historical and parametric portfolio VaR across a selected historical market episode, including model validation and the effect on the investigation decision.**

Not:

> **A standalone parametric VaR calculator.**

And not initially:

> **A standalone descriptive Change Report.**

The proposed scope would be:

```text
One portfolio
Two risk models
One rolling estimation framework
One historical episode
Model validation
Selected disagreement dates
Risk attribution under the parametric model
Investigation decision comparison
One research-style write-up
```

Explicitly defer:

- Monte Carlo;
- GARCH;
- factor models;
- dynamic portfolio weights;
- optimisation;
- trade recommendations;
- multiple portfolios;
- production framework work.

---

# The stronger hiring story

The temporal-report story is:

> “I built a workflow that compares portfolio risk across dates and explains how risk contributions changed.”

That is good.

The model-comparison story is:

> “I compared empirical and parametric portfolio-risk estimates across a historical market episode, validated their behaviour, investigated where they disagreed, and assessed how model choice changed the portfolio manager’s decision to investigate. I also used the covariance model to produce a reconciled asset-level risk attribution.”

That story demonstrates:

- quantitative implementation;
- statistical assumptions;
- portfolio mathematics;
- research discipline;
- empirical validation;
- model risk;
- investment workflow awareness;
- clear communication.

That is closer to the complete profile you need.

## Bottom line

Your pushback is correct.

Given your existing profile, **workflow awareness alone is not enough**. The next slice should create visible technical evidence, but the technical work must remain tied to a real decision.

So I would revise the decision to:

> **Build parametric VaR as a model-comparison and model-risk investigation, using historical replay to determine whether the choice of risk model changes the PM’s investigation decision.**

Then use the resulting time-series comparison to build the Change Report.

That sequencing better addresses both sides of your career transition:

```text
Dealer-side strength:
I can build real-time risk and trading systems.

Buy-side capability to prove:
I can evaluate portfolio-risk models,
understand their assumptions and failure modes,
and connect them to investment decisions.
``` 
