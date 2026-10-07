from datetime import datetime

from src.domain.attribution import Attribution


def render_attribution_markdown(
    attribution: Attribution,
    *,
    portfolio_name: str,
    date: str,
    estimation_window: int,
) -> str:
    """Render attribution evidence as a PM-facing markdown artifact."""
    rows = [
        "| Asset | Weight | Portfolio risk contribution | % | Cumulative risk contribution |",
        "|---|---:|:---|---:|---:|",
    ]
    for contribution in attribution.risk_contributions:
        rows.append(
            f"| {contribution.asset} | {contribution.weight:.0%} | "
            f"{_contribution_bar(contribution.risk_contribution_pct)} | "
            f"{contribution.risk_contribution_pct:.0%} | "
            f"{contribution.cumulative_risk_contribution_pct:.0%} |"
        )

    return (
        "**ATTRIBUTION**<br><br>"
        f"**{portfolio_name}**<br>"
        f"As of {_format_date(date)}<br><br>"
        "**Where does risk live?**<br><br>"
        "Ranked by signed contribution to portfolio risk.<br><br>\n\n"
        + "\n".join(rows)
        + "\n\n"
    )


def _format_date(date_text: str) -> str:
    return datetime.fromisoformat(date_text).strftime("%d %B %Y")


def _contribution_bar(contribution_pct: float, width: int = 20) -> str:
    if contribution_pct >= 0:
        return "█" * round(contribution_pct * width)
    return "◄"
