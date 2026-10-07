# Rebalancing in systematic investment management

A useful way to understand **rebalancing** is not as “resetting portfolio weights,” but as a **decision process that converts a desired portfolio into trades**.

Suppose a systematic strategy says:

> “Given the information available today, I want 60% equities, 30% bonds, and 10% commodities.”

But because markets have moved, the portfolio you actually own is:

| Asset       | Current | Target | Difference |
| ----------- | ------: | -----: | ---------: |
| Equities    |     66% |    60% |        -6% |
| Bonds       |     26% |    30% |        +4% |
| Commodities |      8% |    10% |        +2% |

Something has to decide:

> **Should we trade? If so, what should we trade, how much, and when?**

That is the rebalancing problem.

And in systematic investment management, the interesting part is that **“trade back to target immediately” is usually not the complete answer.**

---

## 1. Start with the workflow

Imagine you're running a systematic multi-asset portfolio.

Your system might look roughly like this:

```text
Market data / fundamentals / forecasts
                ↓
        Signal generation
                ↓
       Portfolio construction
                ↓
        Desired portfolio
                ↓
          REBALANCING
                ↓
      Proposed trade list
                ↓
     Pre-trade risk / constraints
                ↓
           Execution
                ↓
        Actual portfolio
                ↓
       Risk + performance
          monitoring
                ↺
```

Portfolio construction answers:

> **What portfolio would I ideally like to own?**

Rebalancing answers:

> **Given what I own now, is it worth trading toward that portfolio?**

Execution then answers:

> **How should I actually execute those trades?**

Keeping those three problems separate is an important mental model.

---

# 2. Why portfolios need rebalancing

Consider a simple £1m portfolio:

* £600k equities
* £400k bonds

So:

$$
w_E = 60\%
$$

$$
w_B = 40\%
$$

Suppose equities rise 20% while bonds don't move.

Now:

$$
V_E = \text{£720k}
$$

$$
V_B = \text{£400k}
$$

and total portfolio value is:

$$
V = \text{£1.12m}
$$

Therefore the equity weight becomes:

$$
w_E = \frac{720}{1120} \approx 64.3\%
$$

and bonds:

$$
w_B = \frac{400}{1120} \approx 35.7\%
$$

Nothing was traded.

But the portfolio has changed.

If the investment mandate is still 60/40, the portfolio now contains **more equity risk than intended**.

To restore 60% equities:

$$
0.60 \times \text{£1.12m} = \text{£672k}
$$

So roughly:

$$
\text{£720k} - \text{£672k} = \text{£48k}
$$

of equities must be sold and £48k of bonds bought.

That's the mechanical version of rebalancing.

But systematic investment management makes the problem much richer.

---

# 3. There are really two portfolios

This is the mental model I'd keep.

At any moment, distinguish:

### Current portfolio

What you actually own:

$$
w_t
$$

### Target portfolio

What the investment process says you ideally want to own:

$$
w_t^*
$$

The simplest desired trade is therefore:

$$
\Delta w_t = w_t^* - w_t
$$

For our portfolio:

$$
w_t =
\begin{bmatrix}
0.643 \\
0.357
\end{bmatrix}
$$

and:

$$
w_t^* =
\begin{bmatrix}
0.60 \\
0.40
\end{bmatrix}
$$

Therefore:

$$
\Delta w_t =
\begin{bmatrix}
-0.043 \\
+0.043
\end{bmatrix}
$$

Conceptually:

```text
Current Portfolio
       ↓
Compare
       ↑
Target Portfolio
       ↓
Difference
       ↓
Potential Trades
```

But **potential trades are not necessarily actual trades**.

That's where rebalancing policy enters.

---

# 4. Why wouldn't we always rebalance immediately?

Because trading isn't free.

Suppose your target moves from:

```text
Asset A: 10.00%
```

to:

```text
Asset A: 10.03%
```

Should you trade?

Probably not.

Perhaps tomorrow the signal changes and the target goes back to 10.00%.

You've paid:

* bid/ask spread,
* commissions/fees,
* market impact,
* potentially taxes,
* operational costs,

for essentially no economic benefit.

So there is a fundamental trade-off:

> **The portfolio gets worse when you don't trade, but trading itself costs money.**

This is the heart of systematic rebalancing.

We can think of it as:

$$
\text{Rebalance if benefit of trading} > \text{cost of trading}
$$

That simple statement eventually leads to quite sophisticated optimisation methods.

---

# 5. What causes the current and target portfolios to diverge?

There are several different mechanisms, and distinguishing them is useful.

## A. Market movement

You wanted 60/40.

Equities rally.

Now you're 64/36.

Your **target didn't change; your holdings drifted away from it.**

---

## B. Signals change

Imagine a systematic equity strategy ranking stocks using momentum.

Yesterday:

```text
Target MSFT = 4%
Target AAPL = 3%
```

New data arrives and your model changes its view:

```text
Target MSFT = 3%
Target AAPL = 4%
```

The portfolio must potentially trade.

Here, **the desired portfolio changed**.

---

## C. Risk changes

Suppose you're running volatility targeting.

Your target portfolio risk is:

$$
\sigma^* = 10\%
$$

Market volatility jumps.

Your holdings haven't changed much, but estimated portfolio volatility goes:

$$
10\% \rightarrow 14\%
$$

Your risk model may tell you to reduce exposure.

So the rebalance is driven by **risk**, rather than asset prices simply drifting away from fixed weights.

---

## D. Cash flows

Suppose investors add £10m to a £100m fund.

You now have cash that must be allocated.

Or investors redeem £10m.

You need to decide what to sell.

Cash-flow-aware rebalancing can reduce transaction costs because new cash can be used to move the portfolio toward target without selling existing positions.

---

## E. Portfolio constraints change

Perhaps:

* an asset becomes ineligible,
* an issuer breaches a concentration limit,
* liquidity deteriorates,
* leverage exceeds a limit,
* ESG restrictions change,
* an asset leaves an index,
* a risk limit is breached.

The feasible portfolio changes, forcing a rebalance.

---

# 6. Rebalancing policies

Now we get to the actual systematic decision.

There are several broad approaches.

## Calendar rebalancing

The simplest:

> Rebalance every Monday.

Or:

> Rebalance on the last trading day of every month.

So:

```text
Market movement
Market movement
Market movement
Market movement
       ↓
Monday
       ↓
Recalculate targets
       ↓
Trade
```

This is operationally simple and predictable.

But the obvious weakness is arbitrary timing.

Why should Monday matter economically?

You might have huge portfolio drift on Thursday and wait four days.

Or almost no drift on Monday and trade unnecessarily.

---

# 7. Threshold rebalancing

Instead, define tolerance bands.

Suppose:

$$
w_E^* = 60\%
$$

and allow:

$$
55\% \leq w_E \leq 65\%
$$

Then:

```text
60 → 61 → 62 → 63 → 64 → 64.8
                         no trade

60 → 61 → 63 → 65 → 66
                    ↓
                 REBALANCE
```

Now trading is triggered by the **state of the portfolio**, rather than the calendar.

This introduces an important systematic-investing idea:

> **Not every deviation from target is economically meaningful.**

---

# 8. But what should the threshold measure?

Weight deviation is only one possibility.

You could trigger based on:

### Weight drift

$$
|w_i - w_i^*| > \delta
$$

where:

* $w_i$ = current weight of asset $i$
* $w_i^*$ = target weight
* $\delta$ = permitted deviation.

But you could also monitor:

### Portfolio volatility

```text
Target = 10%
Current = 12.7%
Limit = 12%
→ rebalance
```

### Tracking error

For an index or benchmark-relative portfolio:

$$
TE > TE_{\max}
$$

### Factor exposures

Perhaps:

```text
Target market beta = 0.5
Current beta = 0.71
Maximum allowed = 0.65
→ rebalance
```

### Concentration

```text
Maximum single stock = 5%
Current NVDA weight = 5.6%
→ rebalance
```

### VaR

This connects directly to risk systems:

```text
Portfolio VaR
      ↓
Risk budget
      ↓
Within tolerance?
    /       \
  yes       no
   ↓         ↓
hold     rebalance
```

So **rebalancing doesn't necessarily mean maintaining fixed weights**.

It can mean maintaining the portfolio inside a desired **risk state**.

That's much more general.

---

# 9. Rebalancing as a control system

This is probably the most useful mental model for you.

Think of a thermostat.

You want:

```text
Target temperature = 20°C
```

But you don't want the heating system doing this:

```text
19.999°C → ON
20.001°C → OFF
19.999°C → ON
20.001°C → OFF
```

That would be inefficient.

Instead, you might tolerate:

```text
19°C ←──── 20°C ────→ 21°C
             target
```

and intervene when temperature moves sufficiently far away.

A systematic portfolio is similar.

```text
                    Markets
                      ↓
                  Portfolio
                      ↓
               Measure state
                      ↓
             Compare with target
                      ↓
               Is intervention
                  required?
                /          \
              no            yes
              ↓              ↓
            Hold          Generate
                           trades
                              ↓
                          Execute
                              ↓
                        New portfolio
                              ↺
```

This is why rebalancing is better understood as **portfolio control** than simply "resetting weights."

The portfolio manager has:

* a desired state,
* an observed state,
* disturbances,
* control actions,
* costs associated with control.

Markets continually disturb the system.

Trading is the control mechanism.

---

# 10. Rebalancing can itself encode an investment strategy

Here's where things get interesting.

Consider again 60/40.

Equities rally:

$$
60\% \rightarrow 66\%
$$

You rebalance by selling equities.

Then equities fall:

$$
60\% \rightarrow 54\%
$$

You rebalance by buying equities.

The strategy mechanically does:

> **Sell assets after they outperform and buy them after they underperform.**

So rebalancing can create a form of contrarian exposure.

Compare that with momentum.

A momentum strategy may say:

> Stocks that have risen should receive *more* weight.

So now there is a tension:

```text
Market movement:
Equities rise strongly
       ↓
Fixed-weight policy
       ↓
SELL EQUITIES

but

Momentum signal
       ↓
BUY MORE EQUITIES
```

This illustrates why you can't really separate rebalancing from the underlying investment philosophy.

---

# 11. Target portfolios in systematic investing are often moving

This is an important distinction from textbook 60/40 examples.

Suppose you're running a systematic factor strategy.

Every day you calculate expected returns:

$$
\hat{\mu}_t
$$

risk:

$$
\Sigma_t
$$

and perhaps transaction costs:

$$
C_t
$$

Portfolio construction produces:

$$
w_t^*
$$

Tomorrow, new information arrives:

$$
\hat{\mu}_{t+1}, \Sigma_{t+1}, C_{t+1}
$$

and therefore:

$$
w_{t+1}^*
$$

may be different.

So you're chasing a **moving target**.

```text
Monday
Current → Target A

Tuesday
Current → Target B

Wednesday
Current → Target C
```

This creates the concept of **turnover**.

A highly reactive strategy might constantly generate trades.

That can look fantastic in a frictionless backtest while being terrible in reality because transaction costs consume the alpha.

---

# 12. Turnover becomes a first-class concern

Suppose a strategy generates 20% annual alpha before costs.

Sounds excellent.

But imagine it turns over its entire portfolio 50 times per year.

If the effective cost per turnover is sufficiently high, a huge portion of that alpha disappears.

So systematic portfolio construction often asks something closer to:

> What portfolio improves my expected investment outcome **enough to justify moving away from my existing portfolio?**

That is a much richer question than:

> What is today's mathematically optimal portfolio?

This gives us three important objects:

$$
w_t
$$

current portfolio,

$$
w_t^*
$$

the theoretically desirable portfolio,

and:

$$
w_{t+1}
$$

the portfolio we actually choose to trade toward.

Those don't necessarily have to be the same.

---

# 13. Rebalancing becomes an optimisation problem

Eventually you can formalise the decision.

Suppose candidate portfolio $w$ has:

* expected return,
* risk,
* transaction costs.

Conceptually we might choose:

$$
\text{Portfolio utility} = \text{Expected return} - \text{Risk penalty} - \text{Trading cost}
$$

A common mathematical structure is:

$$
\max_w \left[ \mu^\top w - \frac{\lambda}{2} w^\top \Sigma w - C(w - w_{\text{current}}) \right]
$$

Don't worry about solving this yet.

The components are what matter.

$\mu$ is the vector of expected asset returns.

$w$ is the portfolio we're considering holding.

$\Sigma$ is the covariance matrix describing asset risk and co-movement.

$\lambda$ represents how strongly we penalise risk.

And:

$$
C(w - w_{\text{current}})
$$

represents the cost of trading from where we are now to the candidate portfolio.

That final term changes the nature of portfolio construction.

Without it:

> "What is the best portfolio?"

With it:

> "Given what I already own, what portfolio is worth paying to move to?"

That is much closer to the real investment-management problem.

---

# 14. Rebalancing vs portfolio construction vs execution

I'd make this distinction very explicit.

| Problem                | Core question                                     |
| ---------------------- | ------------------------------------------------- |
| Signal generation      | What opportunities do I believe exist?            |
| Portfolio construction | What exposures do I want?                         |
| Rebalancing            | Is it worth changing my existing exposures?       |
| Trade generation       | What orders achieve that change?                  |
| Execution              | How should those orders interact with the market? |
| Risk monitoring        | Are the resulting exposures acceptable?           |

They interact heavily.

For example:

```text
Momentum model
    ↓
AAPL attractive
    ↓
Portfolio construction
    ↓
Desired AAPL = 5%

Current AAPL = 3%
    ↓
Rebalancing
    ↓
Is moving 3% → 5% worth the cost?
    ↓
YES
    ↓
Trade generator
    ↓
Buy £2m AAPL
    ↓
Execution algorithm
    ↓
How/when should £2m be bought?
```

This is an excellent example of how quantitative methods become part of an **operational decision system** rather than existing as isolated calculations.

---

# 15. Where risk fits

Risk makes the workflow considerably richer.

Imagine:

```text
Current portfolio
       ↓
Portfolio risk engine
       ↓
Volatility = 11.2%
VaR = £1.8m
Beta = 0.74
Factor exposures = ...
       ↓
Compare against
mandate / risk budget
       ↓
Portfolio construction
       ↓
Candidate portfolio
       ↓
Recalculate risk
       ↓
Acceptable?
       ↓
Rebalance
```

And different violations can imply different urgency.

For example:

| Situation                        | Possible response               |
| -------------------------------- | ------------------------------- |
| Target weight moved 0.1%         | Ignore                          |
| Target weight moved 2%           | Consider trading                |
| Volatility slightly above target | Gradually deleverage            |
| Hard leverage limit breached     | Immediate rebalance             |
| VaR approaching budget           | Alert / investigate             |
| VaR exceeds hard limit           | Mandatory risk reduction        |
| Liquidity collapses              | Change execution/rebalance plan |

So a mature system doesn't merely output:

> **REBALANCE = TRUE**

It communicates **why intervention is required and what constraint or objective is driving it**.

---

# 16. A useful architecture for a rebalancing system

Given your interest in decision systems, I'd model the software around this workflow:

```text
┌─────────────────────────┐
│ Current Portfolio       │
│ holdings / cash / NAV   │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│ Market + Signal State   │
│ prices / alpha / vol    │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│ Target Portfolio        │
│ desired exposures       │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│ Rebalancing Engine      │
│                         │
│ drift                   │
│ risk                    │
│ constraints             │
│ transaction costs       │
│ turnover                │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│ Decision                │
│                         │
│ HOLD                    │
│ REBALANCE               │
│ FORCED REBALANCE        │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│ Proposed Trades         │
└───────────┬─────────────┘
            │
            ↓
       Execution
```

And importantly, the rebalancing engine should produce **decision context**, not merely trades:

```text
REBALANCE RECOMMENDED

Reason:
Equity risk exceeds target band.

Current:
Equity weight       64.8%
Target              60.0%
Allowed range       57–63%

Portfolio volatility
Current             11.7%
Target              10.0%

Proposed:
Sell £4.2m equities
Buy  £4.2m bonds

Expected result:
Equity weight       60.9%
Portfolio vol       10.3%

Estimated cost:
£7,800
```

That's much closer to an actual investment-management capability.

---

# 17. A project I'd build

Rather than build a "portfolio rebalancing calculator," build a **Systematic Portfolio Rebalancing Workbench**.

Start extremely small:

### Version 1

Five ETFs:

```text
SPY
TLT
GLD
DBC
IEF
```

Give the strategy fixed target weights.

Your system maintains:

```text
Current Portfolio
Target Portfolio
Drift
Risk
Rebalance Status
Proposed Trades
```

Simulate daily market prices.

Don't even need live data initially.

Then implement three policies:

1. Monthly rebalance
2. ±5% weight bands
3. Risk-based rebalance

Run exactly the same simulated market path through all three.

Measure:

$$
\text{Turnover}
$$

$$
\text{Transaction costs}
$$

$$
\text{Realised volatility}
$$

$$
\text{Maximum drift}
$$

$$
\text{Portfolio return}
$$

and perhaps:

$$
\text{VaR breaches}
$$

Now you aren't just learning what rebalancing means.

You're investigating an actual portfolio-management question:

> **How should an investment manager trade off portfolio drift against transaction costs and risk?**

That's a genuine systematic-investing problem.

---

# 18. Where I'd take the learning next

There's a natural progression:

```text
Fixed target weights
        ↓
Calendar rebalancing
        ↓
Threshold rebalancing
        ↓
Risk-based rebalancing
        ↓
Transaction costs
        ↓
Turnover constraints
        ↓
Moving target portfolios
        ↓
Signals + portfolio construction
        ↓
Cost-aware optimisation
        ↓
Optimal rebalancing / no-trade regions
```

The particularly important conceptual jump is **no-trade regions**.

Instead of believing there is one exact portfolio you must continuously maintain:

```text
          MUST BE HERE
               ↓
────────────── 60% ──────────────
```

you recognise that because trading is costly, there can be a region of portfolios where doing nothing is optimal:

```text
          NO-TRADE REGION

        57%              63%
         │                │
─────────┼────────────────┼─────────
         │      60%       │
         │     target     │

      HOLD              HOLD

< 57%                       > 63%
  ↓                           ↓
TRADE                       TRADE
```

That is a powerful mental model: **the mathematically ideal portfolio is not necessarily the economically optimal portfolio to trade to right now.**

For systematic investment management, I'd therefore define rebalancing as:

> **A control process that determines when and how to move the actual portfolio toward its desired risk and return exposures, while accounting for the costs and constraints of intervention.**

That definition will remain useful as you move from simple 60/40 portfolios all the way to systematic multi-factor and institutional portfolio construction.
