# The minimum credible CV version

Your principle is exactly right:

> **Don’t lower quality to move faster. Lower scope until you can move fast at the required quality.**

The key is defining what “required quality” means.

For this project, required quality is **not**:

- production-grade infrastructure;
- a complete portfolio platform;
- multiple VaR methodologies;
- a dashboard;
- automated alerts;
- a full historical operating history;
- optimised rebalancing;
- every possible risk measure.

Required quality is:

> **A hiring manager can see a real investment-management decision, understand how your system supported it, inspect credible evidence, and believe you understand both the quantitative method and its limitations.**

That means the minimum viable flagship should be a **complete case-study vertical slice**, not a miniature platform.

---

# My recommendation: V1-Micro

The fastest credible version is:

> **One multi-asset portfolio, one risk methodology, one investigation workflow, one historical market episode, and one well-evidenced decision-support case study.**

The workflow is:

```text
Portfolio data
    ↓
Historical VaR snapshot
    ↓
Investigation trigger
    ↓
Asset-level risk attribution
    ↓
PM-style investigation memo
```

That is enough to signal:

- interest in systematic investment management;
- multi-asset portfolio understanding;
- quantitative risk knowledge;
- ability to build research tooling;
- ability to connect analysis to decisions;
- awareness of model limitations;
- ability to communicate with investment professionals.

It is much smaller than the full V1 previously defined.

---

# The minimum user story

## User

A multi-asset portfolio manager.

## Decision

> **The portfolio’s risk appears unusually high. Should I investigate it, and what appears to be driving the change?**

## Portfolio

Use the existing four-asset portfolio:

| Asset | Proxy | Weight |
|---|---:|---:|
| US equities | SPY | 40% |
| International equities | EFA | 20% |
| US Treasuries | IEF | 25% |
| Gold | GLD | 15% |

Do not add more assets.

Four assets are enough to demonstrate:

- equity concentration;
- diversification;
- cross-asset interaction;
- risk contribution;
- portfolio-level thinking.

## Method

Use only:

- historical VaR;
- a 252-day rolling window;
- 95% confidence;
- positive loss convention;
- fixed portfolio weights;
- daily returns.

Do not implement parametric or Monte Carlo VaR for this version.

---

# The minimum outputs

I would reduce the deliverables to **four externally visible outputs**.

## Output 1: Working portfolio risk calculation

This is the code and tests underneath the visible work.

It must be able to:

- load or receive the four asset return series;
- construct portfolio returns;
- calculate historical VaR for a selected date;
- calculate the portfolio’s rolling VaR history;
- calculate percentile rank or an equivalent “unusual risk” measure;
- determine `investigate` or `no action`;
- reproduce the same result from the same inputs.

This does not need to be a reusable library with elaborate abstractions.

It does need to be inspectable and tested.

### Minimum quality bar

- core calculations have tests;
- no look-ahead in the selected case;
- assumptions are explicit;
- missing or insufficient data fails clearly;
- numerical outputs can be reproduced.

---

## Output 2: One Risk Snapshot

This is the first visible artifact.

It should answer:

> **What risk is the portfolio taking at this point in time, and does it require attention?**

Minimum contents:

- date;
- portfolio;
- NAV;
- daily VaR;
- annualised VaR;
- risk budget;
- budget utilisation;
- percentile rank;
- `investigate` or `no action`;
- one paragraph of plain-language interpretation.

This is largely what you already have.

Do not expand the snapshot unnecessarily. It is a triage artifact, not the full investigation.

---

## Output 3: One Attribution and Investigation Report

This can be one combined artifact rather than separate Change Report and Attribution Report.

It should answer:

> **Why did the portfolio require investigation, and where does the risk appear to come from?**

Minimum contents:

1. What triggered the investigation?
2. What was the current VaR?
3. What was the comparison VaR?
4. How large was the change?
5. What were the asset-level risk contributions?
6. Which assets contributed most?
7. What changed in volatility, correlation, or portfolio composition?
8. What does the evidence suggest?
9. What can the analysis not establish?

For example:

```text
The portfolio entered the investigation state because its VaR
rose above the 90th percentile of its trailing history.

The increase was concentrated in equity risk. SPY and EFA
accounted for most of the portfolio's risk contribution, while
the diversification benefit from IEF was weaker than usual.

This supports further PM investigation. It does not, by itself,
establish that equities should be sold or identify an optimal
replacement allocation.
```

That single report demonstrates much more than two disconnected technical outputs.

---

## Output 4: One Historical Case Study

This is the piece that makes the project CV-worthy rather than merely interesting.

Choose **one** historical episode where the system produces a meaningful investigation.

The case study should contain:

```text
Market environment
    ↓
Portfolio state
    ↓
System output
    ↓
Investigation trigger
    ↓
Attribution
    ↓
Hypothetical PM interpretation
    ↓
Limitations
    ↓
What the system should do next
```

You do not need three to five case studies for the minimum version.

One strong case study is enough to establish the concept.

Choose a period where the portfolio behaviour is genuinely interesting, such as:

- an equity selloff;
- a period of rising rates;
- an inflation shock;
- a period where equities and bonds became less diversifying;
- a period where risk rose but the right response was not obviously “sell.”

The last option may be the most intellectually valuable because it shows that your system supports judgment rather than mechanically prescribing trades.

---

# The minimum documentation package

The four outputs above need to be packaged into three short documents.

## 1. README

The README should explain:

- the investment decision;
- the portfolio;
- the workflow;
- the outputs;
- the main finding;
- the limitations;
- what is deliberately out of scope.

The first paragraph should not begin with Python, architecture, or package structure.

It should begin with the investment problem.

For example:

> This project demonstrates a portfolio-risk monitoring workflow for a four-asset multi-asset portfolio. It uses rolling historical VaR and asset-level risk attribution to identify when portfolio risk requires investigation and to help explain the sources of change. The system is operated through a historical market episode to test whether its outputs support a plausible portfolio-management decision.

## 2. Methodology note

This should document only the methods used in the case study:

- data source;
- return construction;
- portfolio weights;
- historical VaR;
- lookback window;
- confidence level;
- percentile calculation;
- attribution method;
- point-in-time treatment;
- limitations.

It does not need to teach all of portfolio risk.

It needs to make your specific result defensible.

## 3. Historical investigation memo

This is the main investor-facing artifact.

It should read like a short internal risk note, not like a software tutorial.

The structure could be:

```text
# Portfolio Risk Investigation: [Date / Episode]

## Executive conclusion

## Portfolio and market context

## What the system observed

## Why investigation was triggered

## Risk attribution

## Interpretation

## Hypothetical PM decision

## What the system does not tell us

## Lessons for the workflow
```

That memo is likely to be more valuable in an interview than another 500 lines of code.

---

# The minimum definition of done

I would define V1-Micro as complete when all of these are true.

## Scope

- [ ] One four-asset portfolio is documented.
- [ ] One historical VaR methodology is used.
- [ ] One historical episode is selected.
- [ ] One PM investigation decision is defined.

## Implementation

- [ ] Portfolio returns are generated reproducibly.
- [ ] Point-in-time historical VaR works for a selected date.
- [ ] Risk budget or unusual-risk detection works.
- [ ] Asset-level risk attribution works.
- [ ] Core numerical logic has tests.
- [ ] No look-ahead is used in the case study.

## Evidence

- [ ] A Risk Snapshot is produced.
- [ ] An Investigation and Attribution Report is produced.
- [ ] The historical case study shows the actual outputs.
- [ ] The case study records a hypothetical PM interpretation.
- [ ] At least one limitation or ambiguity is discussed honestly.

## Presentation

- [ ] The README explains the decision workflow.
- [ ] The methodology is documented.
- [ ] The result is understandable without reading the code.
- [ ] The project can be explained in two minutes.
- [ ] The CV bullet can be written without exaggeration.

When these boxes are checked, stop.

That is the important part.

---

# What you are explicitly not building

To prevent scope expansion, V1-Micro should have hard exclusions:

```text
No:
- second VaR methodology
- second portfolio
- factor attribution
- trade recommendation
- portfolio optimiser
- dashboard
- live monitoring
- automated alerts
- transaction costs
- performance attribution
- multiple historical episodes
- deployment
- generic framework abstractions
```

The rule should be:

> **If it does not improve the credibility of this one investigation case, it is not V1-Micro work.**

---

# Why one case study is enough initially

You might worry that one historical case is too little.

It would be too little if you were claiming:

> “This system has been validated across market regimes.”

You are not claiming that.

You are claiming:

> “I built a narrow decision-support workflow and operated it through one historical episode to examine whether it provided useful evidence for a portfolio investigation.”

That is a proportionate claim.

One case study can demonstrate the entire chain:

```text
method
→ implementation
→ portfolio context
→ trigger
→ attribution
→ interpretation
→ limitations
```

A second and third case study improve the project later, but they are not required to establish the initial signal.

---

# The likely shortest path from where you are now

Based on the current project state, I would sequence the remaining work like this.

## Step 1 — Freeze the V1-Micro contract

Write down:

```text
One portfolio
One method
One investigation
One historical episode
One investor-facing memo
```

Do not begin new methodology work after this point.

## Step 2 — Finish the existing snapshot

Your current snapshot already has most of the required structure:

- historical VaR;
- budget utilisation;
- percentile rank;
- plain-language interpretation;
- investigate/no-action decision.

Bring that to a stable, tested state.

## Step 3 — Add the smallest useful attribution

Implement asset-level attribution for the existing four-asset portfolio.

Do not build factor attribution.

Do not build a general attribution framework.

Make the method explicit and test it on simple synthetic examples.

## Step 4 — Select the historical episode

Choose the episode based on the output, not in advance based on what sounds impressive.

Run the system across enough dates to find a case where:

- investigation is triggered;
- attribution is interpretable;
- the market context is understandable;
- the conclusion is not trivial.

## Step 5 — Write the investigation memo

This is the highest-value artifact.

Use the actual system outputs. Do not write a hypothetical report before seeing the evidence.

## Step 6 — Package and stop

Update:

- README;
- methodology note;
- investigation memo;
- CV bullet.

Then call it V1.

---

# The quality threshold

The project is ready for the CV when a hiring manager can answer “yes” to these questions:

| Hiring-manager question | Evidence required |
|---|---|
| Does he understand portfolio risk? | Multi-asset portfolio and risk context |
| Can he implement quantitative methods? | Working VaR and attribution code |
| Does he understand how the output is used? | Investigation decision and PM-oriented artifacts |
| Can he reason beyond a number? | Interpretation and attribution |
| Does he understand model risk? | Explicit limitations |
| Has he operated the system rather than just designed it? | Historical case study |
| Can he communicate with investment professionals? | Clear investigation memo |
| Is the scope credible? | Explicit non-goals and no exaggerated claims |

If the answer is yes, the project has done its job.

---

# The core distinction

There are two possible minimums.

## Too small

```text
Notebook calculating VaR for SPY, EFA, IEF, and GLD
```

This shows interest and some technical ability, but not enough workflow understanding.

## Correct minimum

```text
A tested, point-in-time multi-asset risk calculation
that identifies an investigation event, attributes the risk,
and produces a PM-style historical investigation memo.
```

That is the smallest version I would trust as a flagship CV project.

# Bottom line

Your V1 should not be:

> **“A complete portfolio risk-monitoring platform.”**

It should be:

> **“One complete, credible portfolio-risk investigation workflow.”**

The finish line is:

```text
Risk Snapshot
    ↓
Investigation Trigger
    ↓
Asset Attribution
    ↓
Historical Investigation Memo
```

With:

- one portfolio;
- one methodology;
- one historical episode;
- tested calculations;
- honest limitations;
- clear documentation.

That is the scope reduction I would make.

It preserves the required quality while removing almost everything that would turn this into a long-running platform project.
