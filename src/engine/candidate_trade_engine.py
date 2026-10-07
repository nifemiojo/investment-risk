from src.domain.candidate_trade import CandidateTrade, CandidateTradeResult
from src.domain.rebalance_trigger import RebalanceTrigger


class CandidateTradeEngine:
    """Generate one fixed-weight transfer from reviewed contribution drift."""

    def generate(
        self,
        reviewed_drift: RebalanceTrigger,
        transfer_weight: float,
    ) -> CandidateTradeResult:
        if transfer_weight <= 0:
            raise ValueError("Transfer weight must be positive.")

        eligible_donors = [
            observation
            for observation in reviewed_drift.observations
            if observation.outside_tolerance and observation.signed_drift > 0
        ]
        eligible_receivers = [
            observation
            for observation in reviewed_drift.observations
            if observation.outside_tolerance and observation.signed_drift < 0
        ]
        if not eligible_donors or not eligible_receivers:
            return CandidateTradeResult(
                candidate=None,
                reason="No eligible donor and receiver were available.",
            )

        donor = max(eligible_donors, key=lambda item: (item.signed_drift, item.asset))
        receiver = min(eligible_receivers, key=lambda item: (item.signed_drift, item.asset))
        return CandidateTradeResult(
            candidate=CandidateTrade(
                donor_asset=donor.asset,
                receiver_asset=receiver.asset,
                transfer_weight=transfer_weight,
            )
        )


__all__ = ["CandidateTradeEngine"]
