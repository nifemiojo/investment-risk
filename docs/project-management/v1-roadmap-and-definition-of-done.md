# Yes — the real task is to define a bounded V1

The project currently has a strong **long-term constitution**, but that is not the same thing as a V1 scope.

The constitution describes the eventual flagship:

```text
Monitor → Detect → Diagnose → Decide → Rebalance → Evaluate
```

That is the direction of travel.

V1 should not attempt to complete that entire chain. It should deliver one **credible, operated vertical slice** that demonstrates the most important career transition:

> **I can connect portfolio-risk measurement to an investment-management decision.**

My recommendation is:

# V1: Portfolio Risk Monitoring → Investigation Decision

V1 should answer:

> **When a multi-asset portfolio’s risk changes, can the system tell a portfolio manager whether to investigate, explain what changed, and provide enough evidence to form a view about what to do next?**

That is enough to be worthy of the CV.

It is also bounded enough to finish.

---

# What V1 should prove

V1 should prove four things:

| Capability | Evidence |
|---|---|
| **Portfolio risk measurement** | Reproducible historical VaR for a multi-asset portfolio |
| **Risk monitoring** | Point-in-time risk snapshots with budget and historical context |
| **Risk diagnosis** | Change analysis and asset-level risk attribution |
| **Investment workflow thinking** | Historical replay showing what was flagged, why, and what decision followed |

This gives you a strong career signal without pretending to have built a complete asset-management platform.

The central story becomes:

> **I built and operated a portfolio risk-monitoring workflow across a historical period. It identified periods requiring investigation, explained the sources of risk change, and produced decision-support artifacts that demonstrated where the analysis was useful and where its limitations mattered.**

That is a complete story.

---

# What should not be part of V1

The following should remain outside V1:

- parametric VaR;
- Monte Carlo VaR;
- factor attribution;
- multiple portfolios;
- live data feeds;
- interactive dashboards;
- automated alerts;
- production deployment;
- transaction-cost modelling;
- expected-return forecasts;
- full portfolio optimisation;
- automated trade recommendations;
- client-facing reporting;
- sophisticated regime classification;
- performance attribution;
- dynamic asset allocation.

These are not bad ideas. They are simply not necessary to establish the initial career signal.

Most importantly, **rebalance recommendations should be V2**, not V1.

The reason is conceptual: a risk snapshot can establish that the PM should investigate. Attribution can help explain why. But recommending a specific trade requires additional assumptions about:

- expected returns;
- constraints;
- turnover;
- liquidity;
- transaction costs;
- mandate;
- tax;
- implementation timing;
- acceptable tracking error.

If V1 recommends trades without modelling those things properly, it risks looking like a toy optimiser.

V1 should deliberately stop at:

> **“Investigate this portfolio, here is what appears to have changed, and here are the limitations of the evidence.”**

That is intellectually defensible.

---

# V1’s precise user story

## Primary user

A systematic or multi-asset portfolio manager.

## Portfolio

Keep the portfolio deliberately small:

| Asset | Proxy | Weight | Role |
|---|---:|---:|---|
| US equities | SPY | 40% | Growth |
| International equities | EFA | 20% | Equity diversification |
| US Treasuries | IEF | 25% | Duration and deflation hedge |
| Gold | GLD | 15% | Inflation and crisis diversification |

Portfolio assumptions:

- £10 million NAV;
- daily observations;
- historical VaR;
- 95% confidence;
- 252-day rolling window;
- positive loss convention;
- fixed initial weights for V1;
- point-in-time calculations with no look-ahead.

The exact portfolio is less important than keeping it:

- genuinely multi-asset;
- simple enough to understand;
- rich enough for diversification and attribution to matter.

## Primary decision

> **Should the PM investigate this portfolio today, or move on?**

## Secondary question

If investigation is required:

> **What changed, and which assets or risk relationships appear to be responsible?**

That is the full V1 decision scope.

---

# V1 workflow

```text
Historical market data
        ↓
Portfolio return series
        ↓
Point-in-time VaR
        ↓
Risk budget and historical context
        ↓
Investigate / no action
        ↓
Risk-change analysis
        ↓
Asset-level attribution
        ↓
Historical decision record
```

Notice what this does not include:

```text
        ↓
Automatic sell recommendation
        ↓
Optimised portfolio
        ↓
Trade execution
```

Those belong later.

---

# The V1 deliverables

V1 should produce five visible deliverables.

## 1. A working risk engine

This is the implementation foundation.

It should support:

- portfolio construction from asset returns;
- historical VaR;
- rolling VaR history;
- annualisation;
- risk-budget comparison;
- percentile ranking;
- point-in-time calculation;
- deterministic configuration.

The engine should be reusable by notebooks and report generation, but the architecture should remain modest. You do not need to build a general-purpose framework.

The existing `RiskSnapshotEngine`, `RiskSnapshot`, and renderer are already moving in the right direction.

## 2. Daily Risk Snapshot

This is the triage artifact.

It should answer:

> **What risk is the portfolio taking today, and does it require attention?**

Minimum content:

- portfolio and date;
- NAV;
- daily VaR in currency and percentage terms;
- annualised VaR;
- risk budget;
- budget utilisation;
- breach status;
- historical percentile rank;
- plain-language interpretation;
- `investigate` or `no action` decision.

The existing snapshot work is already close to this.

The important design choice you made is correct:

> The snapshot routes attention. It does not prescribe a trade.

## 3. Risk Change Report

This is the next artifact after investigation.

It should answer:

> **What changed relative to the previous relevant observation?**

Minimum content:

- current VaR versus comparison VaR;
- absolute and percentage change;
- change relative to normal historical changes;
- whether the change is gradual or abrupt;
- whether the change is driven by portfolio returns, volatility, correlation, or weights;
- a plain-language interpretation;
- limitations of the diagnosis.

You do not need a perfect causal decomposition.

You need to give the PM a defensible first hypothesis.

For example:

```text
Portfolio VaR increased materially over the observation period.

The increase appears to be associated primarily with:
1. higher equity volatility;
2. weaker diversification between equities and bonds;
3. a larger equity contribution to portfolio risk.

The analysis does not establish that one mechanism caused the entire change.
```

That is much better than presenting a false level of precision.

## 4. Asset-level Risk Attribution

This should answer:

> **Where does the portfolio’s risk come from?**

For V1, asset-level attribution is sufficient.

You do not need factor attribution.

A useful output might show:

| Asset | Portfolio weight | Risk contribution | Contribution share |
|---|---:|---:|---:|
| SPY | 40% | ... | ... |
| EFA | 20% | ... | ... |
| IEF | 25% | ... | ... |
| GLD | 15% | ... | ... |

The artifact should communicate something like:

> Equities represent 60% of capital but account for 78% of portfolio risk.

That is actionable portfolio thinking.

The attribution method must be explicit. If you use leave-one-out or incremental VaR, document:

- what is removed;
- what is held constant;
- whether contributions reconcile;
- why the result should be interpreted as an attribution rather than an exact decomposition;
- what the method cannot tell the PM.

This is an important credibility point.

## 5. Historical Replay and Decision Journal

This is what turns the repository into a flagship project.

Without historical replay, you have built a system.

With historical replay, you demonstrate that you can **operate and evaluate** the system.

The replay should:

- run the system point-in-time over a defined historical period;
- generate snapshots;
- identify investigation events;
- generate change and attribution outputs for selected events;
- record what the system saw;
- record the decision you would have made;
- review what happened afterwards;
- record what the system got right and wrong.

You do not need to write a detailed report for every day.

The sensible pattern is:

```text
All days:
    Generate machine-readable risk snapshots

Selected days:
    Produce full investigation artifacts and decision memos
```

I would aim for **three to five historical case studies**, not hundreds.

Possible environments to investigate include:

- an equity-led stress period;
- a rates and inflation shock;
- a period where traditional diversification weakened;
- a period where VaR rose but no intervention would have been justified;
- a false positive where the system flagged unusual risk that subsequently normalised.

The last two are particularly important. A good monitoring system is not judged only by whether it finds dramatic crises. It is also judged by whether it creates unnecessary noise.

---

# The V1 definition of done

V1 is done when all of the following are true.

## A. Scope and assumptions

- [ ] The portfolio, assets, weights, NAV, currency, and risk budget are documented.
- [ ] Historical VaR methodology is documented.
- [ ] Confidence level and rolling window are fixed and explicit.
- [ ] Annualisation convention is explained.
- [ ] Positive-loss sign convention is documented.
- [ ] Data source and data limitations are documented.
- [ ] The point-in-time/no-look-ahead rule is documented.

## B. Risk engine

- [ ] The four-asset portfolio return series can be generated reproducibly.
- [ ] Point-in-time VaR can be calculated for any valid date.
- [ ] Rolling VaR history can be calculated.
- [ ] Annualised VaR is compared against the risk budget.
- [ ] Percentile rank is calculated against a defined historical distribution.
- [ ] The engine produces an explicit `investigate` or `no action` result.
- [ ] Core calculations have automated tests.
- [ ] Edge cases are handled deliberately, including insufficient history and missing data.

## C. Primary artifacts

- [ ] A Daily Risk Snapshot can be generated for a chosen date.
- [ ] A Risk Change Report can be generated for an investigation date.
- [ ] An Asset Risk Attribution report can be generated for an investigation date.
- [ ] Each artifact states who uses it, when it is used, and what decision it supports.
- [ ] Each artifact includes plain-language interpretation.
- [ ] Each artifact states its limitations.
- [ ] The artifacts are understandable without reading the implementation.

## D. Historical replay

- [ ] The system is replayed across a defined historical period.
- [ ] Every observation is calculated using only information available at that date.
- [ ] Investigation events are recorded.
- [ ] At least three historical episodes are selected for deeper analysis.
- [ ] At least one false positive or ambiguous case is discussed.
- [ ] The system’s behaviour is reviewed across different market environments.

## E. Decision journal

For each selected case:

- [ ] The market context is described.
- [ ] The portfolio state is described.
- [ ] The system output is shown.
- [ ] The investigation trigger is explained.
- [ ] The risk-change diagnosis is shown.
- [ ] The attribution result is shown.
- [ ] A hypothetical PM decision is recorded.
- [ ] Subsequent outcomes are reviewed.
- [ ] The system’s limitations are discussed.
- [ ] A lesson for the system is recorded.

## F. Career-facing presentation

- [ ] The project can be explained in one paragraph.
- [ ] The repository has a clear README.
- [ ] The README leads with the investment decision, not the code architecture.
- [ ] At least three representative outputs are easy to find.
- [ ] There is a concise methodology note.
- [ ] There is a concise historical case-study write-up.
- [ ] The project makes clear what is simulated and what is real.
- [ ] The CV can describe the project without overstating its claims.
- [ ] A hiring manager can understand the career relevance in under two minutes.

That is a substantial V1.

It is not a toy, but it is not an endless platform.

---

# A sensible roadmap from where you are now

## Phase 0 — Reset the scope

### Goal

Turn the existing project constitution and earlier plan into one agreed V1 contract.

### Decisions to lock

- V1 ends at investigation and diagnosis.
- Rebalance recommendations are deferred to V2.
- The primary portfolio is SPY/EFA/IEF/GLD.
- The primary artifact chain is Snapshot → Change Report → Attribution.
- Historical replay is part of V1, not an optional extra.
- The final output is a small set of case studies, not a production dashboard.

### Completion test

You should be able to write:

> “V1 is complete when I can run this four-asset portfolio through a historical period, identify when risk requires investigation, explain the main sources of change, and present three decision records showing what a PM would have known and decided.”

If that sentence is stable, Phase 0 is complete.

---

## Phase 1 — Finish the portfolio-level foundation

### Goal

Make the existing risk snapshot a reliable and reproducible primitive.

### Work

- finalise portfolio construction;
- finalise data loading;
- confirm point-in-time behaviour;
- confirm rolling VaR;
- confirm annualisation;
- confirm risk-budget treatment;
- strengthen tests;
- generate snapshots for selected dates.

### Output

A working Risk Snapshot for any valid date.

### Stop condition

Do not keep expanding the snapshot once it answers:

> **Should I investigate this portfolio today?**

Additional information should go into downstream artifacts.

---

## Phase 2 — Complete the investigation path

### Goal

Build the next artifact after an investigation trigger.

### Work

- define the comparison period;
- calculate VaR changes;
- describe change magnitude and speed;
- identify volatility and correlation context;
- distinguish observed facts from interpretation;
- render a Risk Change Report.

### Output

A report that answers:

> **What changed since the last meaningful observation?**

### Stop condition

The report does not need to explain every basis point. It needs to provide a useful, honest diagnostic hypothesis.

---

## Phase 3 — Complete asset-level attribution

### Goal

Show where risk is located in the portfolio.

### Work

- settle the V1 attribution method;
- implement asset-level contributions;
- test behaviour on synthetic portfolios;
- check interpretation in the multi-asset portfolio;
- document reconciliation and limitations;
- render the attribution artifact.

### Output

A report that answers:

> **Which assets are responsible for the portfolio’s current risk and its recent change?**

### Stop condition

Do not move to factor attribution. Asset-level attribution is enough for V1.

---

## Phase 4 — Operate the system historically

### Goal

Convert the system from a codebase into evidence.

### Work

- select the replay period;
- run point-in-time snapshots;
- identify investigation events;
- classify event types;
- choose three to five cases;
- generate full artifacts for those cases;
- record hypothetical decisions;
- review subsequent outcomes.

### Output

A historical replay dataset plus decision journal.

### Stop condition

You have enough evidence to answer:

- Did the system flag genuinely interesting periods?
- Did it create too many false positives?
- Did attribution help explain the change?
- Were there cases where the model was misleading?
- What information was missing?

---

## Phase 5 — Package the flagship

### Goal

Make the work legible to someone outside the project.

### Work

- rewrite the README around the investment workflow;
- add a system overview;
- add the V1 definition of done;
- add representative outputs;
- add the historical case studies;
- add a limitations section;
- add a clear “what I would build next” section;
- prepare the CV bullet;
- prepare a five-minute interview walkthrough.

### Output

A finished V1 that can be shown, discussed, and defended.

---

# What the CV version should communicate

The CV should not say:

> Built a portfolio risk platform with VaR, attribution, dashboards, rebalancing, and alerts.

That sounds broad, generic, and probably overstated.

A stronger version would be closer to:

> **Built and historically operated a multi-asset portfolio risk-monitoring workflow using rolling historical VaR, risk-budget monitoring, change detection, and asset-level risk attribution; produced decision-support reports showing when a portfolio manager should investigate changing risk and evaluated the system across multiple market environments.**

That tells the reader:

- what you built;
- what methods you used;
- who it was for;
- what decision it supported;
- how you validated it;
- why it matters.

---

# The most important scope decision

Do not define “done” as:

> “The system has every capability in the long-term architecture.”

Define “done” as:

> **“The system supports one complete and credible investment decision workflow, and I have operated it enough to understand both its value and its limitations.”**

That is the right threshold.

A project becomes flagship-worthy through **coherence and evidence**, not feature count.

Your V1 does not need to be a complete investment-management system. It needs to be a convincing demonstration that you can move through this chain:

```text
Quantitative model
    ↓
Portfolio context
    ↓
Decision trigger
    ↓
Risk diagnosis
    ↓
Human interpretation
    ↓
Historical evaluation
```

That is the bridge between your existing identity as a quantitative developer and the identity you want recruiters to see: a quant research engineer who understands how investment systems support real portfolio decisions.

## Bottom line

I would set the V1 finish line at:

> **Snapshot → Investigation Trigger → Change Report → Asset Attribution → Historical Replay → Decision Journal**

Then stop, package it, put it on the CV, and only afterwards decide whether the next investment of time should be:

- rebalance recommendations;
- factor attribution;
- performance attribution;
- a signal/research component;
- or a different project entirely.

That stopping rule is important. V1 should be a **finished flagship slice**, not the first unfinished chapter of a five-year platform.
