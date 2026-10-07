from datetime import datetime

from src.domain.rebalance_trigger import RebalanceTrigger


def render_rebalance_review_markdown(
    rebalance_trigger: RebalanceTrigger,
    *,
    portfolio_name: str,
    date: str,
) -> str:
    """Render tolerance-band evidence and directional review suggestions."""
    review_status = "REVIEW REBALANCE" if rebalance_trigger.triggered else "WITHIN TOLERANCE"
    tolerance_pp = rebalance_trigger.tolerance * 100
    rows = [
        "| Asset | Target | Current | Drift | Band | Status | Suggested direction |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for observation in rebalance_trigger.observations:
        status = "Outside" if observation.outside_tolerance else "Within"
        rows.append(
            f"| {observation.asset} | "
            f"{observation.target_risk_contribution_pct:.0%} | "
            f"{observation.current_risk_contribution_pct:.0%} | "
            f"{observation.signed_drift * 100:+.2f} pp | "
            f"±{observation.tolerance * 100:.2f} pp | "
            f"{status} | "
            f"{observation.suggested_direction} |"
        )

    return (
        "**RISK DRIFT — REBALANCE REVIEW**<br><br>"
        f"**{portfolio_name}**<br>"
        f"As of {_format_date(date)}<br><br>\n\n"
        f"Tolerance band: ±{tolerance_pp:.2f} percentage points<br><br>\n\n"
        f"**{review_status}**<br><br>\n\n"
        + "\n".join(rows)
        + "\n\n"
        "The trigger identifies risk-contribution drift outside the configured "
        "tolerance band. It does not determine trade size, execution, cost, "
        "liquidity, or whether the PM should rebalance.\n\n"
    )


def _format_date(date_text: str) -> str:
    return datetime.fromisoformat(date_text).strftime("%d %B %Y")


__all__ = ["render_rebalance_review_markdown"]


