# The Parameter Problem and Overfitting in VaR Models

**Date:** 2026-07-21
**Topic:** Why more parameters make backtests look better but models perform worse
**Turn:** 008c

## The seductive intuition

You have three parameters: VaR window (252 or 504), decay factor λ (0.90–0.99), and vol window (10–60). That's roughly 2 × 10 × 5 = 100 possible combinations. One of them will produce a breach rate that's closest to 5% with the most even distribution across regimes.

The intuition says: "Great! More knobs to turn means we can tune the model to be exactly right. Find the combination that worked best historically and use that going forward."

This intuition is wrong. Here's why.

## The overfitting trade-off

Every parameter you add does two things simultaneously:

| Effect | What it means |
|--------|--------------|
| **Reduces bias** | The model can capture more complex patterns in the data |
| **Increases variance** | The model starts fitting noise, not signal |

The total error of a model is: **bias² + variance + irreducible error.** Adding parameters reduces bias (good) but increases variance (bad). The net effect depends on how much signal exists relative to noise.

In financial returns, the signal-to-noise ratio is very low. Daily returns are ~99% noise. Adding parameters to a noise-dominated process mainly fits the noise.

## A concrete thought experiment

Take SPY daily returns from 2018–2026. Split into two halves: 2018–2021 (training) and 2022–2026 (testing). Now:

1. Try all 100 parameter combinations on the training period
2. Pick the combination with the most consistent breach rates
3. Apply that combination to the test period

What happens? The "best" combination on the training data will almost certainly NOT be the best on the test data. Why? Because the training data contains specific noise patterns (the exact sequence of COVID returns, the exact timing of the 2020 recovery) that won't repeat.

The parameter combination that "won" the training period did so partly by fitting real patterns (the COVID crash was genuinely high-vol) and partly by fitting noise (the exact day COVID returns peaked, the exact day vol subsided). The noise-fitting doesn't generalise.

## Why this is counterintuitive

You run 100 backtests. One combination gives 4.98% breaches on training — nearly perfect. Your brain says: "This model understood the data." The model didn't understand anything. It's a percentile calculation with weights. It can't "understand." The 4.98% is partially luck — another random draw of market history would have produced a different "best" combination.

The statistical term is **data snooping**: when you use the same data to both choose the model AND evaluate it, your evaluation is contaminated. You've peeked at the answer.

## The three-parameter reality

With three parameters, the space of possible VaR estimates on any given day is wide:

- Window=252, λ=0.90, vol_window=10: Very reactive, noisy VaR
- Window=504, λ=0.99, vol_window=60: Very stable, slow VaR
- Window=252, λ=0.94, vol_window=20: The "standard" combination

In a backtest, the reactive combination will look terrible during calm periods (too many breaches) but great during crises (VaR rises fast). The stable combination will look great during calm (few breaches) but terrible during crises (VaR is slow). The "best" combination depends entirely on which period you care about — and you only know which periods mattered AFTER they happen.

## The right way to think about parameters

Parameters should be chosen based on **what you believe about the world**, not what optimises a backtest:

| Parameter | What belief does it encode? |
|-----------|---------------------------|
| Window = 252 | "One year of trading days captures a full market cycle." |
| λ = 0.94 | "Yesterday matters ~6% more than the day before. This is the RiskMetrics standard." |
| Vol window = 20 | "One month of trading days gives a reasonable vol estimate." |

These are defensible a priori — you can justify them before seeing the data. A parameter chosen because it gave 4.98% breaches in a backtest is not defensible — it's the result of a search over noise.

## The safeguard: out-of-sample testing

The only honest way to evaluate a model with chosen parameters:

1. **Decide parameters first** — based on beliefs, theory, or industry standards
2. **Fix them** — no looking at results and adjusting
3. **Run the backtest once** — one evaluation, one breach rate
4. **Accept the result** — if it's 6.2% instead of 5.0%, that's the honest answer

If you iterate — run the backtest, see the breach rate, adjust parameters, run again — you've contaminated the evaluation. The final breach rate is no longer an honest measure of model performance; it's a measure of how well you can fit noise.

## The meta-point for this project

This is why we've been disciplined about parameters throughout. We chose 252 days because it's the industry standard (one trading year). We chose λ=0.94 because it's the RiskMetrics standard. We chose the 20-day vol window because it's standard for daily data. We didn't optimise — we selected based on defensible priors and then evaluated honestly.

The decay-weighted VaR produces ~5.97% breaches against an expected 5.00%. The equal-weighted VaR produces 4.76%. These are honest numbers — they weren't achieved by searching for the right λ or window. They're what the model actually does with reasonable, pre-committed parameters.

The alternative — running 100 combinations and picking the one with 5.02% — would produce a model that looks better on paper but performs worse out of sample. The extra 0.98% of "accuracy" is mostly fitted noise.