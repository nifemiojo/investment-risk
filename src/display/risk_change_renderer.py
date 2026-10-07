from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd


def render_risk_change_markdown(comparison) -> str:
    """Render risk-change evidence as a compact Markdown report."""
    current = comparison.current
    previous_observation = comparison.previous_observation
    relative_change = (
        "—"
        if comparison.relative_var_change_pct is None
        else f"{comparison.relative_var_change_pct:+.2%}"
    )
    return f"""## RISK CHANGE — {comparison.portfolio_name}
**Current observation:** {_format_date(comparison.resolved_current_date)}<br>
**Previous observation requested:** {_format_date(comparison.requested_previous_observation_date)} · resolved close: {_format_date(comparison.resolved_previous_observation_date)}<br><br>

### Portfolio-level VaR

| Measure | Previous observation | Current observation | Change |
|---|---:|---:|---:|
| Annualised VaR | {previous_observation.var_annualised_pct:.2%} | {current.var_annualised_pct:.2%} | {(current.var_annualised_pct - previous_observation.var_annualised_pct) * 100:+.2f} pp |
| Currency VaR | £{previous_observation.var_currency:,.0f} | £{current.var_currency:,.0f} | £{comparison.absolute_var_change_currency:+,.0f} ({relative_change}) |

### Risk-budget
| Measure | Previous observation | Current observation | Change |
|---|---:|---:|---:|
| Risk-budget utilisation | {previous_observation.budget_utilisation:.2%} | {current.budget_utilisation:.2%} | {comparison.budget_utilisation_change_pct_points * 100:+.2f} pp |
| Breach status | {previous_observation.is_breach} | {current.is_breach} | — |

### Distribution context
| Measure | Previous observation | Current observation | Change |
|---|---:|---:|---:|
| Historical percentile | {previous_observation.percentile_rank:.0%} | {current.percentile_rank:.0%} | {comparison.historical_percentile_change_points * 100:+.0f} pp |

Requested and resolved dates are shown separately. Values describe portfolio-level VaR; the comparison does not attribute the change or recommend an action.
"""


def plot_trailing_portfolio_var(
    history: pd.Series,
    *,
    previous_observation_date: str,
    current_date: str,
    annualised_risk_budget: float | None = None,
):
    """Plot annualised as-of-close VaR history and comparison markers."""
    figure, axis = plt.subplots(figsize=(14, 5))
    axis.plot(
        history.index,
        history.values * 100,
        label="Annualised portfolio VaR",
    )
    if annualised_risk_budget is not None:
        axis.axhline(
            annualised_risk_budget * 100,
            color="black",
            linestyle="--",
            linewidth=1,
            label="Annualised risk budget",
        )
    axis.axvline(
        pd.Timestamp(previous_observation_date),
        color="tab:orange",
        linestyle=":",
        label="Previous observation",
    )
    axis.axvline(
        pd.Timestamp(current_date),
        color="tab:green",
        linestyle=":",
        label="Current close",
    )
    axis.set_ylabel("Annualised VaR (%)")
    axis.set_xlabel("Date")
    axis.set_title("Portfolio-level VaR")
    axis.legend()
    figure.tight_layout()
    return figure, axis


def _format_date(date_value: str) -> str:
    return datetime.fromisoformat(date_value).strftime("%d %b %Y")
