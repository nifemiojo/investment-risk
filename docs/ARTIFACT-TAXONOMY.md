# Artifact Taxonomy: Organising By Question, Not By Timeframe

**Status**: Mental model — guides how we think about outputs  
**Date**: 2026-08-02

---

## Core Principle

> An artifact answers a question. Timeframe is an attribute of an instance, not the artifact type itself.

"Daily Risk Brief" conflates artifact type with frequency. Attribution appears in both daily and monthly outputs — it's the same artifact type, just different instances. Organizing by timeframe jumbles unrelated analyses together and scatters related analyses across multiple documents.

The three independent dimensions:

```
                    Artifact Type
                    (what question it answers)
                         │
                         │
        Frequency ───────┼─────── Audience
        (how often)      │       (who reads it)
                         │
```

An "Attribution Report" is an artifact type. "Daily Attribution" and "Monthly Attribution" are instances of the same type with different lookback windows — same structure, different data range.

---

## The Artifact Types

### 1. Risk Snapshot

> *"What risk is the portfolio taking right now?"*

| Field | Type |
|---|---|
| VaR (£, % of NAV) | Number |
| Budget utilisation (% of limit) | Number + threshold flag (breach Y/N) |
| Percentile rank in historical VaR distribution | Number |
| Percentile meaning (prose: "about average" / "worth a look" / "investigate" / "escalate") | Text |
| Plain-language summary | Text (2-3 sentences) |

Point-in-time. The "when" is a parameter. Could be intraday, daily, weekly — same structure. This is the most basic artifact. Everything else builds on it.

### 2. Change Report

> *"What changed between point A and point B?"*

| Field | Type |
|---|---|
| VaR delta (£, %, z-score) | Number + significance label |
| Attribution delta — which assets drove the change | Per-asset breakdown |
| Correlation shifts — which pairs moved | Pairwise breakdown |
| Plain-language explanation of the driver | Text |

The "between point A and point B" is a parameter: yesterday vs. today, last week vs. this week, last month vs. this month. Same structure, different window.

### 3. Attribution

> *"Where is the risk coming from?"*

| Field | Type |
|---|---|
| Per-asset contribution (£, % of total VaR) | Asset-level breakdown |
| Standalone VaR per asset | Number per asset |
| Diversification benefit (standalone sum − portfolio VaR) | Number |
| Diversification ratio | Number + trend label ("rising", "falling", "stable") |
| Concentration: % of risk in top N assets, % per asset class | Summary stats |

A decomposition of one Risk Snapshot into its sources. The "when" is a parameter.

### 4. Drift Analysis

> *"How has the risk allocation shifted from target?"*

| Field | Type |
|---|---|
| Per-asset target risk contribution vs. actual | Asset-level comparison |
| Drift amount and direction | Number + flag ("reduce", "add", "hold") |
| Overall concentration vs. target | Summary stat |
| Trend: how drift has evolved over recent periods | Direction + magnitude |

Compares the current Attribution to the Portfolio's `risk_allocation_target`. This is the artifact that feeds directly into the rebalance decision. It's the bridge between measurement and action.

### 5. Rebalance Recommendation

> *"Should we rebalance? If so, how?"*

| Field | Type |
|---|---|
| Should rebalance? (Y/N) | Boolean |
| Proposed trades: which assets, direction (buy/sell), amount (£) | Per-asset trade list |
| Rationale: why the system recommends this | Text |
| Counterargument: the case for not acting | Text |
| Historical context: what happened in similar situations | Text |

Takes Drift Analysis as input. Produces a specific, actionable trade list. The PM accepts or overrides. This is the artifact where the system stops diagnosing and starts prescribing.

### 6. Decision Record

> *"What was decided and why?"*

| Field | Type |
|---|---|
| Decision (rebalance / let ride / partial) | Enum |
| PM rationale | Text |
| Date and timestamp | Timestamp |
| Outcome (filled at next review) | Link to next period's Drift Analysis |
| Did risk return to target? | Boolean (filled later) |
| Notes | Text |

This is a log entry, not a report. It captures the human decision for audit, learning, and the Decision Journal meta-artifact. The system proposes; the PM decides; the Decision Record captures what happened and what happened next.

### 7. Diversification Monitor

> *"Is diversification breaking down?"*

| Field | Type |
|---|---|
| Diversification ratio trend over lookback period | Number + chart data |
| Correlation matrix shifts: which pairs are converging/diverging | Pairwise breakdown |
| Regime label for each shifting pair | Text |
| Implication for the portfolio | Text |
| Historical analogues: when has this happened before? | Text |

Triggered by threshold crossing, not by schedule. The Diversification Monitor is event-driven — it fires when the diversification ratio crosses below (or above) a threshold. It answers the question the PM didn't know to ask.

### 8. Scenario Impact

> *"What would [historical crisis] do to this portfolio?"*

| Field | Type |
|---|---|
| Scenario name, date, description | Text |
| Projected portfolio loss (£, %, peak-to-trough) | Numbers |
| Recovery duration (trading days to breakeven) | Number |
| Breakdown: projected loss per asset | Per-asset numbers |
| Comparison to risk budget: utilisation under scenario | Number + flag |
| Historical context: what actually happened in that period | Text |

On-demand or quarterly. Could be run against a library of scenarios (2008, 2011, 2015, 2018 Q4, 2020 COVID, 2022 rates). Uses current portfolio weights applied to historical crisis returns.

---

## How They Compose

Artifacts are not a flat list. They form a dependency graph:

```
Risk Snapshot ──→ Change Report
       │              (delta between two snapshots)
       │
       └──────→ Attribution
                     (decomposes snapshot into sources)
                     │
                     ├──────→ Diversification Monitor
                     │           (triggered when attribution
                     │            shows diversification weakening)
                     │
                     └──────→ Drift Analysis
                                   (compares attribution to target)
                                   │
                                   └──────→ Rebalance Recommendation
                                                 (trades, rationale,
                                                  counterargument)
                                                 │
                                                 └──────→ Decision Record
                                                              (PM decides,
                                                               outcome tracked)
                                                              │
                                                              └──→ feeds historical
                                                                   context into next
                                                                   Rebalance Recommendation

Scenario Impact ←── on demand
    (uses current portfolio weights + historical crisis returns)
```

The composition IS the workflow. Each artifact is a node in the graph. Timeframe is a parameter on the edges — how often does this flow run?

---

## Composition vs. Artifact

What we previously called the "Daily Risk Brief" is a **composition** of Snapshot + Change + Attribution at a daily frequency, rendered for the PM.

What we called the "Monthly Risk Review" is a **composition** of Snapshot + Drift Analysis + Rebalance Recommendation at a monthly frequency, rendered for the PM.

Neither is a distinct artifact type. They're assemblies of the same underlying artifact types, composed at different frequencies and with different subsets of the full graph.

This means:
- The engine produces individual artifact types (dataclasses)
- The composition happens at the edge (notebook, orchestrator, cron job)
- A "daily notebook" calls: snapshot engine, change engine, attribution engine — and renders all three
- A "monthly notebook" additionally calls: drift engine, rebalance engine
- Same engines, different composition. No engine knows about "daily" or "monthly"

---

## Rendering Is Orthogonal

Each artifact type produces a structured dataclass. Rendering is a completely separate concern:

```
RiskSnapshot dataclass
    │
    ├── render_risk_snapshot_markdown()    → notebook cell, cron email
    ├── render_risk_snapshot_terminal()    → CLI output
    ├── render_risk_snapshot_streamlit()   → dashboard tile
    └── render_risk_snapshot_html()        → web app component
```

Same dataclass. Four renderers. The artifact is the concept — the dataclass is the contract. The renderer is whichever UI consumes it.

---

## What This Means for the Architecture

Each artifact type maps to one engine module and one domain dataclass:

```
src/domain/                         src/engine/
├── risk_snapshot.py     ←──        ├── risk_snapshot_engine.py
├── change_report.py     ←──        ├── change_report_engine.py
├── attribution.py       ←──        ├── attribution_engine.py
├── drift.py             ←──        ├── drift_analysis_engine.py
├── rebalance.py         ←──        ├── rebalance_engine.py
├── diversification.py   ←──        ├── diversification_engine.py
└── scenario.py          ←──        └── scenario_engine.py
```

One module, one concept, one dataclass. No module does two things. No "daily_brief()" that jumbles everything.

---

## Design Heuristics

| Heuristic | Rationale |
|---|---|
| If an artifact type appears in multiple compositions, it's a first-class type | Don't duplicate attribution logic in daily and monthly flows. One engine, call it twice. |
| If an artifact can be produced at different frequencies with the same structure, frequency is a parameter | Snapshot(day=2022-03-31) and Snapshot(day=2022-03-25) are the same type. |
| If you're tempted to name something "Daily X" or "Monthly Y", you're naming the composition, not the artifact | Name the underlying artifact types. Compose at the edge. |
| Each artifact type answers exactly one question | "What risk?" ≠ "What changed?" ≠ "Where from?" ≠ "Should I act?" — these are separate artifacts. |
| The engine produces data, not prose | "Plain-language summary" is a text field on the dataclass, not a separate artifact. The interpretation engine fills it in. The renderer decides how it's displayed. |

---

## V1 Scope: Which Artifacts?

| Artifact | V1? | Rationale |
|---|---|---|
| Risk Snapshot | ✓ | Foundation. Everything builds on it. |
| Change Report | ✓ | The "investigate?" trigger. |
| Attribution | ✓ | The "where from?" answer. Makes the portfolio transparent. |
| Drift Analysis | ✓ | Feeds the rebalance decision. The action driver. |
| Rebalance Recommendation | ✓ | The action. The thing the PM decides on. |
| Decision Record | ✓ | Closes the loop. Enables the Decision Journal meta-artifact. |
| Diversification Monitor | Defer | Event-driven, needs threshold calibration. V1 has the diversification ratio inside Attribution — enough signal for now. |
| Scenario Impact | Defer | Needs scenario data library. V1 focuses on monitoring → action loop. |