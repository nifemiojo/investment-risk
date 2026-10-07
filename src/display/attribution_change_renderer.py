from datetime import datetime

from src.domain.attribution_change import AttributionChange


def render_attribution_change_markdown(
    attribution_change: AttributionChange,
    *,
    portfolio_name: str,
) -> str:
    """Render contribution-change evidence in the compact attribution style."""
    rows = [
        "| Asset | Reference contribution % | Current contribution % | Change, percentage points |",
        "|---|---:|---:|---:|",
    ]
    for observation in attribution_change.observations:
        rows.append(
            f"| {observation.asset} | "
            f"{observation.reference_contribution_percentage:.0%} | "
            f"{observation.current_contribution_percentage:.0%} | "
            f"{observation.change_percentage_points * 100:+.2f} pp |"
        )

    return (
        "**CONTRIBUTION CHANGE**<br><br>"
        f"**{portfolio_name}**<br>"
        f"Reference as of {_format_date(attribution_change.reference_date)}<br>"
        f"Current as of {_format_date(attribution_change.current_date)}<br><br>"
        "**How has risk contribution changed?**<br><br>\n\n"
        + "\n".join(rows)
        + "\n\n"
    )


def _format_date(date_text: str) -> str:
    return datetime.fromisoformat(date_text).strftime("%d %B %Y")


__all__ = ["render_attribution_change_markdown"]
