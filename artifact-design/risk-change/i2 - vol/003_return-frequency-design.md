This is the right first question, because **return frequency** and **observation frequency** are separate design choices.

- **Return basis:** daily or monthly returns used to estimate volatility and covariance.
- **Observation frequency:** how often we recalculate and display the estimate, such as daily or month-end.

A sensible design could therefore be:

> **Estimate volatility from daily returns, but observe and report it at month-end.**

That is different from estimating volatility from monthly returns.

# What decision is the PM making?

The relevant decision is not:

> “What was the volatility of each calendar month?”

It is closer to:

> “Given the current allocation, has the risk environment changed enough that I should investigate the portfolio or consider rebalancing?”

For that decision, the estimate should be:

- sufficiently responsive to a changing risk environment;
- stable enough not to react to one unusual return;
- based on enough observations to estimate cross-asset covariance credibly;
- comparable with the existing point-in-time risk snapshot.

Those requirements favour **daily returns as the estimation basis**.

# Daily return volatility

The current approach uses 252 daily return observations. Conceptually, it estimates the covariance matrix from roughly one year of daily market movements and applies the current weights.

This has several advantages.

## More observations for covariance estimation

With four assets, the covariance matrix contains multiple variances and pairwise covariance terms. Using 252 observations provides materially more information than using only 12 monthly observations.

With monthly returns, a one-year window would contain approximately:

```text
12 observations
```

That is a very small sample for estimating a multi-asset covariance matrix. The resulting portfolio volatility and asset contributions could move substantially because of one or two monthly observations.

## Better detection of changing risk

Daily data allows the rolling window to react gradually as a volatility episode enters or leaves the sample.

For example, a sharp market shock can begin influencing the estimate before the end of the month. A monthly-return estimate would only represent that event in the single month in which it occurred.

## Consistency with the existing artifact

The current snapshot already uses daily returns over 252 observations. Retaining that basis means the change-over-time extension compares like with like:

```text
existing snapshot:
daily returns → covariance → portfolio volatility

trend:
repeated daily-return covariance estimates → portfolio volatility history
```

Changing to monthly returns would make it harder to tell whether a difference came from the market environment or from changing the estimation methodology.

# Monthly return volatility

Monthly returns are not inherently wrong. They answer a different question:

> “How variable were monthly portfolio returns?”

That could be relevant if the PM explicitly makes decisions on a monthly return-risk horizon. However, there are drawbacks for this V1.

## Small effective sample

A rolling 12-month window is too short for a reliable covariance-based asset decomposition.

A longer monthly window, such as 60 months, would provide more observations, but then the estimate would be slow to respond to a changing risk environment. It would also represent a different risk horizon from the current daily/252-day snapshot.

## Coarser event representation

Daily movements within a month are compressed into one observation. Two months with very different paths can have similar monthly returns and therefore appear similarly risky under a monthly-return calculation.

## Potential mismatch with the decision

The PM may review or rebalance monthly, but that does not necessarily mean the risk estimate should be based on monthly returns. The review frequency determines **when we inspect the estimate**; it does not by itself determine **how the risk estimate should be calculated**.

# The recommended distinction

For this artifact, I would use:

| Design choice | Recommendation |
|---|---|
| Return basis | Daily returns |
| Covariance window | 252 trading days |
| Observation frequency | Month-end |
| Volatility output | Annualised |
| Portfolio weights | Current weights applied at every historical observation |
| Comparison | Latest month-end versus previous month-end |

This gives the PM a monthly operating view without throwing away the information in daily returns.

The design could describe the measure as:

> **Annualised structural portfolio volatility estimated from a rolling 252-trading-day window of daily asset returns, evaluated at month-end.**

That sentence makes all three dimensions explicit:

1. what is being measured;
2. which returns are used;
3. when observations are recorded.

# One subtle point: daily basis does not mean daily decisioning

Using daily returns does not mean the PM is expected to react to daily noise.

The 252-day rolling window smooths the estimate, and month-end observation points further establish the operating rhythm. The PM sees:

- a stable but responsive estimate;
- a monthly change;
- a historical path showing context.

This is likely more useful than either:

- a daily chart that encourages overreaction; or
- a monthly-return covariance estimate built from too few observations.

# What about the PM’s actual holding horizon?

If the portfolio is intended to be managed over a longer horizon, such as several months or a year, the daily estimate can still be appropriate. Daily data is commonly used to estimate the underlying covariance structure, while the result is annualised for comparison and portfolio risk budgeting.

However, we should not imply that annualised daily volatility is an exact forecast of realised annual volatility. Annualisation uses a scaling convention. In the simplest form:

$$
\sigma_{\text{annual}} = \sigma_{\text{daily}}\sqrt{252}
$$

Here:

- $\sigma_{\text{daily}}$ is the estimated standard deviation of daily portfolio returns;
- $252$ is the approximate number of trading days in a year;
- $\sqrt{252}$ converts the daily scale to an annual scale under the usual independence assumption.

In practice, daily returns are not fully independent, especially during stressed markets. So this is a consistent reporting convention, not a guarantee that annual risk will equal daily risk multiplied by $\sqrt{252}$.

# Should we add monthly-return volatility later?

Possibly, but I would treat it as a **different diagnostic**, not a replacement.

A later comparison could ask:

> “Does the portfolio’s risk look different when measured at the monthly return horizon?”

That may be useful for understanding horizon dependence, but putting both measures into V1 risks confusing the PM:

- daily-based structural volatility;
- monthly-return realised volatility;
- perhaps daily realised volatility as well.

The first version should establish one stable convention.

# The important implementation detail

We should not describe the proposed visual simply as:

> “Monthly portfolio volatility.”

That could mean volatility calculated from monthly returns.

Instead, label it something like:

> **Portfolio structural volatility — daily returns, rolling 252-day window, month-end observations**

Or, in a shorter PM-facing label:

> **Annualised portfolio volatility**

with the methodology note beneath it.

# Recommendation

For the current decision workflow, I would keep the **daily return basis** and introduce the time dimension through **month-end observation dates**.

The rationale is:

1. the current snapshot already uses daily returns;
2. daily data gives a more credible covariance estimate for a multi-asset portfolio;
3. it responds to changing market conditions sooner;
4. monthly reporting matches a plausible PM review cadence;
5. it avoids treating a 12-observation monthly covariance estimate as precise;
6. it preserves comparability between the snapshot and the trend.

The design decision would be:

> **V1 estimates annualised structural portfolio volatility from daily returns over a rolling 252-trading-day window, recalculates it at month-end, and compares the latest estimate with prior month-end estimates.**

The remaining question is not primarily daily versus monthly returns. It is whether the **252-day window is the right responsiveness/stability trade-off** for the PM’s decision. That can be tested after fixing the return basis.
