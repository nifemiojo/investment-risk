# Why Daily? The Frequency Question

**Date:** 2026-07-10
**Topic:** Why daily is the convention for VaR simulation — empirical, practical, and decision-driven reasons, and what you lose at other frequencies

---

## The Honest Answer

Daily is a choice, not a fact. It's chosen for three reasons: empirical, practical, and decision-aligned. But it's worth understanding what you sacrifice.

---

## Reason 1: Empirical — This Is Where the Signal Lives

Volatility clustering is most pronounced at daily frequency. Here's what happens at other frequencies:

### Too High: Intraday (Minutes, Ticks)

At very high frequencies, you're measuring market microstructure noise, not return dynamics:

- **Bid-ask bounce:** A trade at the bid followed by a trade at the ask looks like a return, but it's just the spread
- **Order flow effects:** Price moves from order imbalance, not from changes in the fundamental risk process
- **Overnight gaps:** The biggest moves happen when markets are closed — intraday data misses the most important shocks

If you fit a GARCH model to 1-minute returns, you're mostly modeling noise. The volatility dynamics you care about (persistent shifts in risk) get buried.

### Too Low: Monthly, Quarterly

At low frequencies, you don't have enough observations to estimate time-varying volatility:

- 10 years of monthly data = 120 observations. You can't reliably estimate a GARCH model with 120 data points — the parameters won't converge.
- Volatility clustering is a *persistent but decaying* effect. If a shock happened 3 weeks ago, is today's volatility still elevated? Monthly data can't tell you.

### The Sweet Spot

Daily frequency captures the persistence of volatility (shocks decay over days to weeks, not minutes or months) while providing enough observations for estimation (252 per year, 1,260 over 5 years — enough for GARCH parameter convergence).

---

## Reason 2: Practical — Daily Data Is What You Have

- **Availability:** Daily closing prices are clean, standardized, and available for nearly every traded instrument going back decades
- **Quality:** Daily data has been cleaned — corporate actions adjusted, splits handled, outliers reviewed
- **No async issues:** All assets close at the same time (within a timezone). Intraday data across timezones creates async problems — the 2pm FTSE price and 2pm S&P price aren't from the same moment
- **System alignment:** Spreadex, like most firms, runs end-of-day risk calculations. The systems are built around the daily cycle

This isn't a satisfying theoretical answer, but it matters. You use daily data because that's what the infrastructure produces and what decades of research have been built on.

---

## Reason 3: Decision-Aligned — The VaR Horizon Is 1 Day

The VaR question is: "What could I lose by tomorrow's close?" The natural simulation frequency is the same as the decision horizon.

If you were managing intraday risk for a high-frequency trading desk, you'd simulate at minute or second frequency. That's a different problem with different tools. For the risk management VaR is designed for — end-of-day position monitoring, regulatory capital, portfolio construction — daily is the right match.

---

## What You Lose by Choosing Daily

You're right that this is a choice with consequences:

### 1. You Miss Intraday Risk

If a position can blow up between 10am and 2pm, daily VaR doesn't see it. This is why intraday risk limits and real-time monitoring exist separately from VaR.

### 2. You Assume the Overnight Close-to-Close Return Is the Right Unit

Markets gap overnight. The close-to-close return bundles the overnight shock with the day's trading. Is that the right unit of observation? Maybe not — but it's the one we have clean data for.

### 3. Multi-Scale Volatility Dynamics Exist

Research on **realized volatility** and **HAR models** shows that volatility operates at multiple timescales simultaneously:

$$RV_{t+1} = \beta_0 + \beta_D \cdot RV_t^{(daily)} + \beta_W \cdot RV_t^{(weekly)} + \beta_M \cdot RV_t^{(monthly)} + \epsilon_t$$

**Terms:**
- $RV_{t+1}$: realized volatility over the next day
- $RV_t^{(daily)}$: yesterday's realized volatility
- $RV_t^{(weekly)}$: average realized volatility over the past 5 days
- $RV_t^{(monthly)}$: average realized volatility over the past 22 days

The insight: yesterday's vol matters, last week's vol matters, AND last month's vol matters — all at the same time, with different decay rates. A simple daily GARCH captures one of these effects. The HAR model captures all three.

---

## The Real Answer

Daily is chosen because it's where the strongest volatility clustering signal lives, it's what data infrastructure supports, and it aligns with the decision horizon.

But you're right to push on this. **Frequency is a modeling choice, not a law of nature.** A GARCH model estimated on daily data will give different VaR estimates than one estimated on weekly data. There's no "correct" frequency — there's only the frequency that best captures the risk dynamics relevant to your decision horizon.

And this is itself a Monte Carlo failure mode: **your simulation is only as good as the process you specify, and the process specification includes a frequency choice that you probably inherited from convention rather than tested.**

---

## Check-In

Does that land? The frequency choice is partly empirical (signal strength), partly practical (data availability), and partly a modeling assumption you should be aware of.

And here's the practical question: **at Spreadex, is the autohedging system's risk monitoring at daily frequency? Or does it run intraday? If intraday, what does that imply about the appropriate simulation frequency for a Monte Carlo VaR model of the room?**