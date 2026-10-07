I would **not** try to force historical VaR into a component-VaR framework, and I would **not** manually present volatility and covariance changes as if they were the causes of historical VaR changing.

For this project, I would approach **“Why did risk change?” as a separate historical-VaR change diagnostic**, while retaining structural volatility attribution as a separate current-state view.

## Short answer

Use three distinct layers:

1. **Historical VaR change**
   - “VaR rose/fell by how much?”
   - “Was that due to portfolio weights or the historical scenario set?”

2. **Historical tail diagnostics**
   - “Which observations now define or influence VaR?”
   - “What asset losses made up those observations?”

3. **Structural risk decomposition**
   - “Where does risk currently live across the portfolio?”
   - Based on portfolio volatility, not historical VaR.
   - Do not expect it to reconcile to historical VaR.

Then, later:

4. **Incremental VaR / trade analysis**
   - “What happens to VaR if I make this actual trade?”

That is a clean workflow boundary.

# Why not use component VaR as the answer?

Component VaR is tempting because it appears to answer:

> “How much of current VaR comes from each asset?”

But with historical VaR, this is not a naturally stable or canonical quantity.

Historical VaR is an empirical quantile:

$$
\operatorname{VaR}_\alpha(w)
=
\operatorname{Quantile}_\alpha
\left(
-\mathbf{w}^{\mathsf T}\mathbf{R}
\right)
$$

In plain terms:

- take the portfolio return for every historical day;
- turn those returns into losses;
- sort the losses;
- select the relevant percentile.

The selected observation can change abruptly when:

- the portfolio weights change slightly;
- the lookback window rolls;
- a new observation enters;
- an old observation leaves;
- two losses change order.

That means a finite-difference “marginal VaR” can be useful as a local sensitivity, but it does not necessarily provide a stable explanation of why the reported historical VaR changed.

I would therefore avoid displaying something called:

> “Historical Component VaR by Asset”

unless you are very explicit that it is an approximation or a separate allocation model.

Otherwise the PM may reasonably assume:

> “These asset values add exactly to the historical VaR headline and explain its movement.”

They generally do not.

# Why not manually decompose historical VaR into volatility and covariance?

The categories you listed are economically sensible:

- allocation;
- asset volatility;
- covariance/correlation;
- tail;
- model effects.

But volatility and covariance are not direct primitive drivers of historical VaR. They are summaries of the return distribution. Historical VaR depends on the actual ordered portfolio-loss observations.

For example, two return distributions can have similar volatility and correlation but different tails. Their historical VaRs can be materially different.

Conversely, historical VaR can change because one observation enters or leaves the lookback window even though the estimated volatility and correlation barely change.

So I would not write:

> “Historical VaR increased by 0.4% because asset volatility increased by 0.2% and covariance increased by 0.2%.”

That would be a model-based explanation imposed on a non-parametric measure.

You could calculate those quantities as **contextual diagnostics**, but the labels should be:

- “change in estimated volatility”;
- “change in estimated correlations”;
- “change in tail observations”;

not:

- “the volatility contribution to historical VaR change”;
- “the covariance contribution to historical VaR change”;

unless you have defined and implemented a proper counterfactual methodology.

# What I would implement for “Why did historical VaR change?”

Historical VaR is directly determined by two things:

1. the portfolio exposures;
2. the historical scenario set.

That gives you a defensible first decomposition.

## 1. Allocation or weight effect

Ask:

> “What would the previous historical VaR have been using the current portfolio weights?”

Let:

- $w_0$ be the previous portfolio weights;
- $w_1$ be the current portfolio weights;
- $R_0$ be the previous lookback return matrix.

Calculate:

$$
V_{00} = \operatorname{VaR}(w_0, R_0)
$$

This is the previous VaR.

Then calculate:

$$
V_{10} = \operatorname{VaR}(w_1, R_0)
$$

This is the VaR using current weights but the previous scenario window.

The conditional allocation effect is:

$$
\Delta V_{\text{weights}}
=
V_{10} - V_{00}
$$

This answers:

> “How much would VaR have changed solely because the portfolio weights changed, holding the historical scenarios constant?”

That is directly relevant to rebalancing because it tells the PM whether the portfolio itself has become more risky through:

- discretionary trades;
- drift;
- cash changes;
- allocation changes.

## 2. Historical-window or market-state effect

Now calculate current VaR using current weights and the current scenario window:

$$
V_{11} = \operatorname{VaR}(w_1, R_1)
$$

The conditional scenario-window effect is:

$$
\Delta V_{\text{window}}
=
V_{11} - V_{10}
$$

This answers:

> “How much would VaR have changed because the historical scenario set changed, holding current weights constant?”

This captures:

- new observations entering;
- old observations leaving;
- the ranking of losses changing;
- the empirical tail becoming more or less severe;
- the VaR-defining scenario changing.

The total change reconciles:

$$
V_{11} - V_{00}
=
\Delta V_{\text{weights}}
+
\Delta V_{\text{window}}
$$

provided you use this ordering.

This is already a useful and honest answer to the PM:

> “VaR increased by 0.9 percentage points. Approximately 0.1 points came from portfolio-weight changes and 0.8 points from the updated historical scenario window.”

That is much more defensible than pretending to have asset-level historical Component VaR.

# Important qualification: the bridge has an interaction effect

The order above gives an exact bridge, but the allocation effect depends on the order in which you calculate the changes.

You could instead calculate:

$$
V_{01} = \operatorname{VaR}(w_0, R_1)
$$

Then:

$$
\Delta V_{\text{window, conditional on old weights}}
=
V_{01} - V_{00}
$$

and:

$$
\Delta V_{\text{weights, conditional on new window}}
=
V_{11} - V_{01}
$$

Both paths reconcile to the total change, but they allocate the interaction differently.

For a small research project, I would not hide this. I would either:

### Option A: Use one clearly labelled bridge

For example:

> “Weight effect, holding the previous scenario window constant”

and:

> “Scenario-window effect, holding current weights constant”

This is simple and transparent.

### Option B: Average both paths

Calculate both orderings and report the average effect:

$$
\Delta V_{\text{weights}}
=
\frac{(V_{10}-V_{00})+(V_{11}-V_{01})}{2}
$$

$$
\Delta V_{\text{window}}
=
\frac{(V_{01}-V_{00})+(V_{11}-V_{10})}{2}
$$

This allocates the interaction symmetrically.

For the project, I would probably choose **Option A initially**, because the conditional interpretation is easier to explain and inspect. You can add the alternate ordering as a methodological sensitivity check rather than introducing Shapley attribution immediately.

# Then explain the scenario-window effect separately

The window effect is still broad. It tells you that the scenario set changed, but not exactly how.

That is where a small diagnostic overlay becomes valuable.

## Scenario diagnostics

For the previous and current snapshots, show:

- previous VaR;
- current VaR;
- previous VaR-defining date;
- current VaR-defining date;
- loss on the defining date;
- asset-level P&L contribution on that date;
- whether the defining observation entered, exited, or remained in the window;
- perhaps the nearest few observations around the VaR threshold.

This answers:

> “What historical experience is now driving the reported VaR?”

It is not a structural risk decomposition. Label it explicitly, for example:

> **Historical VaR scenario diagnostic**  
> Asset contributions to the selected historical loss observation.

The key wording is **selected historical loss observation**, not “asset contribution to VaR” without qualification.

You might also show a small tail table:

| Scenario date | Portfolio loss | Position 1 | Position 2 | Position 3 | Position 4 |
|---|---:|---:|---:|---:|---:|
| Previous VaR scenario | ... | ... | ... | ... | ... |
| Current VaR scenario | ... | ... | ... | ... | ... |
| Nearby tail scenario | ... | ... | ... | ... | ... |

This lets the PM see whether the VaR increase reflects:

- a genuinely worse market episode;
- a different asset mix in the tail;
- a single unstable observation;
- a change in the identity of the worst scenario.

# What happens to volatility and correlation?

I would retain volatility and correlation as **supporting evidence**, not as the primary VaR-change attribution.

For example, the output could say:

### Historical VaR change bridge

| Driver | Change |
|---|---:|
| Portfolio-weight effect | +0.1 percentage points |
| Historical-window effect | +0.8 percentage points |
| Total historical VaR change | +0.9 percentage points |

### Market-state context

| Measure | Previous | Current | Change |
|---|---:|---:|---:|
| Portfolio volatility | ... | ... | ... |
| Equity volatility | ... | ... | ... |
| Equity–bond correlation | ... | ... | ... |

The second table helps the PM interpret the first:

> “The historical-window effect coincided with higher equity volatility and weaker bond diversification.”

But it does not claim:

> “Higher equity volatility caused exactly 0.5 percentage points of the historical VaR increase.”

That distinction preserves analytical honesty.

# Where does the structural decomposition fit?

The structural decomposition remains valuable, but it answers a different question:

> “Given the portfolio's current covariance structure, where does current portfolio risk live?”

The workflow could show:

1. Historical VaR changed by +0.9%.
2. Most of that change came from the updated historical scenario window.
3. The current VaR scenario is concentrated in equity losses.
4. Current structural volatility risk is concentrated in SPY and EFA.
5. IEF is providing less diversification under the current covariance estimate.
6. Compare this state with the target allocation and risk budget.
7. Test candidate trades.

The structural decomposition may move in the same direction as VaR, but it may not.

That is not a problem. It is useful information.

For example:

- historical VaR rises because a severe 2020-like observation enters the window;
- structural volatility contribution barely changes;
- this tells the PM the headline VaR is being driven by empirical tail history rather than a major change in the estimated current covariance structure.

Or:

- historical VaR changes little;
- structural equity risk contribution rises materially;
- this may indicate that current covariance-based risk is becoming more concentrated, even though the selected historical percentile has not moved yet.

The gap is not something to conceal. It is a feature of using different risk measures.

You should make it explicit:

> Historical VaR and structural volatility contribution are different measures with different sensitivities. Their movements are not expected to reconcile or move identically.

# What belongs at each workflow stage?

| Workflow stage | PM question | Recommended output |
|---|---|---|
| Risk snapshot | “How risky is the portfolio now?” | Historical VaR, volatility, stress measures |
| Risk change | “What changed?” | Current value, previous value, absolute and relative change |
| VaR change diagnosis | “Why did historical VaR change?” | Weight/scenario-window bridge |
| Tail inspection | “What historical experience is driving it?” | Defining scenario and nearby tail diagnostics |
| Current risk location | “Where does risk live now?” | Structural volatility contribution |
| Portfolio assessment | “Is this consistent with the intended portfolio?” | Target weights, risk budget, permitted ranges |
| Trade analysis | “What can I do about it?” | Incremental VaR, marginal risk, post-trade VaR, costs |

This also clarifies the models in `001_historical-var-attribution-models.md`:

| Model | Where it is valuable |
|---|---|
| Scenario attribution | Tail inspection: “What happened in the selected VaR scenario?” |
| Finite-difference marginal VaR | Later trade sensitivity or local risk sensitivity |
| Component VaR approximation | Optional research comparison; not the primary historical VaR explanation |
| Incremental VaR | Candidate-trade analysis |
| Conditional/tail attribution | Later tail-risk or Expected Shortfall artifact |
| Shapley attribution | Research extension when interaction allocation itself is the question |

The original suggestion to implement scenario attribution plus incremental VaR first is reasonable in a general sense, but for the specific **“Why did VaR change?”** question I would insert the weight/window bridge before incremental VaR.

Incremental VaR answers:

> “What would happen if I changed the portfolio now?”

It does not answer:

> “Why did the reported VaR change between yesterday and today?”

# My recommendation for this project

For the current stage, I would define the minimum useful scope as:

## A. Keep the existing structural attribution

Purpose:

> Current-state risk location.

Do not rename it as historical VaR attribution.

## B. Add a historical VaR change bridge

Purpose:

> Explain the change in the headline historical VaR.

Use:

- previous weights and previous scenario window;
- current weights and previous scenario window;
- previous weights and current scenario window;
- current weights and current scenario window.

Start with the transparent two-step bridge:

1. weight effect;
2. scenario-window effect;
3. exact reconciliation to total VaR change.

## C. Add a small tail diagnostic

Purpose:

> Show which historical observations and asset losses are behind the window effect.

Include the defining scenario and perhaps nearby observations, but do not turn this into the main risk attribution.

## D. Add an explicit non-reconciliation note

Something like:

> Historical VaR is an empirical quantile of portfolio losses. Structural risk contribution is a covariance-based decomposition of portfolio volatility. They answer different questions and are not expected to reconcile or move identically.

## E. Defer component historical VaR

Do not make it part of the main PM workflow yet.

## F. Add incremental VaR only when candidate trades exist

Once the workflow reaches:

> “Should I reduce SPY, increase IEF, or make another allocation change?”

then incremental VaR becomes directly valuable.

---

## The core answer

Do not choose between:

- component VaR;
- manual volatility/covariance decomposition;
- ignoring the difference.

Instead:

> **Explain historical VaR changes with a historical-VaR-specific counterfactual bridge, use tail scenarios to diagnose the empirical distribution, and keep structural risk decomposition as a separate current-state view.**

The gap between historical VaR and structural volatility attribution should be **documented and interpreted**, not artificially eliminated.
