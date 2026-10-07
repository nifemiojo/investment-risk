# Portfolio Risk Change in Snapshot Notebook — Implementation Plan

> **Implementation approach:** Work directly in the repository. Write the code, run the tests, fix any issues, and verify the notebook.

**Goal:** Extend `src/notebooks/001-risk-snapshot.ipynb` so the existing risk snapshot is accompanied by an evidence-first comparison of current portfolio-level risk with a manually supplied reference date and an annualised trailing portfolio-level VaR chart.

**Architecture:** Keep the feature together with the existing Risk Snapshot notebook and workflow, but give temporal comparison its own `RiskChangeEngine`. The engine is responsible for loading the required data and calculating comparison evidence over time. Rendering remains separate from calculation through a new `risk_change_renderer`; the initial output is a compact full-width table followed by a separate annualised VaR history chart. The exact timing convention for the chart history is an explicit implementation checkpoint because the existing backtesting function and the point-in-time snapshot use different as-of dates.

**Tech Stack:** Python 3.12, pandas, NumPy, Matplotlib, Jupyter Notebook, pytest, existing historical VaR and rolling VaR functions.

---

## 1. Scope and decisions already made

### In scope

- Extend `src/notebooks/001-risk-snapshot.ipynb`; do not create a separate notebook for this feature at this stage.
- Keep the current snapshot and risk-change outputs together in the same notebook workflow.
- Let the user provide a custom reference date.
- Compare the current observation date with that reference date.
- Show current and reference portfolio-level risk side by side.
- Show the absolute and relative change in risk.
- Show the corresponding change in risk-budget utilisation.
- Include the full available history of annualised portfolio-level historical VaR risk states as a separate graph, not as part of the initial minimal table render.
- Define the chart history as an as-of-close risk-state history by relabelling the existing `rolling_var()` VaR observations to the close used by their input windows and appending the latest snapshot VaR at the latest close.
- Treat current risk level and direction/change as separate pieces of evidence.
- Avoid normative labels for combinations such as “high and rising” or “normal and stable.”
- Remain tabular and graphical only; no plain-language explanation, interpretation, decision, or recommendation is required at this stage.
- Do not add attribution, causal explanation, correlation diagnosis, target comparison, or trade recommendations.

### Explicit non-goals

This slice should not add:

- asset-level risk contributions;
- component-volatility attribution;
- factor attribution;
- explanations of why the risk changed;
- automatic “material change” judgement unless a separate threshold is explicitly approved;
- normative labels for the level/direction matrix;
- drift analysis;
- rebalance sizing;
- trade recommendations;
- a new production dashboard;
- a new independent notebook;
- a default reference-date calculation: the notebook requires a manually supplied reference date.

### Resolved presentation boundary

The notebook does not need a plain-language conclusion, explanation, interpretation, decision, or recommendation for this slice. It should present the evidence in tabular and graphical form only. The existing Risk Snapshot may retain its established output; the new Risk Change output should not add a second narrative layer.

---

## 2. User workflow to support

The notebook should tell one narrow story:

```text
Select current observation date
        ↓
Render the existing Risk Snapshot
        ↓
Select a custom reference date
        ↓
Calculate the reference portfolio-level risk state
        ↓
Compare reference and current states
        ↓
Show annualised trailing portfolio-level VaR history
        ↓
Leave diagnosis and action to later artifacts
```

The PM-facing questions are:

1. What is the portfolio’s current total risk?
2. What was the total risk at the selected reference date?
3. How much has the estimated risk changed, in which direction, and over what interval?
4. Has risk-budget utilisation moved closer to or further from the budget?
5. What does the current level look like in the available annualised portfolio-level VaR history?
6. Does the history provide temporal context without becoming an interpretation?

The notebook should expose evidence for these questions without deciding what the PM should do.

---

## 3. Data and calculation contract

The existing snapshot engine currently calculates a point-in-time `RiskSnapshot` from a portfolio name and date. It loads returns through the requested date, constructs portfolio returns, computes historical VaR, computes rolling VaR history, derives percentile context, annualises VaR, and compares it with the risk budget.

The existing rolling function returns a DataFrame with:

- `VaR`;
- `NextReturn`;
- `Breach`;
- a date index.

The implementation should reuse the existing historical VaR conventions:

- historical VaR;
- positive loss convention;
- 95% confidence by default;
- 252-observation rolling window by default;
- fixed portfolio weights for V1;
- no look-ahead in the existing out-of-sample `rolling_var()` backtesting series;
- for the chart, an as-of-close observation may use returns through that close, because those returns are available at the close being reported.

The comparison result should make the following unambiguous:

```text
current_date
previous_observation_date
current_var_pct
reference_var_pct
absolute_var_change_pct_points
relative_var_change_pct
current_var_currency
reference_var_currency
absolute_var_change_currency
current_annualised_var_pct
reference_annualised_var_pct
current_budget_utilisation
reference_budget_utilisation
budget_utilisation_change_pct_points
current_is_breach
reference_is_breach
current_percentile_rank
reference_percentile_rank
trailing_annualised_var_history
```

The exact Python type and field names remain subject to the architecture checkpoint below. The important requirement is that the calculation output contains structured evidence and does not contain a generated judgement such as `material_change`, `investigate`, `safe`, or `appropriate` unless separately approved. The history field must make its timing convention explicit; it must not be presented as an undifferentiated “rolling VaR” series.

### Definitions to preserve

- **Absolute VaR change in percentage points:** `current_var_pct - reference_var_pct`.
- **Currency VaR change:** `current_var_currency - reference_var_currency`.
- **Budget utilisation change in percentage points:** `current_budget_utilisation - reference_budget_utilisation`.
- **:** `1.0 - current_budget_utilisation`.

The renderer must label percentage-point changes separately from relative percentage changes. It must not display an unqualified value such as `+18.75%` when the intended meaning is an absolute percentage-point movement.

---

## 4. Architecture decision: separate `RiskChangeEngine`

The current direction is to create a new `RiskChangeEngine` responsible for loading the data and calculating temporal comparison evidence. `RiskSnapshotEngine` remains responsible for the existing point-in-time snapshot.

The API is:

```python
engine.compare(
    portfolio_name=PORTFOLIO,
    current_date=DATE,
    previous_observation_date=PREVIOUS_OBSERVATION_DATE,
)
```

The new engine should own:

- loading the return data needed for both dates;
- resolving a manually supplied non-trading reference date to the last available close;
- calculating the current and reference portfolio-level risk states;
- calculating absolute and relative changes;
- calculating budget-utilisation and headroom evidence;
- calculating the annualised as-of-close portfolio-level VaR history used by the chart;
- preserving the existing out-of-sample rolling VaR calculation as a separate backtesting concern rather than silently changing its meaning.

This boundary keeps temporal comparison semantics testable outside the notebook and avoids making the point-in-time snapshot engine responsible for a second artifact. The engine should not generate prose, normative labels, decisions, causal explanations, or recommendations.

The implementation should avoid duplicated downloads and inconsistent windows by loading data once per comparison operation. The exact internal reuse of snapshot calculations can be decided during implementation, but the public responsibility belongs to `RiskChangeEngine`.

---

## 5. Rendering decision: new `risk_change_renderer`

The initial render specification is consolidated here from the former standalone render design record. The first output is a minimal, full-width, evidence-only comparison table, followed by a separate annualised portfolio-level VaR history chart. The earlier `001_portfolio-risk-change-view.md` design record remains unchanged.

### Initial render question and evidence boundary

The table answers:

> **How different is the portfolio’s current estimated total risk from its estimated total risk at the selected reference date?**

It keeps three facts visually separate:

1. current level;
2. reference level;
3. signed movement between the two states.

It must not collapse them into labels such as `high and rising`, `material change`, `investigate`, or `reduce risk`. The renderer presents evidence only; it does not generate a conclusion, causal explanation, decision, recommendation, or workflow route.

### Compact full-width table design

Use the same compact, evidence-first discipline as the attribution artifact. The table should use the structure:

```text
Measure | Previous observation | Current observation | Change
```

Include:

- portfolio name;
- requested and resolved current date;
- requested and resolved reference date;
- daily portfolio-level historical VaR, if retained in the calculation contract, with explicit daily units;
- annualised portfolio-level historical VaR as the primary display basis;
- absolute VaR change in percentage points;
- relative VaR change as a percentage of the reference value;
- current and reference currency VaR and absolute currency change;
- current and reference risk-budget utilisation and utilisation change in percentage points;
- current headroom;
- current and reference breach status;
- current and reference percentile ranks, if available from the calculation contract.

The renderer must distinguish percentage-point movement from relative percentage movement. A signed value such as `+1.5 pp` is not interchangeable with `+18.8%`. Currency values retain currency units. Do not use red/green treatment or other styling that implies an overall judgement. Literal breach status may remain `Yes`/`No` because it reports the defined limit state, not a combined screen verdict.

Illustrative layout only — values are not actual portfolio results:

```text
RISK CHANGE
60/40 Multi-Asset
Current observation: 21 June 2025 · resolved close: 21 June 2025
Previous observation requested: 24 May 2025 · resolved close: 23 May 2025

PORTFOLIO-LEVEL VaR

Measure                         Previous observation   Current observation   Change
Annualised VaR                  12.7%             15.1%           +2.4 pp
Currency VaR                    £80,000           £95,000         +£15,000 (+18.8%)

RISK-BUDGET EVIDENCE
Risk-budget utilisation         80.0%             95.0%           +15.0 pp
                —                 5.0%
Breach status                   No                No

DISTRIBUTION CONTEXT
Historical percentile           54th              78th              +24 pp

Percentage-point changes are shown in the Change column; the currency VaR change also includes the relative percentage inline.
Values describe estimated portfolio-level historical VaR at two resolved closes.
The comparison does not attribute the change or recommend a portfolio action.
```

The example is a layout specification only. The current snapshot display remains recognizable and is not rewritten as a combined monolithic report.

Use a separate history cell for the graph; do not add it as another table section or interpretation layer.

Use a new renderer rather than extending `snapshot_renderer.py`:

```text
src/display/snapshot_renderer.py
    → existing point-in-time snapshot only

src/display/risk_change_renderer.py
    → temporal comparison table
    → annualised trailing-history plot
```

The renderer should expose separate functions for separate outputs:

```python
render_risk_change_markdown(comparison)
plot_trailing_portfolio_var(comparison.trailing_annualised_var_history, ...)
```

The initial minimal render is the table. The agreed annualised history plot is rendered in a different notebook cell using a separate function in the same renderer module. That keeps the calculation boundary in `RiskChangeEngine`, the tabular/graphical presentation boundary in `risk_change_renderer`, and the notebook workflow readable.

The current snapshot display must remain recognizable and must not be rewritten as a combined monolithic report.

---

## 6. Proposed notebook structure

The notebook should remain a compact, inspectable workflow.

### Cell 1 — Imports and composition root

Retain the existing imports and dependency wiring. Add only the selected comparison engine/domain type and comparison renderer/plotting dependencies.

If Matplotlib is used, import it explicitly and use Matplotlib only.

### Cell 2 — Parameters

Retain:

```python
DATE = "2025-06-21"
PORTFOLIO = "60/40 Multi-Asset"
```

Add:

```python
PREVIOUS_OBSERVATION_DATE = "2025-05-21"
```

The dates must be clearly named and easy to change. The notebook should not silently select a reference date.

If a requested date is not an available trading observation, the behavior must be explicit: either resolve to a documented available date or fail clearly. Do not silently compare a different date without displaying the resolved date.

### Cell 3 — Current snapshot

Keep the existing snapshot calculation and display behavior:

```python
snapshot = engine.snapshot(PORTFOLIO, DATE)
display(Markdown(render_snapshot_markdown(snapshot)))
```

Avoid changing the meaning or layout of the current snapshot as part of this slice.

### Cell 4 — Risk-change calculation

Calculate the comparison result using the selected architecture and custom reference date.

The output should retain both actual resolved dates and the two point-in-time risk states.

### Cell 5 — Risk-change summary

Display a compact comparison table or Markdown report with:

- reference date;
- current date;
- reference VaR;
- current VaR;
- absolute change in percentage points;
- relative change;
- reference and current currency VaR;
- currency change;
- reference and current annualised VaR;
- reference and current budget utilisation;
- utilisation change in percentage points;
- current headroom;
- reference and current percentile ranks;
- breach status at both dates.

The summary must present current level and direction as separate evidence. It should not produce a combined normative label.

### Cell 6 — Annualised trailing portfolio-risk history

The trailing history in this slice is the full available time series of **annualised portfolio-level historical VaR risk states** calculated under the same fixed portfolio, confidence level, and lookback convention as the comparison. It is not:

- a history of raw portfolio returns;
- a history of individual asset VaRs;
- an asset-level risk-contribution history;
- an out-of-sample breach report by another name;
- a causal explanation of the change.

Render it in a separate notebook cell through `plot_trailing_portfolio_var(...)`, not inside the Markdown comparison table.

The chart should include:

- date on the x-axis;
- one clearly labelled annualised portfolio-level VaR series;
- a marker or vertical line for the resolved reference date;
- a marker or vertical line for the current date;
- the actual history range;
- units on the y-axis;
- the annualised risk-budget line.

The plotted VaR and risk-budget line are both annualised. The chart must not plot daily VaR against the annualised budget.

#### Visual chart design

The chart is a full-width graphical companion to the comparison table. It should use the same compact, evidence-first visual discipline as the table: one clearly identified portfolio-level series, one comparable budget reference, and two date markers.

Illustrative layout only — the values below are not actual portfolio results:

```text
ANNUALISED PORTFOLIO-LEVEL VaR
60/40 Multi-Asset · fixed weights · 95% confidence · 252-observation window

VaR (%)
  20 ┤                                                              ╭── Current close
     │                                                        ╭─────╯
  15 ┤                                  ╭──────────────╮──────╯
     │                         ╭────────╯              │
  10 ┤─────────────────────────┼──────────────────────┼──────────── Risk budget
     │                         │                      │
   5 ┤                         ╰──── Reference close  │
     │
   0 ┼────────────────────────────────────────────────────────────────────
     2019             2021             2023             2025

     Previous observation requested: 24 May 2025 · resolved close: 23 May 2025
     Current observation: 21 June 2025
```

The implementation should use Matplotlib and preserve the following composition:

- a full-width figure rather than a dashboard of small panels;
- one solid line for the annualised portfolio-level historical VaR series;
- one visually distinct horizontal line for the annualised risk budget;
- a vertical reference marker at the **resolved** reference close;
- a vertical current marker at the resolved current observation;
- direct, concise labels for the two date markers without generated pattern descriptions;
- a y-axis labelled `Annualised VaR (%)`;
- a date x-axis with the actual plotted history range;
- a legend only if direct labels would make the chart less readable;
- consistent percentage formatting and no mixing of daily and annualised values.

The chart should make the two comparison points easy to locate without drawing attention away from the history. If the requested reference date differs from the resolved close, show that distinction in the surrounding date note or caption; do not place two apparently equivalent risk observations at different dates on the series.

The chart must not add:

- red/green treatment that implies an overall judgement;
- labels such as `spike`, `persistent`, `new regime`, or `unusual`;
- causal annotations;
- asset-level contribution bars;
- a combined risk-status score;
- a recommendation or action route.

The chart mockup is a visual specification, not a claim about actual values. The final output should preserve the same evidence boundary as the table: show the annualised risk level, budget reference, dates, and history; stop before interpretation.

### Rolling-history timing convention — implementation checkpoint

The existing `rolling_var()` function is explicitly a **backtesting** function:

```text
For date t:
    calculate VaR from returns before t
    label the result with t
    compare it with the realised return on t
```

Its `VaR` column is therefore a one-step-ahead forecast series. The date label identifies the day being tested, not the close through which the risk estimate was formed. Its `NextReturn` and `Breach` columns are useful for backtesting but are not required for the risk-change chart.

The existing point-in-time snapshot uses a different convention:

```text
For date t:
    calculate VaR from the latest lookback window through t
    report the risk state as of close t
```

Consequently, the final value of `rolling_var()` may not equal the snapshot VaR for the same displayed date. Reusing it without documenting this distinction would make the chart appear to be a history of the snapshot measure when it is actually a forecast-and-breach series.

### Agreed implementation

Reuse the existing `rolling_var()` calculation and its historical VaR values, but correct the date interpretation for the chart. For a row labelled `t+1`, `rolling_var()` calculates VaR from the return window ending at the close of `t`. Therefore, move that VaR observation back by one available trading observation and label it with the close through which its calculation window runs.

Conceptually:

```text
rolling_var() row at t+1
    VaR uses returns through close t
    → as-of-close history observation at close t
```

This is a relabelling of the forecast date to the input-window close; it is not `shift(1)` applied blindly to the displayed dates. “One day” means one available market observation, not one calendar day.

The `RiskChangeEngine` should expose the resulting display-ready series under an explicit name such as `as_of_close_var_history`. It may use a clearly named intermediate such as `rolling_forecast_var` and should document the relabelling in a comment. The renderer must not contain this timing logic.

The transformed `rolling_var()` output stops at the penultimate available close because the latest close has no following observation from which `rolling_var()` can produce a row. Append the latest snapshot’s annualised VaR at the latest resolved close so the history includes the current observation and agrees with the current snapshot.

Only the VaR values are reused for this chart. Do not carry `NextReturn` or `Breach` into the as-of-close risk-state history: those fields retain their original forecast/backtesting meaning. Preserve `rolling_var()` unchanged for its existing backtesting use case; do not add a new public low-level method for this slice. The engine owns the relabelling and endpoint completion, while `risk_change_renderer` only renders the returned annualised series.

The resulting history must use the same VaR methodology, confidence, window, fixed portfolio weights, and annualisation convention as the comparison snapshots. This makes the chart comparable to the reference and current as-of-close states without changing the established `rolling_var()` contract.

### Cell 7 — Method and boundary note

Include a short Markdown note:

> This comparison describes how the estimated portfolio-level historical VaR changed between two selected dates. It does not explain the source of the change, establish causality, or recommend a portfolio action. With fixed weights, the comparison reflects the empirical return distribution and rolling estimation window rather than portfolio reweighting.

### Cell 8 — No prose conclusion required

Do not add a plain-language conclusion, explanation, interpretation, decision, or recommendation for this slice. The table and annualised VaR history graph are the outputs. The existing Risk Snapshot’s established content is not being redesigned here.

---

## 7. Implementation tasks

The implementation should be direct and iterative: write the code, run tests, fix issues, then integrate and verify the notebook.

### Task 1: Inspect the existing implementation and create the risk-change boundary

**Objective:** Confirm the existing snapshot, rolling VaR, data-provider, and renderer contracts before adding the feature.

**Files:**

- Inspect: `src/engine/risk_snapshot_engine.py`, `src/domain/risk_snapshot.py`, `src/rolling.py`, `src/boundaries/returns_provider.py`, `src/display/snapshot_renderer.py`.
- Create: `src/engine/risk_change_engine.py`.
- Create: `src/domain/risk_change.py`.

Keep `RiskSnapshotEngine`, `rolling_var()`, and the snapshot renderer compatible. The new engine owns the two-date comparison, date resolution, and as-of-close history. Use explicit names such as `rolling_forecast_var` and `as_of_close_var_history`.

### Task 2: Write the comparison and history code

**Objective:** Implement the smallest complete calculation contract described above.

The code should:

- accept current and manually supplied reference dates;
- resolve non-trading dates to the last available close and retain requested/resolved dates;
- calculate current/reference evidence and signed changes;
- reuse `rolling_var()` VaR values while relabelling them to the close used by each input window;
- annualise the history using the existing `sqrt(252)` convention;
- append the latest snapshot annualised VaR at the latest close;
- exclude `NextReturn` and `Breach` from the as-of-close chart history;
- avoid prose, normative labels, decisions, and recommendations.

Do not add a new public low-level rolling-history method or change the established `rolling_var()` contract.

### Task 3: Add the dedicated renderer

**Objective:** Render the compact full-width evidence table and the separate annualised history chart.

**Files:**

- Create: `src/display/risk_change_renderer.py`.
- Add or update focused tests under `tests/test_risk_change.py`.

Implement separate rendering functions for the table and chart. Show requested/resolved dates, annualised VaR, percentage-point and relative changes with distinct labels, budget evidence, the full-width history, the annualised budget line, and reference/current markers. Do not add interpretation or recommendation styling.

### Task 4: Run focused tests and fix issues

**Objective:** Exercise the new calculation and renderer, then correct any failures or semantic mismatches found.

Run:

```bash
pytest tests/test_risk_change.py -v
```

If the focused tests expose issues, fix the implementation and rerun them. Cover at least: positive/negative/zero changes, non-trading reference dates, insufficient history, equal dates, zero reference VaR, date ordering, annualisation, relabelling, latest snapshot endpoint completion, and preservation of `rolling_var()` backtesting behavior.

### Task 5: Integrate the notebook

**Objective:** Add the comparison table and separate annualised history chart to the existing snapshot notebook.

**File:**

- Modify: `src/notebooks/001-risk-snapshot.ipynb`.

Add the manually supplied `PREVIOUS_OBSERVATION_DATE`, retain the existing snapshot cell, add a comparison calculation/table cell, and add a separate chart cell. Use Matplotlib only, show requested/resolved dates and units, and keep the notebook tabular and graphical without a prose conclusion. Rewrite notebook JSON through Python rather than hand-editing it.

### Task 6: Run the full test suite and notebook validation, then fix remaining issues

**Objective:** Verify the complete feature and resolve any failures before considering the plan complete.

Run:

```bash
pytest tests/ -q
python3 -m jupyter nbconvert \
  --to notebook \
  --execute \
  --inplace \
  --ExecutePreprocessor.timeout=180 \
  src/notebooks/001-risk-snapshot.ipynb
```

Fix any test, execution, formatting, date-resolution, unit, or rendering issues and rerun the relevant checks until they pass. Inspect the executed notebook for the existing snapshot, comparison table, annualised history figure, visible dates, and absence of misleading or normative labels.

### Task 7: Final scope and regression review

**Objective:** Confirm that the implementation remains within the agreed risk-change slice.

Check that:

- existing snapshot behavior remains intact;
- `rolling_var()` remains unchanged as a backtesting helper;
- the engine/renderer separation is preserved;
- the latest snapshot completes the as-of-close history;
- daily and annualised units are not mixed;
- no attribution, causal explanation, drift, rebalance, trade recommendation, or prose conclusion was added;
- all focused tests, full tests, and notebook execution pass.

---

## 8. Risks and tradeoffs

### Historical VaR is an estimate, not a direct observation of economic risk

The report should describe a change in the estimated historical VaR produced by the rolling empirical distribution. It should not claim that the portfolio’s economic risk changed for a known reason.

### `rolling_var()` is a backtesting series, not automatically the chart’s risk-state history

The existing `rolling_var()` function deliberately calculates a forecast for date `t` from returns before `t`, then compares that forecast with the realised return on `t`. The chart is intended to show the portfolio’s estimated risk state as of each close. Those are different questions and can produce different values at the same displayed date.

The implementation must not silently reuse the `rolling_var()` date labels or carry its backtesting fields into the chart. It should reuse the existing `rolling_var()` VaR calculation, relabel each value to the close through which its input window runs, and append the latest snapshot’s annualised VaR for the latest close. This produces the as-of-close history required by the chart without changing `rolling_var()` or adding a new public low-level method.

### Comparison date versus available trading date

A custom date may be a weekend or holiday. Silent date substitution would undermine trust. The implementation needs an explicit policy and visible resolved date.

### Daily versus annualised units

The current snapshot exposes daily VaR and annualised VaR, while the low-level rolling history currently contains daily VaR. The chart will display annualised VaR, using the existing `sqrt(252)` scaling convention, and will show the annualised budget on the same basis. The daily series must not be plotted directly against the annualised budget.

### Repeated calculation

Calculating two snapshots independently may load and process the same return history twice. That is acceptable for the first notebook slice unless it creates a measurable execution problem. Do not introduce caching or a generalized data pipeline without evidence that it is needed.

### Engine scope

A separate `RiskChangeEngine` owns the temporal comparison and the as-of-close history because the chart requires semantics that are distinct from the existing point-in-time snapshot and the existing backtesting helper. The engine should reuse `rolling_var()` for the historical VaR values, relabel those values to the close used by each input window, and append the latest snapshot’s annualised VaR. It should not duplicate the VaR formula, change `rolling_var()`, or expose a new public low-level rolling-history method for this slice.

### Normative interpretation

A change can be large but leave current risk below the budget. A small change can move risk near a limit. The feature should expose both level and direction and leave the PM to interpret the combination until a decision rule is explicitly designed.

### Notebook maintenance

The notebook is a user-facing research artifact. Keep the new cells readable and ordered around the PM’s workflow, not around internal implementation details.

---

## 9. Definition of done

The feature is ready for review when:

- `PREVIOUS_OBSERVATION_DATE` is a custom notebook parameter;
- the existing snapshot remains visible and behaviorally intact;
- a tested comparison result shows current and reference portfolio-level risk;
- absolute and relative changes are separately labelled;
- budget utilisation and headroom changes are shown;
- current and reference percentile context are shown without normative labels;
- the annualised trailing-history plot is included as a separate output;
- date resolution and actual history range are visible;
- daily and annualised units are not mixed;
- no attribution, causal explanation, drift, rebalance, or trade recommendation has been added;
- all tests pass;
- the notebook executes successfully with `nbconvert`;
- the notebook has no new prose conclusion, explanation, decision, or recommendation;
- the annualised history timing convention is documented.

---

## 10. Questions for the next iteration

1. Should equal current and reference dates be rejected?
2. Should the chart mark only the resolved reference date, or both requested and resolved dates when they differ?
3. No new public low-level history helper is required for this slice; keep the relabelling and latest-snapshot endpoint completion inside `RiskChangeEngine` unless implementation evidence later justifies extraction.
4. After this comparison slice, should attribution be opened from the notebook as a later cell, or remain a separate artifact until the temporal comparison has been reviewed?
