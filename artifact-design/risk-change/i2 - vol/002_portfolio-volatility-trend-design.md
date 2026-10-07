# Designing the Portfolio Volatility Trend

The existing artifact answers:

> **“Where does portfolio risk come from at this observation date?”**

The trend extension should answer a narrower additional question:

> **“Has the portfolio’s structural risk level changed over time, and how recently?”**

That suggests we should add a **time dimension to the headline measure**, without redesigning the existing asset-level snapshot.

## Recommended artifact relationship

Treat the trend as a second section of the same artifact:

1. **Portfolio volatility trend** — how the headline risk level has changed;
2. **Current asset contribution snapshot** — where risk currently lives;
3. **Optional current-versus-prior contribution comparison** — how the distribution of risk has changed.

The trend should come first because it establishes whether there is a change worth investigating. The existing contribution view then helps the PM inspect the current state.

---

# What “trend” should mean in V1

There are several possible meanings:

### 1. A sequence of historical observations

For example, calculate portfolio volatility at each month-end using a rolling covariance window.

This shows the path:

```text
January: 8.7%
February: 9.1%
March: 10.4%
April: 9.8%
```

### 2. A current-versus-prior change

For example:

```text
Current volatility: 9.8%
One month earlier: 10.4%
Change: −0.6 percentage points
Change: −5.8%
```

### 3. A persistent movement

For example:

```text
Volatility has increased over four of the last six observations.
```

The first two are appropriate for V1. The third begins to interpret the series and would need a definition of persistence.

I would therefore avoid describing V1 as detecting a “trend” in a formal statistical sense. It should display a **volatility history plus a clearly defined recent change**.

A better internal description may be:

> **Portfolio volatility history and recent change**

The artifact can still be named `Portfolio Volatility Change`, but this distinction helps avoid implying that we have built a trend-detection model.

---

# Proposed visual

## A single time-series chart

The primary visual should be a line chart with:

- x-axis: observation date;
- y-axis: annualised portfolio volatility;
- one point per observation date;
- a highlighted latest observation;
- optionally, a highlighted prior comparison observation.

Example:

```text
Annualised portfolio volatility

12% |                         ●
10% |              ●────●─────┘
 8% |      ●──●
 6% |
    +--------------------------------
      Jan   Feb   Mar   Apr   May
```

The visual should not initially include:

- a target volatility line;
- warning thresholds;
- shaded “high-risk” regions;
- multiple estimation windows;
- annotations explaining market events.

Those additions would introduce judgement or competing interpretations.

## Why a line rather than bars?

Volatility is a level observed through time. A line makes continuity and direction visible. Bars would emphasise individual observations and make the artifact feel more like a period-by-period reporting table.

A table can sit below or beside the chart for inspectability, but the chart should carry the time-series concept.

---

# The headline comparison

The chart needs a compact summary so the PM does not have to estimate the change visually.

I would place three values beside or above the chart:

```text
Current volatility       9.8%
Previous observation    10.4%
Change                  −0.6 pp
```

The primary change measure should be **percentage points** because volatility itself is expressed as a percentage.

For example:

- 9.8% versus 10.4%;
- change: **−0.6 percentage points**.

A relative change can be included as a secondary diagnostic:

```text
Relative change: −5.8%
```

But it should not be the only change measure. Percentage-point changes are easier to interpret and do not obscure the underlying levels.

---

# Which prior observation?

This is an important design choice because “change” has no meaning without a reference.

For a monthly artifact, I would use:

> **latest month-end versus previous month-end**

That is simple and matches the likely operating rhythm of a PM reviewing risk.

The time-series chart could show the preceding 12–24 monthly observations, while the headline comparison uses the last two available points.

This gives two different horizons:

- **chart:** context and persistence;
- **headline:** immediate recent change.

We should label the dates explicitly rather than saying only “current” and “previous”:

```text
31 Mar 2024: 10.4%
30 Apr 2024: 9.8%
```

This avoids ambiguity around missing month-ends, holidays, and irregular data.

---

# What should the PM be able to infer?

The portfolio volatility section should support three visual readings.

## 1. Current level

Where is the portfolio’s estimated structural volatility now?

This is still the existing snapshot’s primary headline.

## 2. Recent direction

Has the level moved up or down since the previous observation?

This introduces the change-over-time concept directly.

## 3. Shape of the recent history

Does the latest move appear to be:

- part of a gradual increase;
- part of a gradual decrease;
- a sharp one-period movement;
- a reversal;
- broadly stable?

The artifact should let the PM make those observations without embedding labels such as “persistent increase” or “risk escalation.”

---

# Methodological design

For consistency with the current decomposition, each historical point should use:

1. the same portfolio weights;
2. a rolling covariance estimate;
3. the same annualisation convention;
4. the same asset universe;
5. the same missing-data rules.

Conceptually:

```text
portfolio volatility at date t
= volatility implied by the rolling covariance estimate ending at date t
  using the current portfolio weights
```

The important part is that the calculation convention must remain fixed across dates. Otherwise, a change in the chart could be caused by changing methodology rather than changing risk.

## Recommended starting convention

- daily asset returns;
- 252 trading-day rolling estimation window;
- month-end observation dates;
- annualised volatility;
- current portfolio weights applied to each historical covariance estimate.

That makes the visual a history of the **current allocation’s estimated structural risk**.

The section should explicitly say this somewhere in the body:

> Historical observations use the current portfolio weights. The series shows how the current allocation’s estimated structural risk would have changed as the return and covariance environment changed. It is not the realised volatility history of the portfolio as actually held through time.

That note is essential. Without it, the chart could be mistaken for a performance or realised-risk history.

---

# Avoiding a misleading smooth trend

Rolling covariance estimates overlap. If we use a 252-day window and monthly observations, adjacent points share most of their data.

That is acceptable for monitoring, but it means:

- observations are not independent;
- the line will naturally look smooth;
- a gradual movement does not automatically establish a statistically meaningful trend.

Therefore, the artifact should use neutral language:

- “estimated volatility increased over the recent observations”;
- “the latest estimate is higher than the previous observation”;
- “the series shows a sustained rise across the displayed period.”

It should avoid:

- “volatility is definitively trending higher”;
- “the increase is persistent”;
- “the portfolio has entered a high-volatility regime.”

Those stronger statements need additional rules.

---

# How this changes the artifact structure

I would make the visual structure:

## Header

- artifact name;
- portfolio name;
- latest observation date.

## Section 1 — Portfolio volatility history

- line chart;
- latest value;
- prior comparable value;
- absolute change in percentage points;
- optional relative change.

## Section 2 — Current asset risk contribution

- existing ranked contribution table;
- current portfolio weights;
- contribution bars;
- cumulative contribution.

## Section 3 — Contribution change

Only if we decide it adds enough value for V1:

- prior contribution;
- current contribution;
- change in percentage points;
- ranked by current contribution.

## Methodology note

- rolling window;
- observation frequency;
- annualisation;
- fixed-current-weights convention;
- interpretation boundary.

The key design principle is that the trend section should not replace the current snapshot. It provides context for it.

---

# Is the asset contribution change needed immediately?

There are two reasonable V1 scopes.

## Narrowest V1

Include only:

- portfolio volatility history;
- latest-versus-prior volatility change;
- existing current contribution snapshot.

This answers:

> “Has total structural risk changed, and where does risk currently live?”

This is the safest minimal extension.

## Slightly broader V1

Add the current-versus-prior contribution comparison.

This answers:

> “Has total structural risk changed, and has the distribution of risk between assets changed too?”

I lean toward the broader version eventually, but I would design the artifact in two conceptual layers:

### Required

Portfolio volatility history and latest change.

### Supporting extension

Asset contribution change between the latest two observations.

The reason is that the time-series concept should first be made clear at the portfolio level. If we immediately add several comparison columns to the asset table, the primary idea—change in the headline risk level—may become less obvious.

---

# My recommended design decision

For this notebook extension, I would specify:

> Add a portfolio-level volatility history above the existing snapshot. Calculate monthly observations using a 252-trading-day rolling covariance window and current portfolio weights. Display the latest estimate, the immediately preceding estimate, and the change in percentage points. Use the full line chart to provide context, but do not classify the movement or make a rebalance recommendation.

That introduces change over time with the smallest conceptual delta:

```text
point-in-time portfolio risk
        ↓
portfolio risk at repeated historical observation dates
        ↓
latest-versus-prior change
        ↓
PM decides whether further investigation or rebalancing analysis is warranted
```

The next design question is whether the trend should display **only the latest 12 monthly observations** or the **full available history**. For a PM-facing artifact, I would initially prefer the latest 12–24 observations, while preserving the full series in the underlying structured output for later analysis.
