from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from src.domain.portfolio_risk import PortfolioRisk, VolatilityObservation


def render_portfolio_risk_markdown(
    portfolio_risk: PortfolioRisk,
    *,
    portfolio_name: str,
    requested_date: str,
) -> str:
    """Render the current portfolio-risk level as Markdown."""
    history = portfolio_risk.volatility_history
    latest = history[-1] if history else None
    previous_month_volatility = getattr(
        portfolio_risk, "previous_month_volatility", None
    )
    previous_month_date = getattr(
        portfolio_risk, "previous_month_observation_date", None
    )

    lines = [
        "## Portfolio risk",
        "",
        f"**{portfolio_name}**<br>",
        f"As of {_format_date(requested_date)}<br>",
        "",
        f"**Current daily volatility:** {portfolio_risk.current_volatility:.2%}<br>",
    ]
    if latest is not None:
        lines.append(
            f"Latest calculated observation: {_format_date(latest.date)}<br>"
        )
    if previous_month_volatility is not None:
        change = portfolio_risk.current_volatility - previous_month_volatility
        lines.extend(
            [
                f"Previous daily volatility ({_format_date(previous_month_date)}): "
                f"{previous_month_volatility:.2%}<br>",
                f"Change since previous month: {change * 100:+.2f} percentage points",
            ]
        )
    return "\n".join(lines)


def plot_rolling_portfolio_volatility(
    volatility_history: tuple[VolatilityObservation, ...],
    *,
    portfolio_name: str,
    requested_date: str,
):
    """Plot rolling daily portfolio volatility and return the Matplotlib figure."""
    dates = [datetime.fromisoformat(item.date) for item in volatility_history]
    values = [item.volatility for item in volatility_history]

    figure, axis = plt.subplots(figsize=(10, 4))
    axis.plot(dates, values, label=portfolio_name)
    if values:
        axis.scatter(dates[-1], values[-1], zorder=3)
    axis.set_title("Rolling Daily Portfolio Volatility — Last Year")
    axis.set_xlabel("Date")
    axis.set_ylabel("Daily volatility (%)")
    axis.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    axis.grid(True, alpha=0.3)
    figure.autofmt_xdate()
    figure.tight_layout()
    return figure


def _format_date(date_text: str) -> str:
    return datetime.fromisoformat(date_text).strftime("%d %B %Y")


__all__ = [
    "plot_rolling_portfolio_volatility",
    "render_portfolio_risk_markdown",
]
