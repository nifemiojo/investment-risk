from datetime import datetime

from src.domain.risk_drift import RiskDrift


def render_risk_drift_markdown(
    risk_drift: RiskDrift,
    *,
    portfolio_name: str,
    date: str,
) -> str:
    """Render mandate risk-drift evidence as a compact markdown artifact."""
    rows = [
        "| Asset | Weight | Target risk contribution | Current risk contribution | Signed drift | Absolute drift |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for observation in risk_drift.observations:
        rows.append(
            f"| {observation.asset} | "
            f"{observation.weight:.0%} | "
            f"{observation.target_risk_contribution_pct:.0%} | "
            f"{observation.current_risk_contribution_pct:.0%} | "
            f"{observation.signed_drift * 100:+.2f} pp | "
            f"{observation.absolute_drift * 100:.2f} pp |"
        )

    return (
        "**RISK CONTRIBUTION DRIFT**<br><br>"
        f"**{portfolio_name}**<br>"
        f"As of {_format_date(date)}<br><br>\n\n"
        + "\n".join(rows)
        + "\n\n"
    )


def _format_date(date_text: str) -> str:
    return datetime.fromisoformat(date_text).strftime("%d %B %Y")


__all__ = ["render_risk_drift_markdown"]


