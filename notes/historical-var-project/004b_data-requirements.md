# How much data for meaningful rolling VaR?

**Date:** 2026-07-12
**Topic:** Minimum data requirements for rolling VaR across three windows
**Turn:** 004b

## User request

How much data do we need in order to calculate a meaningful rolling VaR over the three windows?

## Work and response

The bottleneck is the 504-day window. Here's the arithmetic:

| Window | Warm-up needed | Rolling estimates desired | Total data needed |
|--------|---------------|--------------------------|-------------------|
| 60-day | 60 trading days (~3 months) | 2+ years | ~2.5 years |
| 252-day | 252 trading days (~1 year) | 3+ years | ~4 years |
| 504-day | 504 trading days (~2 years) | 4+ years | ~6 years |

But the real constraint isn't the count — it's **what we want to see**. We want the 504-day window to produce a VaR estimate for late February 2020, so we can watch it fail to react as COVID crashes the market. That means the warm-up needs to end before COVID:

```
504-day warm-up: 2018-01-02 → 2020-01-31  (~504 trading days)
First VaR estimate: 2020-02-03
Rolling estimates:  2020-02-03 → 2026-07-10  (~1,600 trading days)
```

So the minimum is **2018-01-01 to present** — roughly 8.5 years, ~2,140 trading days. That gives us:

- A calm pre-COVID warm-up for all three windows
- The 504-day VaR starting low in Feb 2020 (using only 2018-2019 data)
- COVID crash visible as breaches piling up while 252-day and 504-day VaR slowly rise
- 2022 rate hikes as a second regime-change test
- 2023-2026 calm period to see if the 504-day window stays elevated after the crisis exits

The 504-day window is the limiting factor. If we started in 2020, we wouldn't get a 504-day VaR until 2022 — missing the COVID episode entirely.