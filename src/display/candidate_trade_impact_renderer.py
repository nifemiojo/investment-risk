from datetime import datetime

from src.domain.candidate_trade_impact import CandidateTradeImpact


def render_candidate_trade_impact_markdown(
    impact: CandidateTradeImpact,
    *,
    portfolio_name: str,
    date: str,
) -> str:
    """Render one hypothetical candidate and its before/after evidence."""
    candidate = impact.candidate
    summary_rows = [
        "| Field | Value |",
        "|---|---|",
        f"| Donor | {candidate.donor_asset} |",
        f"| Receiver | {candidate.receiver_asset} |",
        f"| Donor weight change | {-candidate.transfer_weight * 100:.2f} pp |",
        f"| Receiver weight change | {candidate.transfer_weight * 100:+.2f} pp |",
        "| Selection rule | Largest positive drift to largest negative drift |",
        "| Candidate status | Hypothetical |",
    ]
    current = impact.current_risk
    proposed = impact.proposed_risk
    current_max = max(item.absolute_drift for item in current.observations)
    proposed_max = max(item.absolute_drift for item in proposed.observations)
    current_total = sum(item.absolute_drift for item in current.observations)
    proposed_total = sum(item.absolute_drift for item in proposed.observations)
    portfolio_rows = [
        "| Measure | Current | Proposed | Change |",
        "|---|---:|---:|---:|",
        f"| Portfolio volatility | {current.portfolio_volatility:.4f} | {proposed.portfolio_volatility:.4f} | {impact.portfolio_volatility_change:+.4f} |",
        f"| Maximum absolute RC drift | {current_max * 100:.2f} pp | {proposed_max * 100:.2f} pp | {impact.maximum_absolute_drift_change * 100:+.2f} pp |",
        f"| Total absolute RC drift | {current_total * 100:.2f} pp | {proposed_total * 100:.2f} pp | {impact.total_absolute_drift_change * 100:+.2f} pp |",
        f"| Assets outside tolerance | {impact.current_breached_asset_count} | {impact.proposed_breached_asset_count} | {impact.breached_asset_count_change:+d} |",
    ]
    asset_rows = [
        "| Asset | Current RC | Proposed RC | RC change | Current drift | Proposed drift | Drift change |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in impact.asset_impacts:
        asset_rows.append(
            f"| {item.asset} | {item.current_risk_contribution_pct:.2%} | "
            f"{item.proposed_risk_contribution_pct:.2%} | {item.risk_contribution_change * 100:+.2f} pp | "
            f"{item.current_drift * 100:+.2f} pp | {item.proposed_drift * 100:+.2f} pp | "
            f"{item.drift_change * 100:+.2f} pp |"
        )

    return (
        "**CANDIDATE TRADE IMPACT**<br><br>"
        f"**{portfolio_name}**<br>"
        f"As of {_format_date(date)}<br><br>\n\n"
        f"**Candidate:** Sell {candidate.donor_asset} / Buy {candidate.receiver_asset}<br>"
        f"Weight transfer: {candidate.transfer_weight * 100:.2f} percentage points<br><br>\n\n"
        + "\n".join(summary_rows)
        + "\n\nThis is a hypothetical equal-and-opposite weight transfer. "
        "It is not an optimised rebalance or an executable order.\n\n"
        + "**Portfolio-level impact**\n\n"
        + "\n".join(portfolio_rows)
        + "\n\n**Asset-level impact**\n\n"
        + "\n".join(asset_rows)
        + "\n\nThe candidate is shown for hypothetical impact assessment.\n"
    )


def _format_date(date_text: str) -> str:
    return datetime.fromisoformat(date_text).strftime("%d %B %Y")


__all__ = ["render_candidate_trade_impact_markdown"]


