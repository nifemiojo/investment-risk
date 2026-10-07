# Design and implementation plan: asset contribution change comparison

## 1. Purpose

Extend `src/notebooks/001-risk-attribution.ipynb` with a comparison of asset-level contributions to the portfolio's structural volatility between two attribution states.

The existing notebook answers:

> **Where does the portfolio's structural volatility come from at a point in time?**

The new comparison adds:

> **Which assets' shares of the portfolio's structural volatility have changed between a reference observation and the current observation?**

This is a narrow extension. It does not introduce a full attribution time series, explain why contributions changed, or recommend a rebalance.

---

## 2. PM decision supported

The comparison provides evidence for the PM deciding whether the composition of the current portfolio's structural risk warrants further investigation.

It should help the PM observe which asset contribution percentages have:

- increased;
- decreased;
- changed the most in absolute terms.

It does not answer:

> **Should the PM buy or sell an asset?**

That remains a human decision requiring target weights, investment views, constraints, transaction costs, liquidity, and candidate trade analysis.

The artifact is evidence-only. It should not produce materiality labels, investigation routing, conclusions, or trade recommendations.

---

## 3. Canonical V1 design

Use two point-in-time covariance-based attribution states:

```text
Reference attribution → Current attribution → Contribution-percentage change
```

Both states use:

- the same named portfolio;
- the same asset universe;
- the current portfolio weights;
- the same daily return basis;
- the same covariance-based attribution method;
- the same estimation window.

This describes how the current allocation's estimated structural risk composition differs between two return-covariance environments.

It does not describe the risk contribution of the portfolio as historically held. Historical weights or transactions would be required for that question.

The comparison should fail clearly if the reference and current attribution results contain incompatible asset universes. It should not silently compare different sets of assets in V1.

---

## 4. Measure

The primary measure is the change in each asset's contribution percentage:

```text
change = current contribution % − reference contribution %
```

Display the result in **percentage points**:

```text
+6.6 pp
−4.4 pp
−0.3 pp
```

This answers:

> **Has the composition of the portfolio's structural risk changed?**

Do not use relative percentage change. Relative changes are difficult to interpret when the reference contribution is small or near zero.

Do not make absolute risk-contribution change the primary V1 measure. Absolute change mixes a change in contribution share with a change in total portfolio volatility and answers a different question.

---

## 5. Reference and current dates

Add a reference-date parameter alongside the existing current observation date:

```python
REFERENCE_DATE = "2020-02-21"
DATE = "2021-02-21"
ESTIMATION_WINDOW = 252
```

For each requested date, use the latest available return observation on or before that date. This handles weekends and holidays without silently treating a non-trading date as an observed market date.

The comparison must show the **resolved reference date**. The requested reference date does not need to be displayed.

The resolved current date should continue to follow the notebook's existing date-display convention.

For example, the rendered comparison may identify its states as:

```text
Reference observation: 2020-02-21
Current observation: 2021-02-19
```

The exact current-date presentation should remain consistent with the existing artifact. The important requirement is that the reference endpoint is explicit and not silently substituted.

---

## 6. New comparison table

Retain the existing current-state attribution artifact unchanged and add a separate comparison artifact below it.

The current render is a compact PM-facing Markdown artifact rather than a large titled report. It uses:

- the `ATTRIBUTION` identifier;
- portfolio name;
- an `As of` date line;
- the question `Where does risk live?`;
- a ranked table;
- signed contribution bars;
- cumulative risk contribution.

The contribution-change render should follow this established compact style rather than introducing a new `##` heading, a standalone methodology header, or the older standalone-volatility columns that are no longer present in the current attribution render.

### Existing attribution artifact

The current point-in-time output remains recognizable in its current form:

| Asset | Weight | Portfolio risk contribution | % | Cumulative risk contribution |
|---|---:|---:|---:|---:|

The `Portfolio risk contribution` column is rendered with a signed contribution bar, followed by the percentage and cumulative percentage. Negative contributions must continue to use the existing honest negative-value treatment rather than being converted to positive bars.

### New comparison artifact and table

The new artifact should use the same compact render conventions and identify the two states explicitly, for example:

```text
**CONTRIBUTION CHANGE**<br><br>
**60/40 Multi-Asset**<br>
Reference as of 21 February 2020<br>
Current as of 19 February 2021<br><br>
**How has risk contribution changed?**<br><br>
```

The exact wording can follow the established renderer vocabulary, but the resolved reference date must be visible. The requested reference date should not be displayed.

```text
| Asset | Reference contribution % | Current contribution % | Change, percentage points |
|---|---:|---:|---:|
```

The table should be sorted by absolute change descending so that the largest movements are easiest to inspect. This comparison table is additional to, and separate from, the current `ATTRIBUTION` table.

The absolute value used for ordering is a display concern only. It should not be presented as a recommendation or a materiality judgement.

The PM-facing output does not include a reconciliation-evidence section. Internal calculation tests may still verify the existing attribution contracts where appropriate, but contribution totals are not rendered as a separate evidence block.

---

## 7. Attribution semantics

Reuse the existing covariance-based attribution calculation rather than introducing a second decomposition method.

For portfolio weights $w$ and covariance matrix $\Sigma$, portfolio volatility is:

$$
\sigma_p = \sqrt{w^\top \Sigma w}
$$

Where:

- $w$ is the vector of asset weights;
- $w^\top$ is the transpose of the weight vector;
- $\Sigma$ is the covariance matrix of asset returns;
- $\sigma_p$ is portfolio volatility.

An asset-level component contribution in volatility units can be represented as:

$$
CC_i = \frac{w_i(\Sigma w)_i}{\sigma_p}
$$

The contribution percentage is:

$$
RC_i = \frac{CC_i}{\sigma_p}
$$

The comparison calculates the existing contribution percentage at each state and subtracts the reference value from the current value:

$$
\Delta RC_i = RC_{i,\ current} - RC_{i,\ reference}
$$

The implementation should preserve the existing attribution method and its treatment of signed contributions. The comparison layer should compare the resulting structured values; it should not recalculate covariance or silently change the attribution convention.

---

## 8. Architecture

Keep the existing attribution component intact and add a comparison component beside it.

```text
AttributionEngine
    → current point-in-time Attribution

AttributionComparisonEngine
    → reference Attribution
    → current Attribution
    → AttributionChange

attribution_renderer
    → current attribution table

attribution_change_renderer
    → compact contribution-change artifact and table
```

### AttributionComparisonEngine responsibilities

The comparison engine should:

- accept reference and current attribution results;
- confirm that the results are compatible for comparison;
- match assets by stable asset identifier;
- calculate reference contribution percentage;
- calculate current contribution percentage;
- calculate the signed change in percentage points;
- calculate absolute change for display ordering;
- preserve the resolved reference and current observation dates where required by the result contract;
- return an immutable structured result.

It should not:

- download data;
- recalculate covariance;
- calculate a new attribution method;
- decide whether a change is important;
- generate prose interpretation;
- route the PM to another workflow;
- emit a trade or rebalance recommendation.

A likely module boundary is:

```text
src/engine/attribution_comparison_engine.py
src/domain/attribution_change.py
src/display/attribution_change_renderer.py
```

The exact module names should follow the repository's existing naming conventions after the current contracts are inspected.

The comparison engine may reuse `AttributionEngine` through composition. It should not duplicate its covariance logic.

Conceptually:

```python
reference_attribution = attribution_engine.attribute(
    portfolio_name=PORTFOLIO,
    date=REFERENCE_DATE,
    estimation_window=ESTIMATION_WINDOW,
)

current_attribution = attribution_engine.attribute(
    portfolio_name=PORTFOLIO,
    date=DATE,
    estimation_window=ESTIMATION_WINDOW,
)

attribution_change = attribution_comparison_engine.compare(
    reference_attribution=reference_attribution,
    current_attribution=current_attribution,
)
```

---

## 9. Proposed domain output

The comparison result should contain calculated evidence rather than notebook-owned context.

A possible shape is:

```python
@dataclass(frozen=True)
class AttributionChangeObservation:
    asset: str
    reference_contribution_percentage: float
    current_contribution_percentage: float
    change_percentage_points: float


@dataclass(frozen=True)
class AttributionChange:
    reference_date: str
    current_date: str
    observations: tuple[AttributionChangeObservation, ...]
```

The field names should follow the existing domain model. `change_percentage_points` must be explicit so that the renderer cannot confuse an absolute percentage-point difference with a relative percentage change.

The result should not redundantly store:

- portfolio name;
- requested reference date;
- requested current date;
- estimation window;
- display-ordering labels;
- interpretation or recommendation text.

Caller-owned display context can be supplied to the renderer, subject to the existing DTO convention.

---

## 10. Renderer design

Add a renderer dedicated to the comparison result:

```text
src/display/attribution_change_renderer.py
```

Possible API, following the existing renderer pattern:

```python
render_attribution_change_markdown(
    attribution_change,
    *,
    portfolio_name: str,
    reference_date: str,
    current_date: str,
)
```

The renderer should:

- use the established compact Markdown style (`<br>` line breaks and no `##` heading);
- identify the portfolio and comparison states;
- show the resolved reference date;
- show the current observation date according to existing convention;
- render the new comparison table;
- sort rows by absolute contribution-percentage change descending;
- label the change column as percentage points;
- format positive and negative values honestly;
- avoid implying that a larger change is necessarily undesirable.

The renderer should not:

- recalculate differences;
- calculate or render absolute risk-contribution change;
- add a reconciliation block;
- add thresholds or materiality labels;
- generate conclusions;
- render the existing current attribution table.

The existing `attribution_renderer` remains responsible for the current point-in-time `ATTRIBUTION` display, including its signed contribution bars and cumulative contribution column. The new renderer should not alter or duplicate that output.

---

## 11. Notebook structure

The notebook should contain:

1. Parameters;
2. Imports and composition root;
3. Portfolio-risk calculation and rolling-volatility chart;
4. Current asset-attribution calculation and render;
5. Reference/current attribution comparison calculation and render;
6. Methodology notes.

The existing portfolio-risk section should remain as currently rendered: it presents current daily volatility, the latest calculated observation, and—when available—the previous-month daily volatility and change. The contribution-change extension must not collapse this into, or replace it with, an attribution-history visual.

The current attribution output must remain visible and recognizable. The comparison table is an additional output, not a replacement or redesign of the existing table.

The new comparison cell should contain orchestration only:

```python
reference_attribution = attribution_engine.attribute(
    portfolio_name=PORTFOLIO,
    date=REFERENCE_DATE,
    estimation_window=ESTIMATION_WINDOW,
)

current_attribution = attribution_engine.attribute(
    portfolio_name=PORTFOLIO,
    date=DATE,
    estimation_window=ESTIMATION_WINDOW,
)

attribution_change = attribution_comparison_engine.compare(
    reference_attribution=reference_attribution,
    current_attribution=current_attribution,
)

display(Markdown(render_attribution_change_markdown(
    attribution_change,
    portfolio_name=PORTFOLIO,
)))
```

Do not duplicate attribution or comparison business logic in notebook code.

---

## 12. Methodology note

The notebook should display a short note explaining the comparison boundary:

```markdown
The contribution comparison shows how the current portfolio's
covariance-based structural risk composition differs between the
reference and current observation dates.

Both dates use the current portfolio weights and the same 252-observation
daily-return estimation window. The comparison therefore describes how
the current allocation's estimated risk contribution changed with the
return covariance environment. It does not represent the realised risk
contribution of historical portfolio holdings.

Contribution changes are shown in percentage points. The comparison does
not determine whether an asset should be bought or sold.
```

If the reference date is resolved to an earlier trading date, the displayed resolved date should make that substitution visible.

---

# Implementation plan

## Phase 1 — Confirm existing contracts

Before coding:

- inspect the existing `Attribution` domain result;
- inspect the current attribution engine and renderer;
- inspect the current portfolio-risk renderer and notebook ordering;
- confirm the contribution-percentage field and its units;
- confirm the asset identifier used for matching;
- confirm the current engine's date-resolution behavior;
- confirm that current weights are used consistently by the existing attribution calculation;
- confirm the covariance estimation window and daily return convention;
- confirm how incompatible or missing asset data is currently handled;
- preserve the existing attribution behavior.

The plan must respect the current renderer contract: the existing attribution output uses `ATTRIBUTION`, compact line breaks, signed contribution bars, and cumulative risk contribution. It no longer renders standalone volatility as a column. The existing portfolio-risk render includes its current-level and previous-month evidence and should remain unchanged by this extension.

The comparison should use the same portfolio, asset universe, current weights, return source, covariance method, and missing-data convention as the existing attribution workflow.

## Phase 2 — Define the comparison domain result

Create an immutable result for the comparison and its per-asset observations.

Required evidence:

- resolved reference date;
- resolved current date, if required by the existing result/context convention;
- asset identifier;
- reference contribution percentage;
- current contribution percentage;
- signed change in percentage points.

Tests should confirm:

- observations are preserved or returned in the defined ordering;
- reference and current values are retained unchanged;
- the signed difference is calculated correctly;
- percentage-point semantics are explicit;
- the result is immutable;
- no recommendation or interpretation fields are present.

## Phase 3 — Implement comparison calculation

Create `AttributionComparisonEngine` or the repository-equivalent comparison boundary.

Required behavior:

- accept two compatible attribution results;
- match assets by stable identifier;
- calculate current minus reference contribution percentage;
- calculate absolute change only as an internal ordering value if needed;
- reject incompatible asset universes clearly;
- preserve resolved date information;
- return the structured comparison result.

Tests should cover:

- positive contribution-percentage change;
- negative contribution-percentage change;
- zero change;
- multiple assets;
- sorting by absolute change descending;
- asset matching independent of input row order;
- incompatible asset-universe failure;
- no relative percentage-change calculation;
- no absolute risk-contribution field in the PM-facing V1 result unless required by an existing contract.

The comparison engine must not recalculate covariance or duplicate the attribution method.

## Phase 4 — Implement comparison renderer

Create the dedicated comparison renderer.

Verify:

- the table contains the four agreed columns;
- the render follows the existing compact attribution style rather than introducing a `##` report heading;
- rows are ordered by absolute change descending;
- positive and negative changes are visible;
- the change column is labelled in percentage points;
- the resolved reference date is displayed;
- the current date follows the established convention;
- no requested reference date is unnecessarily displayed;
- the existing `ATTRIBUTION` render remains responsible for signed bars and cumulative contribution and is not duplicated or redesigned;
- no reconciliation section is rendered;
- no thresholds, conclusions, recommendations, or routing text are rendered;
- the renderer does not recalculate comparison values.

## Phase 5 — Extend the notebook

Add:

- `REFERENCE_DATE` to the parameters cell;
- comparison-engine and domain-result wiring to the composition root;
- a comparison calculation/render cell after the existing asset-attribution output;
- the agreed methodology note.

Keep the existing current attribution cell and output unchanged.

The notebook should remain an orchestration and evidence artifact rather than containing comparison business logic.

## Phase 6 — Notebook verification

Execute the notebook with the repository's established command, for example:

```bash
python3 -m jupyter nbconvert \
  --to notebook \
  --execute \
  --inplace \
  src/notebooks/001-risk-attribution.ipynb
```

Then verify:

- all cells execute successfully;
- the existing current attribution output remains present;
- the new contribution-change table is produced;
- the table contains the expected assets;
- the resolved reference date is visible;
- the comparison is ordered by absolute percentage-point change;
- no reconciliation evidence is rendered;
- the output does not contain relative percentage-change labels;
- the methodology note explains the current-weight convention;
- the notebook contains no notebook-local comparison business logic.

---

# Acceptance criteria

The implementation is complete when:

1. The notebook accepts an explicit `REFERENCE_DATE` in addition to the current observation date.
2. Reference and current dates resolve to the latest available return observation on or before each requested date.
3. The resolved reference date is displayed; the requested reference date does not need to be displayed.
4. The existing point-in-time attribution table remains unchanged and recognizable.
5. The notebook contains a separate asset-contribution comparison table.
6. The comparison uses two attribution states rather than a full attribution time series.
7. Both states use the same portfolio, asset universe, current weights, return basis, attribution method, and estimation window.
8. The comparison calculates current contribution percentage minus reference contribution percentage.
9. Changes are displayed in percentage points, not relative percentages.
10. The comparison table is ordered by absolute change descending.
11. Positive, negative, and zero changes are represented honestly.
12. Incompatible asset universes fail clearly rather than being silently compared.
13. No reconciliation-evidence section is rendered in the PM-facing output.
14. No thresholds, materiality labels, conclusions, investigation routing, or rebalance recommendations are produced.
15. Attribution calculation remains owned by the existing attribution component.
16. Comparison calculation and rendering have separate responsibilities.
17. The notebook contains no duplicated comparison business logic.
18. The notebook executes successfully with the comparison output present.
19. The methodology note explains that current weights are applied at both dates and that the result is not historical realised portfolio attribution.

---

## Canonical V1 decision

> **Extend `001-risk-attribution.ipynb` with a separate asset-contribution comparison table based on two covariance-based attribution states: a reference observation and the current observation. Use the same portfolio, asset universe, current weights, daily return basis, attribution method, and estimation window at both dates. Display reference contribution percentage, current contribution percentage, and their signed difference in percentage points, ordered by absolute change. Add an explicit reference date, display its resolved trading date, omit reconciliation evidence, preserve the existing attribution output, and keep the comparison evidence-only with no interpretation or rebalance recommendation.**

## Explicitly out of scope for V1

- full rolling or monthly attribution history;
- historical portfolio weights or transaction-aware attribution;
- absolute risk-contribution change as the primary measure;
- relative percentage change;
- reconciliation evidence in the notebook output;
- thresholds or materiality rules;
- generated interpretation;
- investigation routing;
- trade or rebalance recommendations.
