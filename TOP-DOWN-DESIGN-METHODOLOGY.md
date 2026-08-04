# Vertical Slice Design Methodology

**Status**: Active practice  
**Date**: 2026-08-02

---

## Principle

> Start from the outputs and work backward. The artifacts define the contract. The domain model and engine exist to serve them.

Every vertical slice begins with the same sequence:

```
1. Design the artifact(s)
       │
       ▼
2. Annotate every field → what domain concept does it represent?
       │
       ▼
3. Extract the domain objects from the annotations
       │
       ▼
4. Define relationships between objects
       │
       ▼
5. Derive the engine API (functions that produce these objects)
       │
       ▼
6. Implement engine modules to the API
       │
       ▼
7. Build thin display layer (notebook cells as consumers)
```

Steps 1–5 are design. Steps 6–7 are implementation. Design always precedes implementation. The design output is the spec the implementation must meet.

---

## Why This Order

| If you start from code | If you start from artifacts |
|---|---|
| You build an engine and then figure out what to display. The display ends up warped around whatever the engine happened to produce. | The artifact tells you exactly what the engine must compute. No wasted computation. No missing fields. |
| You design domain objects based on what's easy to model. | You design domain objects based on what the user (PM) needs to see and decide. |
| The API is whatever the implementation produced. | The API is derived from the artifact contract. |
| "I built a VaR calculator. What should I show?" | "Here's what the PM needs. What must I compute?" |

The artifact is the user story. It's the one thing that doesn't change — the PM's decision is always the same. How you compute the numbers might change (historical → parametric → Monte Carlo), but the artifact structure is stable.

---

## Step 1: Design the Artifact(s)

Draw the output as it would appear to the PM. Use mock data. Be specific — every number, every label, every sentence.

For each artifact, answer:
- **Who sees this?** (PM, Risk, IC, Client)
- **When?** (Daily, Monthly, Quarterly, On breach)
- **What decision does it enable?** (Investigate? Rebalance? Escalate? Communicate?)
- **What action follows?** (If yes → do X. If no → do Y.)

If you can't name a specific decision the artifact enables, the artifact is information, not decision support. Reconsider whether it earns its place.

---

## Step 2: Annotate Every Field

Go through the artifact line by line. For each piece of data, ask: what domain concept does this represent?

```
╔══════════════════════════════════════════════════════════════╗
║  VaR TODAY                                                   ║
║  £218,400 (2.18% of NAV)                    ← VaRResult     ║
║  vs. Risk Budget: ████████░░ 82% utilised    ← RiskBudget    ║
║                                                              ║
║  CHANGE                                                      ║
║  +£32,100 since last month (+17.2%)          ← VaRChange    ║
║  This change is +1.6σ above normal range     ← VaRChange    ║
║  ⚠ NOTABLE                                   ← Flag         ║
╚══════════════════════════════════════════════════════════════╝
```

Every field gets a domain concept label. If two fields share a concept, they belong on the same object. If a field introduces a new concept, it might be a new object or a new attribute.

---

## Step 3: Extract Domain Objects

Group the annotations into objects. Name them after what they ARE, not what produced them.

| Annotation label | Object | Reason |
|---|---|---|
| VaRResult (on £, %, utilisation) | `VaRResult` | All these describe a single VaR measurement |
| VaRChange (on amount, %, z-score) | `VaRChange` | All these describe change between two measurements |
| Flag (on NOTABLE) | `VaRResult.flags` or separate `Flag` type | Could be an attribute or a rich object — depends on complexity |
| RiskBudget (on limit, utilisation bar) | `RiskBudget` | Separate from VaRResult — the budget exists before the measurement |

Objects that appear across multiple artifacts are shared domain concepts. `VaRResult` appears in both the Daily Brief and the Monthly Review — it's a first-class domain object, not an artifact-specific view.

---

## Step 4: Define Relationships

Map how objects connect:

```
Portfolio (1)
  │
  ├── defines ──→ RiskBudget (1)
  │
  └── produces ──→ VaRResult (many, one per day)
                      │
                      ├── compared to previous ──→ VaRChange
                      │
                      └── decomposed into ──→ Attribution
                                                  │
                                                  └── compared to target ──→ RiskDrift
                                                                                  │
                                                                                  └── drives ──→ RebalanceRecommendation
                                                                                                  │
                                                                                                  └── answered by ──→ Decision
```

Cardinality matters: `1` vs. `many`. Direction matters: `produces` vs. `is compared to`. These relationships become function signatures.

---

## Step 5: Derive the Engine API

Each relationship arrow is a function. `produces` → a method that returns the object. `compared to` → a method that takes the two objects and returns the comparison.

```python
# VaRResult ← "the portfolio produces VaR measurements"
engine.compute_var(returns, date) -> VaRResult

# VaRChange ← "compare two VaRResults"
engine.compute_change(current: VaRResult, previous: VaRResult, 
                       change_history: list[VaRChange]) -> VaRChange

# Attribution ← "decompose VaRResult into asset contributions"
attributor.attribute(returns, date) -> Attribution

# RiskDrift ← "compare Attribution to Portfolio.risk_allocation_target"
monitor.compute_drift(attribution: Attribution, portfolio: Portfolio) -> RiskDrift

# RebalanceRecommendation ← "drift triggers a rebalance proposal"
rebalance.analyze(drift: RiskDrift, portfolio: Portfolio,
                  historical_context: list[DecisionOutcome]) -> RebalanceRecommendation
```

The API surface is exactly the set of questions the artifacts ask. No more, no less.

---

## Step 6: Implement Engine Modules

This is where bottom-up meets top-down. The API from Step 5 is the contract. The implementation uses whatever exists (existing VaR functions, numpy, pandas) to fulfill it.

- Public methods match the Step 5 signatures exactly
- Private methods (`_leading_underscore`) handle implementation details
- Dataclasses from Step 3 become the return types
- Type hints from Step 5 become the function signatures

---

## Step 7: Build Display Layer

Thin notebook cells that import the engine, call the API, and render the result. A cell should be ~10 lines. Business logic lives in `src/`, never in notebook cells.

```python
# Thin cell: import, compute, display
engine = VaREngine(portfolio)
brief = engine.daily_brief(returns, date)
Markdown(render_daily_brief_markdown(brief))
```

---

## The Artifact-First Test

Before writing any engine code, ask:

> "If I had all the domain objects populated with real data, could I render the artifact completely?"

If yes → the domain model is complete. Start implementing.
If no → the domain model is missing something. Go back to Step 2.

The artifact is the spec. If the domain model can't populate every field in the artifact, the domain model is wrong.

---

## Per-Slice Deliverables

Each new vertical slice produces:

| Deliverable | When |
|---|---|
| Artifact mockup (annotated) | Design phase — before any code |
| Domain model (objects + relationships) | Design phase — derived from annotations |
| Engine API (function signatures) | Design phase — derived from relationships |
| `src/` modules implementing the API | Implementation phase |
| `src/display/` renderers for the artifact | Implementation phase |
| Thin notebook(s) consuming the engine | Implementation phase |
| Tests for engine modules | Implementation phase |

---

## Example: How V1 Applied This

| Step | What we did |
|---|---|
| 1. Design artifacts | Sketched Daily Risk Brief + Monthly Risk Review with mock data |
| 2. Annotate fields | Mapped every number/label to a domain concept |
| 3. Extract domain objects | `VaRResult`, `VaRChange`, `Attribution`, `RiskDrift`, `RebalanceRecommendation`, `Decision`, `VaRContext` |
| 4. Define relationships | Portfolio → VaRResult → Attribution → RiskDrift → RebalanceRecommendation → Decision |
| 5. Derive API | `compute_var()`, `compute_change()`, `attribute()`, `compute_drift()`, `analyze()` |
| 6–7. Not yet | Pending |
