Yes — I think adding a second asset-class focus is valuable, but only if it changes the **investment decision and risk model**, rather than merely adding another ticker to the portfolio.

## My recommendation: add rates, implemented through government bond futures

For your stated direction — systematic multi-asset investing, macro, portfolio construction and risk systems — I would choose:

> **Vanilla equities/equity indices + government bond futures**

This gives you both:

- a second economically meaningful asset class: **fixed income/rates**;
- a realistic instrument type: **futures**.

## Why rates are the best complement to equities

Equity risk can initially be represented largely through:

- price returns;
- volatility;
- correlation;
- beta or factor exposure;
- drawdown and stress loss.

Rates introduce a different risk vocabulary:

- yield changes rather than just price changes;
- duration;
- DV01/PV01;
- curve exposure;
- parallel and non-parallel curve shifts;
- carry and roll-down;
- contract expiry and rolling;
- leverage and margin;
- basis risk between the future and the underlying bond basket.

That makes the portfolio risk problem more realistic:

> “The portfolio has 10% bonds” is not enough information.  
> You also need to understand whether that exposure is short- or long-duration, concentrated at the front or long end of the curve, and how it behaves under inflation, growth and central-bank shocks.

That fits your existing project purpose very well: not just calculating total VaR, but explaining **where risk comes from and what decision the PM should consider**.

## The project would become more differentiated

A simple first portfolio could contain:

- equity index exposure;
- international equity exposure;
- government bond futures;
- perhaps cash or a defensive allocation.

The system could then answer questions such as:

- Is the portfolio’s apparent diversification genuine?
- Is the bond allocation still diversifying equity risk?
- How much portfolio risk comes from equity delta versus rates exposure?
- What happens under an equity sell-off combined with a rates sell-off?
- Is the portfolio unintentionally making a duration or curve bet?
- Should the rebalance reduce equity exposure, reduce duration, or reduce both?
- Does the recommended trade respect futures leverage, margin and roll constraints?

This gives you a stronger investment narrative than:

> “I extended my VaR calculator to support more instruments.”

The stronger narrative is:

> “I built a portfolio risk-monitoring workflow that distinguishes between equity price risk and rates risk, identifies the factor driving the portfolio’s current vulnerability, and translates that diagnosis into a rebalance decision.”

## Why I would not choose options as the second asset class right now

Options would be technically impressive, but I would not make them the next extension of this particular project.

You already have credible options experience:

- your CV includes an options risk system;
- your current role includes theta/gamma-based trader alerts and trade suggestions;
- your career notes identify live derivatives risk as part of your existing Spreadex exposure.

That means another options-focused project could be valuable, but it may not add as much **new evidence** to your public portfolio. It could also pull the project toward a dealer/trading-risk narrative rather than the systematic multi-asset portfolio workflow you are trying to establish.

Options should probably become a later, separate vertical slice:

> “How should nonlinear options exposures be incorporated into portfolio stress testing and hedging decisions?”

That would be excellent for applications to:

- options risk;
- derivatives technology;
- quantitative trading;
- volatility trading;
- front-office risk engineering.

But it is less necessary for the first version of your systematic-investing story.

## Why futures are useful, but should not be presented as an asset class

One distinction is worth preserving:

- **Equities, rates, FX and commodities** are asset classes or economic exposures.
- **Futures and options** are instrument types or implementation vehicles.

So the clean framing is:

> **Rates exposure implemented through government bond futures**

That signals that you understand both the economic risk and the trading instrument used to obtain it.

Futures also let you demonstrate practical market knowledge without introducing the full complexity of options:

- contract multipliers;
- notional exposure;
- initial and variation margin;
- expiry;
- contract rolls;
- cheapest-to-deliver considerations, if you go deeper;
- difference between futures price moves and the underlying cash bond exposure.

You do not need to model every futures-market detail in the first version. You can state your assumptions clearly and extend them later.

## Suggested scope boundary

I would avoid trying to support every bond type. Start with:

> **Government bond futures representing a small number of maturity buckets**

For example:

- short maturity;
- intermediate maturity;
- long maturity.

The exact contracts are less important initially than demonstrating the risk concepts. The system could represent each position with:

- contract price;
- contract multiplier;
- position quantity;
- maturity bucket;
- duration or DV01 estimate;
- roll schedule;
- margin requirement;
- historical return series.

Then the risk layer can report both:

1. **market-value contribution**, and  
2. **economic risk contribution**, such as DV01 or factor-based contribution.

That distinction itself would be a good artifact. A position can have a small market value but still make a material contribution to risk because of leverage or sensitivity.

## Recommended sequencing

I would structure the project in three stages.

### Stage 1: Equities and equity indices

Focus on the core workflow:

- measure portfolio risk;
- attribute risk to assets and factors;
- compare VaR methodologies;
- backtest the risk estimate;
- detect risk drift;
- produce a rebalance recommendation.

### Stage 2: Rates exposure through bond futures

Add the minimum rates-specific concepts:

- duration/DV01;
- yield-based stress scenarios;
- curve buckets;
- carry and roll assumptions;
- futures notional and margin;
- equity-rates correlation regimes.

The key question becomes:

> “What changed in the portfolio’s risk, and is the correct rebalance an equity trade, a duration trade, or both?”

### Stage 3: Options as a separate nonlinear-risk slice

Later, add options only when you have a decision that requires them:

- gamma concentration;
- volatility exposure;
- nonlinear stress losses;
- delta hedging;
- implied versus realised volatility;
- margin and liquidity under stress.

That would leverage your professional experience while keeping the main project coherent.

## Hiring narrative

This combination would support several versions of your career story:

### For systematic multi-asset firms

> “I started with equity risk and extended the workflow to rates, where risk is expressed through duration, curve exposure and futures implementation. The system identifies the factor driving portfolio risk and supports a decision about how to rebalance.”

### For portfolio-risk roles

> “I focused on the difference between nominal allocation and true risk allocation. The same percentage allocation can imply very different risk depending on volatility, duration, leverage and correlation.”

### For front-office rates or futures roles

> “I built risk and decision logic around government bond futures, including DV01, curve shocks, margin, roll and basis assumptions.”

### For options or derivatives roles

You would still have your professional Spreadex experience and could later add the options vertical slice as supporting evidence.

## Bottom line

I would not broaden the project into a generic multi-asset instrument library yet.

I would make the deliberate choice:

> **Equities first, then rates exposure through government bond futures.**

That is the best balance of:

- new domain evidence;
- relevance to systematic macro investing;
- meaningful portfolio-construction differences;
- manageable implementation complexity;
- practical front-office awareness;
- alignment with your existing career direction.

The important thing is that the extension should be framed around a changed **risk-and-rebalance decision**, not around the number of asset classes the software happens to support.
