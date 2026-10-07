# Why 252? Trading Days in a Year

**Date:** 2026-07-06
**Topic:** The origin of the 252-day convention

---

## The Arithmetic

$$
\begin{aligned}
365 &\text{ — calendar days in a year} \\
- 104 &\text{ — weekends (52 Saturdays + 52 Sundays)} \\
\hline
261 &\text{ — weekdays} \\
- 9 &\text{ — US market holidays (approx: New Year's, MLK, Presidents',} \\
  &\text{    Memorial, Juneteenth, Independence, Labor, Thanksgiving, Christmas)} \\
\hline
252 &\text{ — trading days}
\end{aligned}
$$

The exact number varies year to year (250–253), but 252 is the accepted convention because it's close enough and nicely divisible — it factors into $252 = 2^2 \times 3^2 \times 7$ and $252 \approx 250$, which makes mental annualization easy (daily vol $\times \sqrt{252} \approx$ daily vol $\times 16$).

---

## Why It Matters for VaR

If you use a 1-year window of daily returns for historical VaR, you're implicitly saying: "one annual cycle of market behavior is the right amount of history." Not two earnings seasons. Not one quarter. A full year — covering all four seasons, one full cycle of earnings announcements, and the typical ebb and flow of volatility through the calendar.

---

## For Non-US Markets

Different exchanges, different counts:
- **UK (LSE):** ~253 (fewer holidays, no Thanksgiving)
- **Crypto:** 365 — trades every day, no weekends, no holidays
- **FX:** ~260–262 (trades weekends via some venues, but liquidity is thin)

The principle is the same: pick the number that represents one year of actual trading in your market. For your work at Spreadex, which covers equities, FX, futures, commodities, and crypto, you'd use different day counts for different asset classes — or standardize to 252 for consistency and explainability.
