def render_snapshot_markdown(snapshot):
    """Convert a RiskSnapshot into a markdown string for notebook display."""
    utilisation_bar = _render_utilisation_bar(snapshot.budget_utilisation)
    level_bar = _render_level_bar(snapshot.percentile_rank)
    breach_icon = "✅" if not snapshot.is_breach else "🚨 BREACH"
    ordinal = _ordinal(snapshot.percentile_rank)
    lookback = _format_lookback(snapshot.distribution_lookback_start)

    return f"""
## RISK SNAPSHOT — {snapshot.portfolio_name}
**{_format_timestamp(snapshot.timestamp)}**<br>

### Portfolio
NAV: £{snapshot.nav:,.0f}<br>

### Portfolio VaR
£{snapshot.var_currency:,.0f} ({snapshot.var_pct:.2%} of NAV daily)<br>

### Risk Budget
Annualised VaR: {snapshot.var_annualised_pct:.1%} of NAV  |  Limit: {snapshot.risk_budget_annual_pct:.0%} of NAV<br>

{utilisation_bar} **{snapshot.budget_utilisation:.0%}** utilised<br>
{breach_icon}<br>

*Limit = {snapshot.risk_budget_annual_pct:.0%} annualised VaR at 95% confidence — the maximum loss the
mandate allows in a typical year, set by the Investment Policy Statement.*

### Is This Normal?
{level_bar} **{ordinal} percentile**<br>

Today's VaR ranks at the {ordinal} percentile of this portfolio's own trailing VaR history since {lookback} — {snapshot.percentile_meaning}.

### Decision
→ {snapshot.decision}<br>
"""


def _format_timestamp(date_str: str) -> str:
    """Format '2022-03-31' → '31 Mar 2022'."""
    from datetime import datetime
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%d %b %Y")


def _format_lookback(date_str: str) -> str:
    """Format '2019-01-02' → 'Jan 2019'."""
    from datetime import datetime
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%b %Y")


def _ordinal(percentile_rank: float) -> str:
    """Format 0.53 → '53rd'."""
    pct = int(round(percentile_rank * 100))
    if 11 <= pct % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(pct % 10, "th")
    return f"{pct}{suffix}"


def _render_utilisation_bar(pct, width=20):
    filled = int(pct * width)
    return "█" * filled + "░" * (width - filled)


def _render_level_bar(pct, width=20):
    filled = int(pct * width)
    return "▓" * filled + "░" * (width - filled)
