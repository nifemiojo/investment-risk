from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateTrade:
    """One hypothetical equal-and-opposite portfolio-weight transfer."""

    donor_asset: str
    receiver_asset: str
    transfer_weight: float

    def __post_init__(self) -> None:
        if not self.donor_asset or not self.receiver_asset:
            raise ValueError("Donor and receiver assets are required.")
        if self.donor_asset == self.receiver_asset:
            raise ValueError("Donor and receiver assets must differ.")
        if self.transfer_weight <= 0:
            raise ValueError("Transfer weight must be positive.")

    def weight_changes(self) -> dict[str, float]:
        return {
            self.donor_asset: -self.transfer_weight,
            self.receiver_asset: self.transfer_weight,
        }


@dataclass(frozen=True)
class CandidateTradeResult:
    """One generated candidate or an expected no-candidate state."""

    candidate: CandidateTrade | None
    reason: str | None = None


__all__ = ["CandidateTrade", "CandidateTradeResult"]


# Explicitly re-exported for consumers that discover module symbols dynamically.
